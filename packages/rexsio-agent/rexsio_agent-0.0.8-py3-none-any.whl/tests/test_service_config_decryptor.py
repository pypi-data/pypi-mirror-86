import os
import unittest
from unittest import mock

from agent.commands.service_config_decryptor import AgentCipher, decrypt_properties

TEST_DIR = os.path.dirname(os.path.abspath(__file__))

PROPERTIES = {
    "secret": "nYcsswJkSrnW0GhYXJHPQByYkEN75qh6edoVu3asjr7P05xiPRSNsbJJ5PlsVmZEgnNEUOMxGZ3inzYBJFlhrZyG/g/Po84s+7HrRjPkPkHJLEvdDiz0B9lK/paCkEUQRMe4Nrwcte/nZnopsQVi3N+NoQkgXvUPfP2OciQKmuw="
}


class TestPropertiesDecryptor(unittest.TestCase):
    def test_cipher(self):
        # given
        cipher = AgentCipher(f"{TEST_DIR}/resources")

        # when
        result = cipher.decrypt_base64_value(PROPERTIES["secret"])

        # then
        self.assertEqual(result, "secret")

    @mock.patch("agent.commands.service_config_decryptor.cipher")
    def test_properties_decryptor(self, cipher_mock):
        # given
        cipher_mock.decrypt_base64_value.return_value = "secret"

        # when
        result = decrypt_properties(PROPERTIES)

        # then
        self.assertDictEqual(result, dict(secret="secret"))
