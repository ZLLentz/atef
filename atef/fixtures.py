import pytest

from .commands import assert_cache


@pytest.fixture(scope='function')
def assert_fixture():
    assert_cache.clear()
    yield
    for result, error_message in assert_cache:
        assert result, error_message
    assert_cache.clear()
