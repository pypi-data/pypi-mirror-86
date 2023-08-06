import os
from unittest import mock
from unittest.case import TestCase

from agent.smart_card.smart_card_resolver import resolve_smart_card_reader_env


class TestSmartCardResolver(TestCase):
    @mock.patch("agent.smart_card.smart_card_resolver.find_smart_card_reader_address")
    @mock.patch("agent.smart_card.logger.info")
    @mock.patch.dict("os.environ", {})
    def test_resolve_smart_card_reader_address__when_private_key_flag_not_in_config(
        self, mock_logger, mock_reader
    ):
        # given
        config = dict(usePrivateKey=False)
        reader_address = "/dev/usb/reader/address"
        mock_reader.return_value = reader_address
        # when
        resolve_smart_card_reader_env(config)
        # then
        mock_logger.assert_called_once_with(
            f"Smart card reader address added: {reader_address}"
        )
        self.assertIn("REXSIO_SMART_CARD_READER_ADDRESS", os.environ)

    @mock.patch("agent.smart_card.smart_card_resolver.find_smart_card_reader_address")
    @mock.patch("agent.smart_card.logger.info")
    @mock.patch.dict("os.environ", {})
    def test_resolve_smart_card_reader_address__when_private_key_flag_in_config(
        self, mock_logger, mock_reader
    ):
        # given
        config = dict()
        # when
        resolve_smart_card_reader_env(config)
        # then
        mock_logger.assert_not_called()
        mock_reader.assert_not_called()
        self.assertNotIn("REXSIO_SMART_CARD_READER_ADDRESS", os.environ)
