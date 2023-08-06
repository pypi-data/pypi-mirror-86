from typing import Any, Dict
from urllib.error import HTTPError

import requests

from agent.certificates.certificate_client import CertificateClient
from agent.certificates.certificate_config_generator import CertificateConfigGenerator
from agent.commands import logger
from agent.commands.docker_commands import docker_compose_pull, docker_compose_up
from agent.commands.service import Service
from agent.commands.service_config_provider import provide_service_config
from agent.commands.service_creator import create_service
from agent.commands.utils import get_docker_compose_path
from agent.config.properties import BASE_SERVICES_PATH, REXSIO_HOST
from agent.exceptions.agent_error import AgentError
from agent.rabbitmq.message_types import DeclareQueueMessage
from agent.rabbitmq.publisher import publisher_queue
from agent.websocket.utils import get_access_token


def provision_service(body: Dict[str, Any]) -> None:
    service = create_service(body)
    create_service_queue(service.id)
    provide_service_config(service_id=service.id, config=service.config)
    generate_service_certificate(service.id)
    start_service(service)
    logger.info(f"Service {service.type}/{service.id} is running")


def generate_service_certificate(service_id: str) -> None:
    token = get_access_token()
    rexsio_path = f"https://{REXSIO_HOST}"
    client = CertificateClient(base_path=rexsio_path, access_token=token)
    generator = CertificateConfigGenerator(
        service_configs_path=BASE_SERVICES_PATH, cert_client=client
    )
    generator.generate_cert_config(service_id)


def create_service_queue(topic: str) -> None:
    publisher_queue.put(DeclareQueueMessage(topic=topic))


def start_service(service: Service) -> None:
    docker_compose_file_path = _download_docker_compose(
        compose_url=service.compose_url, service_id=service.id
    )
    docker_compose_pull(docker_compose_file_path)
    docker_compose_up(docker_compose_file_path)


def _download_docker_compose(compose_url: str, service_id: str) -> str:
    file_path = get_docker_compose_path(service_id)
    try:
        _get_docker_compose_file(url=compose_url, filename=file_path)
    except HTTPError as error:
        logger.error(
            f"Docker compose file download failed: {file_path}, url: {compose_url}"
        )
        raise AgentError(expression=compose_url, message=error)
    logger.info(f"Docker compose file downloaded: {file_path}")
    return file_path


def _get_docker_compose_file(url: str, filename: str) -> None:
    r = requests.get(url)
    r.raise_for_status()
    with open(filename, "wb") as file:
        file.write(r.content)
