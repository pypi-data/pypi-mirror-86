import json
from queue import Queue
from typing import Dict, Any, Union

from pika.exceptions import AMQPConnectionError
from twisted.internet import reactor

from agent.rabbitmq.client import RabbitMqClient
from agent.rabbitmq.message_types import DeclareQueueMessage
from agent.services.utils import get_services_id_list

publisher_queue = Queue()


class RabbitMQPublisher:
    def __init__(self):
        self.client = RabbitMqClient()
        self.logger = self.client.logger
        self._is_publishing_active = False

    def start_publishing_messages(self):
        self.logger.info("Starting publishing messages to RabbitMQ")
        self._is_publishing_active = True
        reactor.callInThread(self._run)

    def stop_publishing_messages(self):
        if self._is_publishing_active and publisher_queue.empty():
            self.logger.info("Stopping publishing messages to RabbitMQ")
            publisher_queue.put(None)

    def _run(self) -> None:
        self._declare_publish_queues()
        while True:
            message = publisher_queue.get()
            if message is None:
                self.logger.info("None in publisher_queue")
                break
            self._safe_process_message(message)
        self._is_publishing_active = False

    def _safe_process_message(self, message: Union[DeclareQueueMessage, Dict[str, Any]]) -> None:
        try:
            self._process_message(message)
        except AMQPConnectionError:
            publisher_queue.put(message)

    def _process_message(self, message: Union[DeclareQueueMessage, Dict[str, Any]]) -> None:
        if isinstance(message, DeclareQueueMessage):
            self._declare_publish_queue(message.topic)
        else:
            self._publish_message(message)

    def _declare_publish_queues(self) -> None:
        queues = get_services_id_list()
        for queue in queues:
            self._declare_publish_queue(queue)

    def _declare_publish_queue(self, queue: str) -> None:
        if queue not in self.client.declared_queues:
            self.client.declare_queue(queue)

    def _publish_message(self, message: Dict[str, Any]) -> None:
        rabbitmq_message = json.dumps(message).encode("utf-8")
        self.client.publish_message(
            message=rabbitmq_message,
            message_type=message["messageType"],
            topic=message["nodeServiceId"],
        )
