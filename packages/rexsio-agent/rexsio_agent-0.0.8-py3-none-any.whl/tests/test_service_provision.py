import unittest
from unittest import mock
from unittest.mock import Mock, MagicMock, call

from agent.commands.service import Service
from agent.commands.service_provision import (
    provision_service,
    start_service,
    create_service_queue,
    generate_service_certificate,
)
from agent.rabbitmq.message_types import DeclareQueueMessage

FILENAME = "/test/path/1234/docker-compose.yaml"

get_base_service_path_mock = Mock()
get_base_service_path_mock.return_value = "/test/path/1234"


class TestServiceInstall(unittest.TestCase):
    @mock.patch(
        "agent.commands.utils.get_base_service_path", get_base_service_path_mock
    )
    @mock.patch("agent.commands.service_provision.start_service")
    @mock.patch("agent.commands.logger.info")
    @mock.patch("agent.commands.service_provision.generate_service_certificate")
    @mock.patch("agent.commands.service_provision.provide_service_config")
    def test_secretary_provision_success(
        self, mock_save_config, mock_cert, mock_logger, mock_docker_compose_service,
    ):
        # given
        service_type = "secretary"
        url = "url"
        config = {"key1": "value1", "key2": "value2"}
        service_id = "id"
        version = "v12"
        body = {
            "nodeServiceId": service_id,
            "config": config,
            "dockerComposeUrl": url,
            "serviceType": service_type,
            "version": version,
        }
        service = Service(
            type=service_type,
            id=service_id,
            config=config,
            compose_url=url,
            version=version,
        )

        # when
        provision_service(body)

        # then
        mock_save_config.assert_called_once_with(service_id=service_id, config=config)
        mock_cert.assert_called_once_with(service_id)
        mock_docker_compose_service.assert_called_once_with(service)
        mock_logger.assert_called_once_with("Service secretary/id is running")

    @mock.patch("agent.commands.service_provision.docker_compose_pull")
    @mock.patch("agent.commands.service_provision.docker_compose_up")
    @mock.patch("agent.commands.service_provision._get_docker_compose_file")
    @mock.patch("agent.commands.utils.get_base_service_path")
    def test_start_service(
        self, mock_path, mock_request, mock_docker_compose_up, mock_docker_compose_pull
    ):
        # given
        service = Service(
            type="service_type",
            id="service_id",
            config=dict(key="value"),
            compose_url="url",
            version="version",
        )
        base_path = "base/path"
        mock_path.return_value = base_path
        filename = f"{base_path}/docker-compose.yaml"

        # when
        start_service(service=service)

        # then
        mock_request.assert_called_once_with(url=service.compose_url, filename=filename)
        mock_docker_compose_up.assert_called_once_with(filename)
        mock_docker_compose_pull.assert_called_once_with(filename)

    @mock.patch("agent.commands.service_provision.publisher_queue.put")
    def test_create_service_queue(self, mock_queue):
        # given
        message = DeclareQueueMessage(topic="topic")

        # when
        create_service_queue(topic="topic")

        # then
        mock_queue.assert_called_once_with(message)

    @mock.patch("agent.commands.service_provision.BASE_SERVICES_PATH", "path")
    @mock.patch("agent.commands.service_provision.REXSIO_HOST", "host")
    @mock.patch("agent.commands.service_provision.get_access_token")
    @mock.patch("agent.commands.service_provision.CertificateClient")
    @mock.patch("agent.commands.service_provision.CertificateConfigGenerator")
    def test_generate_service_certificate(
        self, mock_generator, mock_client, mock_token
    ):
        # given
        client = Mock()
        generator = Mock()
        mock_client.return_value = client
        mock_generator.return_value = generator
        mock_token.return_value = "token"

        # when
        generate_service_certificate("service_id")

        # then
        mock_client.assert_called_once_with(
            base_path="https://host", access_token="token"
        )
        mock_generator.assert_called_once_with(cert_client=client, service_configs_path='path')
        generator.generate_cert_config.assert_called_once_with("service_id")
