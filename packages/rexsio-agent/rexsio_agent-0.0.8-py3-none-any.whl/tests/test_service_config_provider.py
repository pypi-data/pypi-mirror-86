import unittest
from pathlib import Path
from unittest import mock
from unittest.mock import mock_open, call

from agent.commands.service_config_provider import provide_service_config

BASE_PATH = "/test/path/1234"
CONFIG_PATH = f"{BASE_PATH}/config"
JSON_PATH = f"{CONFIG_PATH}/config.json"
OPEN_CALLS = [
    call(f"{JSON_PATH}", "w"),
    call().__enter__(),
    call().__exit__(None, None, None),
]
CONFIG = {
    "properties": {
        "usePrivateKey": True,
        "network": {
            "address": "address",
            "endpoint": "endpoint",
            "networkType": "networkType",
        },
    },
    "encryptedProperties": {"secret": "secret"},
    "serviceId": "serviceId",
}
EXPECTED_CONFIG_CONTENT = {
    "usePrivateKey": True,
    "network": {
        "address": "address",
        "endpoint": "endpoint",
        "networkType": "networkType",
    },
    "serviceId": "serviceId",
    "rabbitmqPass": "pass",
    "secret": "secret",
    "attention": "FILE GENERATED AUTOMATICALLY. DO NOT EDIT",
}


class TestSaveConfig(unittest.TestCase):
    @mock.patch("agent.commands.service_config_provider.RABBITMQ_PASS", "pass")
    @mock.patch("agent.commands.service_config_provider.decrypt_properties")
    @mock.patch("agent.commands.service_config_provider.get_base_service_path")
    @mock.patch("agent.commands.logger.info")
    @mock.patch("json.dump")
    @mock.patch("builtins.open", new_callable=mock_open)
    @mock.patch("os.path")
    def test_save_config__when_config_dir_exists(
        self,
        mock_dir,
        mock_config_file,
        mock_json,
        mock_logger,
        mock_get_base_service_path,
        mock_decrypt_properties,
    ):
        # given
        mock_get_base_service_path.return_value = BASE_PATH
        mock_dir.isdir.return_value = True
        mock_decrypt_properties.return_value = {"secret": "secret"}

        # when
        provide_service_config(config=CONFIG.copy(), service_id="id")

        # then
        mock_config_file.assert_has_calls(calls=OPEN_CALLS, any_order=False)
        mock_json.assert_called_once_with(
            EXPECTED_CONFIG_CONTENT,
            mock_config_file.return_value.__enter__.return_value,
        )
        mock_logger.assert_called_once_with(f"Config updated: {JSON_PATH}")

    @mock.patch("agent.commands.service_config_provider.RABBITMQ_PASS", "pass")
    @mock.patch("agent.commands.service_config_provider.decrypt_properties")
    @mock.patch("agent.commands.service_config_provider.get_base_service_path")
    @mock.patch("agent.commands.logger.info")
    @mock.patch("json.dump")
    @mock.patch("builtins.open", new_callable=mock_open)
    @mock.patch("os.path")
    @mock.patch("agent.commands.service_config_provider.Path.mkdir", autospec=True)
    def test_save_config__when_config_dir_does_not_exist(
        self,
        mock_path,
        mock_dir,
        mock_config_file,
        mock_json,
        mock_logger,
        mock_get_base_service_path,
        mock_decrypt_properties,
    ):
        # given
        mock_get_base_service_path.return_value = BASE_PATH
        mock_dir.isdir.return_value = False
        mock_decrypt_properties.return_value = {"secret": "secret"}

        # when
        provide_service_config(config=CONFIG.copy(), service_id="id")

        # then
        mock_path.assert_called_once_with(
            Path(f"{CONFIG_PATH}"), exist_ok=True, parents=True
        )

        mock_config_file.assert_has_calls(calls=OPEN_CALLS, any_order=False)
        mock_json.assert_called_once_with(
            EXPECTED_CONFIG_CONTENT,
            mock_config_file.return_value.__enter__.return_value,
        )
        logger_calls = [
            call(f"Directory {CONFIG_PATH} does not exist, creating one"),
            call(f"Config updated: {JSON_PATH}"),
        ]
        mock_logger.assert_has_calls(calls=logger_calls, any_order=False)
