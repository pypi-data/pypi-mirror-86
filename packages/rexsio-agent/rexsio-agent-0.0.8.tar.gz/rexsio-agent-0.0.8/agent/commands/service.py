from typing import NamedTuple, Any, Dict


class Service(NamedTuple):
    type: str
    id: str
    config: Dict[str, Any]
    compose_url: str
    version: str
