import base64
import os.path
from typing import Dict

from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

from agent.config.properties import KEYS_DIR


class AgentCipher:
    def __init__(self, keys_dir):
        self.key_path = f"{keys_dir}/private_key.pem"

        if os.path.isfile(self.key_path):
            self.private_key = RSA.import_key(self._load_key())
            self.cipher = PKCS1_v1_5.new(self.private_key)

    def _load_key(self) -> bytes:
        with open(self.key_path, "rb") as f:
            key = f.read()
        return key.strip()

    def decrypt_base64_value(self, value: str) -> str:
        bytes_value = base64.b64decode(value)
        return self.cipher.decrypt(ciphertext=bytes_value, sentinel=None).decode(
            "utf-8"
        )


cipher = AgentCipher(KEYS_DIR)


def decrypt_properties(properties: Dict[str, str]) -> Dict[str, str]:
    return {k: cipher.decrypt_base64_value(v) for k, v in properties.items()}
