""" Test the conf module """
from typing import Generator
import os
from unittest.mock import AsyncMock, MagicMock, NonCallableMagicMock
import openai
import pytest
from pytest_mock import MockerFixture
from senior_swe_ai.conf import (
    get_config_path,
    config_init,
    validate_api_key,
    save_conf,
    append_conf
)


class TestConf:
    """Testing config functions"""

    def test_get_config_path_unix(self) -> None:
        """Test get_config_path unix"""
        assert get_config_path() == os.path.join(
            os.path.expanduser('~/.config/senior_swe_ai'), 'conf.toml')

    def test_get_config_path_windows(self, mocker: Generator[MockerFixture, None, None]) -> None:
        """Test get_config_path windows"""
        mocker.patch('platform.system', return_value='Windows')
        assert get_config_path() == os.path.join(os.path.expanduser(
            '~/AppData/Roaming/senior_swe_ai'), 'conf.toml')

    def test_get_config_path_unsupport(self, mocker: Generator[MockerFixture, None, None]) -> None:
        """Test get_config_path unsupported"""
        mocker.patch('platform.system', return_value='Unsupported')
        with pytest.raises(NotImplementedError):
            get_config_path()

    def test_config_init_exists(self, mocker: Generator[MockerFixture, None, None],
                                setup_class) -> None:
        """Test config_init exists"""
        mocker.patch('os.path.exists', return_value=True)
        mocker.patch('senior_swe_ai.conf.prompt',
                     return_value={'overwrite': False})
        config_init()
        assert os.path.exists(get_config_path()) is True

    def test_validate_api_key_error(self, mocker: MockerFixture) -> None:
        """Test validate_api_key with an unexpected error"""
        mocker.patch('openai.OpenAI', side_effect=openai.OpenAIError)
        api_key = "error_api_key"

        assert validate_api_key(api_key) is False

    def test_validate_api_key_success(self, mocker: MockerFixture) -> None:
        """Test validate_api_key with a successful key"""
        mocker.patch('openai.OpenAI', return_value=AsyncMock())
        api_key = "success_api_key"
        assert validate_api_key(api_key) is True

    def test_save_conf(self, mocker: MockerFixture) -> None:
        """Test save_conf function"""
        mock_open: MagicMock | AsyncMock | NonCallableMagicMock = mocker.patch(
            "builtins.open", mocker.mock_open())
        mock_dump: MagicMock | AsyncMock | NonCallableMagicMock = mocker.patch(
            "toml.dump")

        conf: dict[str, str] = {"api_key": "test_key"}
        save_conf(conf)

        mock_open.assert_called_once_with(
            get_config_path(), 'w', encoding='utf-8')

        mock_dump.assert_called_once_with(
            conf, mock_open.return_value.__enter__.return_value)

    def test_append_conf(self, mocker: MockerFixture) -> None:
        """Test append_conf function"""
        mock_open: MagicMock | AsyncMock | NonCallableMagicMock = mocker.patch(
            "builtins.open", mocker.mock_open())
        mock_load: MagicMock | AsyncMock | NonCallableMagicMock = mocker.patch(
            "senior_swe_ai.conf.load_conf", return_value={"existing_key": "existing_value"})
        mock_dump: MagicMock | AsyncMock | NonCallableMagicMock = mocker.patch(
            "toml.dump")

        conf: dict[str, str] = {"new_key": "new_value"}
        append_conf(conf)

        mock_open.assert_called_once_with(
            get_config_path(), 'w', encoding='utf-8')

        mock_load.assert_called_once()

        mock_dump.assert_called_once_with(
            {
                "existing_key": "existing_value",
                "new_key": "new_value"
            }, mock_open.return_value.__enter__.return_value)
