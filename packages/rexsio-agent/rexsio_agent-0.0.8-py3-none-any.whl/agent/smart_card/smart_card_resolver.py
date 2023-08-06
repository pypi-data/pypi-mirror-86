import os
from typing import Dict, Any

from agent.smart_card import logger
from agent.smart_card.smart_card_reader import find_smart_card_reader_address


def resolve_smart_card_reader_env(config: Dict[str, Any]) -> None:
    if config.get("usePrivateKey") is False:
        _set_smart_card_reader_address()


def _set_smart_card_reader_address() -> None:
    address = find_smart_card_reader_address()
    os.environ["REXSIO_SMART_CARD_READER_ADDRESS"] = address
    logger.info(f"Smart card reader address added: {address}")
