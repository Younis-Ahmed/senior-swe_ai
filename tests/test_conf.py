""" Test the conf module """
from typing import Any, Generator
import pytest
from pytest_mock import MockerFixture
from senior_swe_ai.conf import *


class TestConf:
    """Testing config functions"""
    @pytest.fixture(autouse=True)
    def setup_class(self) -> Generator[None, Any, None]:
        """Setup the class"""
        os.makedirs(os.path.dirname(get_config_path()), exist_ok=True)
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
