import json

from agent.commands import logger
from agent.config.properties import BASE_SERVICES_PATH
from agent.constants import DOCKER_COMPOSE_FILE
from agent.exceptions.agent_error import AgentError


def get_base_service_path(service_id):
    return f"{BASE_SERVICES_PATH}/{service_id}"


def get_docker_compose_path(service_id):
    return f"{get_base_service_path(service_id)}/{DOCKER_COMPOSE_FILE}"


def get_field_from_body(key, body):
    try:
        return body[key]
    except KeyError as e:
        logger.error(f"{body} does not contain any {key}!")
        raise AgentError(body, e)


def prepare_message_to_send(message_type, body):
    message = dict(messageType=message_type, body=body)
    return json.dumps(message).encode("utf-8")


