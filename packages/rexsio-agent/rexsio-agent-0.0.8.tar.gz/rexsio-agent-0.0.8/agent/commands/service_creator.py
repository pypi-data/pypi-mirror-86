from typing import Dict, Any

from agent.commands.service import Service
from agent.commands.utils import get_field_from_body


def create_service(body: Dict[str, Any]) -> Service:
    return Service(
        type=get_field_from_body("serviceType", body),
        id=get_field_from_body("nodeServiceId", body),
        config=get_field_from_body("config", body),
        compose_url=get_field_from_body("dockerComposeUrl", body),
        version=get_field_from_body("version", body),
    )