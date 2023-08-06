import json
import os
from pathlib import Path
from typing import Dict, Any

from agent.commands import logger
from agent.commands.service_config_decryptor import decrypt_properties
from agent.commands.utils import get_base_service_path
from agent.config.properties import RABBITMQ_PASS
from agent.exceptions.agent_error import AgentError
from agent.smart_card.smart_card_resolver import resolve_smart_card_reader_env


def provide_service_config(config: Dict[str, Any], service_id: str) -> None:
    service_config = _resolve_service_config(config)
    _save_config_file(service_config=service_config, service_id=service_id)
    resolve_smart_card_reader_env(config=service_config)


def _save_config_file(service_config: Dict[str, Any], service_id: str) -> None:
    config_directory = _create_config_path_for_service(service_id)
    file_path = f"{config_directory}/config.json"
    _save_data_to_file(service_config, file_path)
    logger.info(f"Config updated: {file_path}")


def _resolve_service_config(config: Dict[str, Any]) -> Dict[str, Any]:
    properties = config.pop("properties")
    decrypted_properties = decrypt_properties(config.pop("encryptedProperties"))
    _add_rabbitmq_pass_to_config(config)
    _add_warning_info(config)
    return {**config, **properties, **decrypted_properties}


def _add_rabbitmq_pass_to_config(config: Dict[str, Any]) -> None:
    config["rabbitmqPass"] = RABBITMQ_PASS


def _add_warning_info(config: Dict[str, Any]) -> None:
    config["attention"] = "FILE GENERATED AUTOMATICALLY. DO NOT EDIT"


def _save_data_to_file(data, file_path):
    with open(file_path, "w") as f:
        json.dump(data, f)


def _create_config_path_for_service(service_id: str) -> str:
    service_base_path = get_base_service_path(service_id)
    config_path = f"{service_base_path}/config"
    _create_config_path_if_needed(config_path)
    return config_path


def _create_config_path_if_needed(config_path: str) -> None:
    if not os.path.isdir(config_path):
        logger.info(f"Directory {config_path} does not exist, creating one")
        try:
            Path(config_path).mkdir(parents=True, exist_ok=True)
        except PermissionError as e:
            logger.error(f"User has no permission to this path: {config_path}")
            raise AgentError(config_path, e)
