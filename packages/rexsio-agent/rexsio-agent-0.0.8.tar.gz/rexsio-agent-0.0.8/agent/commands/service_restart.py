import subprocess
from typing import Any, Dict, List

from agent.commands import logger
from agent.commands.docker_commands import docker_compose_restart
from agent.commands.utils import get_docker_compose_path, get_field_from_body
from agent.commands.service_config_provider import provide_service_config
from agent.constants import SERVICE_RESTARTING, SERVICE_DOWN, SERVICE_UP
from agent.services.status_sender import send_status


def restart_service(body: Dict[str, Any]) -> None:
    service_id = get_field_from_body("nodeServiceId", body)
    config = get_field_from_body("config", body)
    provide_service_config(config=config, service_id=service_id)
    logger.info(f"Restarting {service_id} service")
    _restart_service_by_id(service_id)


def restart_services(service_id_list: List[str]) -> None:
    for service_id in service_id_list:
        logger.info(f"Service {service_id} is DOWN, restarting")
        _restart_service_by_id(service_id)


def _restart_service_by_id(service_id: str) -> None:
    send_status(service_id, SERVICE_RESTARTING)
    docker_compose_path = get_docker_compose_path(service_id)
    try:
        docker_compose_restart(docker_compose_path)
        send_status(service_id, SERVICE_UP)
    except subprocess.CalledProcessError:
        send_status(service_id, SERVICE_DOWN)
