from unittest import TestCase

from agent.commands.service import Service
from agent.commands.service_creator import create_service


class TestServiceCreator(TestCase):
    def test_create_service(self):
        # given
        body = {
            "nodeServiceId": "service_id",
            "config": {"key1": "value1", "key2": "value2"},
            "dockerComposeUrl": "url",
            "serviceType": "service_type",
            "version": "version",
        }

        # when
        result = create_service(body)

        # then
        self.assertIsInstance(result, Service)
        self.assertEqual(result.version, body["version"])
        self.assertEqual(result.id, body["nodeServiceId"])
        self.assertEqual(result.compose_url, body["dockerComposeUrl"])
        self.assertEqual(result.config, body["config"])
        self.assertEqual(result.type, body["serviceType"])
