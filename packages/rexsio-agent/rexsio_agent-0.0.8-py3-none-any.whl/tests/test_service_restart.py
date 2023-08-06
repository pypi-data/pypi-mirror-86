from unittest import mock, TestCase
from unittest.mock import call, Mock

from agent.commands.service_restart import restart_services, restart_service
from agent.exceptions.agent_error import AgentError


class TestServiceRestart(TestCase):
    @mock.patch(
        "agent.commands.service_restart.get_docker_compose_path",
        return_value="/test/path/1234",
    )
    @mock.patch("agent.commands.service_restart.docker_compose_restart")
    def test_check_service_restart__when_no_service_is_down(
        self, mock_docker_compose_restart, mock_get_docker_compose_path
    ):
        service_id_list = []

        restart_services(service_id_list)

        mock_docker_compose_restart.assert_not_called()

    @mock.patch("agent.commands.service_restart.send_status", Mock())
    @mock.patch(
        "agent.commands.service_restart.get_docker_compose_path",
        return_value="/test/path/docker-compose.yaml",
    )
    @mock.patch("agent.commands.service_restart.docker_compose_restart")
    def test_check_service_restart__when_one_service_is_down(
        self, mock_docker_compose_restart, mock_get_docker_compose_path
    ):
        service_id_list = ["uuid1"]

        restart_services(service_id_list)

        mock_docker_compose_restart.assert_called_once_with(
            "/test/path/docker-compose.yaml"
        )

    @mock.patch("agent.commands.service_restart.send_status", Mock())
    @mock.patch(
        "agent.commands.service_restart.get_docker_compose_path",
        side_effect=[
            "/test/path1/docker-compose.yaml",
            "/test/path2/docker-compose.yaml",
        ],
    )
    @mock.patch("agent.commands.service_restart.docker_compose_restart")
    def test_check_service_restart__when_three_services_are_down(
        self, mock_docker_compose_restart, mock_get_docker_compose_path
    ):
        service_id_list = ["uuid1", "uuid2"]
        calls = [
            call("/test/path1/docker-compose.yaml"),
            call("/test/path2/docker-compose.yaml"),
        ]

        restart_services(service_id_list)

        mock_docker_compose_restart.assert_has_calls(calls=calls, any_order=False)

    @mock.patch(
        "agent.commands.service_restart.get_docker_compose_path",
        return_value="/test/path/1234",
    )
    @mock.patch("agent.commands.service_restart.send_status")
    @mock.patch("agent.commands.service_restart.docker_compose_restart")
    @mock.patch("agent.commands.service_restart.provide_service_config")
    def test_check_service_restart_command(
        self,
        mock_save_config,
        mock_docker_compose_restart,
        mock_send_status,
        mock_get_docker_compose_path,
    ):
        # given
        config = {"key1": "value1", "key2": "value2"}
        body = {
            "nodeServiceId": "testId",
            "config": config,
        }
        calls = [call("testId", "RESTARTING"), call("testId", "UP")]

        # when
        restart_service(body)

        # then
        mock_docker_compose_restart.assert_called_with("/test/path/1234")
        mock_save_config.assert_called_once_with(config=config, service_id="testId")
        mock_send_status.assert_has_calls(calls=calls, any_order=False)

    @mock.patch(
        "agent.commands.service_restart.get_docker_compose_path",
        return_value="/test/path/1234",
    )
    @mock.patch("agent.commands.service_restart.send_status")
    @mock.patch("agent.commands.service_restart.docker_compose_restart")
    @mock.patch("agent.commands.service_restart.provide_service_config")
    def test_check_service_restart__when_no_service_id(
        self,
        mock_save_config,
        mock_docker_compose_restart,
        mock_send_status,
        mock_get_docker_compose_path,
    ):
        # given
        body = {"config": {"key1": "value1", "key2": "value2"}}

        # when
        with self.assertRaises(AgentError) as e:
            restart_service(body=body)

        # then
        mock_save_config.assert_not_called()
        mock_docker_compose_restart.assert_not_called()
        mock_send_status.assert_not_called()

    @mock.patch(
        "agent.commands.service_restart.get_docker_compose_path",
        return_value="/test/path/1234",
    )
    @mock.patch("agent.commands.service_restart.send_status")
    @mock.patch("agent.commands.service_restart.docker_compose_restart")
    @mock.patch("agent.commands.service_restart.provide_service_config")
    def test_check_service_restart__when_no_config(
        self,
        mock_save_config,
        mock_docker_compose_restart,
        mock_send_status,
        mock_get_docker_compose_path,
    ):
        # given
        body = {"nodeServiceId": "id"}

        # when
        with self.assertRaises(AgentError) as e:
            restart_service(body=body)

        # then
        mock_save_config.assert_not_called()
        mock_docker_compose_restart.assert_not_called()
        mock_send_status.assert_not_called()
