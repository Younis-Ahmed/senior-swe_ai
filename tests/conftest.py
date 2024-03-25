"""This module contains the fixtures for the tests."""
from typing import Any, Generator
import os
import pytest
from pytest_mock import MockerFixture
from senior_swe_ai.conf import get_config_path


@pytest.fixture
def setup_class(
    mocker: Generator[MockerFixture, None, None]
) -> Generator[None, Any, None]:
    """Setup the class"""
    try:
        os.makedirs(os.path.dirname(get_config_path()), exist_ok=True)
        with open(get_config_path(), 'w', encoding='utf-8') as f:
            f.write('api_key="test_key"')
        mocker.patch('os.environ', return_value='test_key')
        yield
    finally:
        if os.path.exists(get_config_path()):
            os.remove(get_config_path())
