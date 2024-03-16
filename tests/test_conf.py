""" Test the conf module """
from typing import Any, Generator
import os
import pytest
from pytest_mock import MockerFixture
from senior_swe_ai.conf import (
    get_config_path,
    config_init
)


class TestConf:
    """Testing config functions"""
    @pytest.fixture(autouse=True)
    def setup_class(self) -> Generator[None, Any, None]:
        """Setup the class"""
        os.makedirs(os.path.dirname(get_config_path()), exist_ok=True)
        with open(get_config_path(), 'w', encoding='utf-8') as f:
            f.write('api_key="test_key"')
        yield
        if os.path.exists(get_config_path()):
            os.remove(get_config_path())

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

    def test_config_init_exists(self, mocker: Generator[MockerFixture, None, None]) -> None:
        """Test config_init exists"""
        mocker.patch('os.path.exists', return_value=True)
        mocker.patch('senior_swe_ai.conf.prompt',
                     return_value={'overwrite': False})
        config_init()
        assert os.path.exists(get_config_path()) is True

    def test_config_init_overwrite(self, mocker: Generator[MockerFixture, None, None]) -> None:
        """Test config_init overwrite"""
        mocker.patch('os.path.exists', return_value=True)
        mocker.patch('senior_swe_ai.conf.prompt',
                     return_value={'overwrite': True})
        config_init()
        assert os.path.exists(get_config_path()) is True

    def test_config_init_env_var_not_exists(
        self, mocker: Generator[MockerFixture, None, None]
    ) -> None:
        """Test config_init env var not exists"""
        mocker.patch('os.path.exists', return_value=False)
        mocker.patch.dict('os.environ', {}, clear=True)
        mock_getpass = mocker.patch('getpass.getpass', return_value='test_key')
        mock_api_validate = mocker.patch(
            'senior_swe_ai.conf.validate_api_key', return_value=True)

        config_init()
        mock_getpass.assert_called()
        mock_api_validate.assert_called()
