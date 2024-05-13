from pathlib import Path

import pytest
import requests

from Scripts.helpers import cache_if_missing

# Data sample
SAMPLE_URL = "https://example.com/sample_file"
SAMPLE_CONTENT = b"Sample content"


@pytest.fixture
def cache_file_path(tmp_path) -> Path:
    """Fixture to create a temporary cache file path."""
    cache_file_path = tmp_path / "cached_file.txt"
    return cache_file_path


def test_cache_if_missing_success(mocker, cache_file_path):
    """Test caching a file when it doesn't exist locally."""
    # Mocking requests.Session().get() to return a valid response
    mock_session = mocker.Mock()
    mock_session.get.return_value.content = SAMPLE_CONTENT

    cache_if_missing(cache_file_path, SAMPLE_URL, session=mock_session)

    assert cache_file_path.exists()
    assert cache_file_path.read_bytes() == SAMPLE_CONTENT


def test_cache_if_missing_file_exists(mocker, cache_file_path):
    """Test caching a file when it already exists locally."""
    cache_file_path.write_bytes(SAMPLE_CONTENT)

    mock_session = mocker.Mock()

    cache_if_missing(cache_file_path, SAMPLE_URL, session=mock_session)

    assert cache_file_path.exists()
    assert cache_file_path.read_bytes() == SAMPLE_CONTENT

    assert not mock_session.get.called


def test_cache_if_missing_http_error(mocker, cache_file_path):
    """Test caching a file when an HTTP error occurs."""
    # Mocking requests.Session().get() to raise an HTTP error
    mock_session = mocker.Mock()
    mock_session.get.side_effect = requests.HTTPError()

    with pytest.raises(requests.HTTPError):
        cache_if_missing(cache_file_path, SAMPLE_URL, session=mock_session)

    assert not cache_file_path.exists()


def test_cache_if_missing_io_error(mocker, cache_file_path):
    """Test caching a file when an I/O error occurs."""
    # Mocking requests.Session().get() to return a valid response
    mock_session = mocker.Mock()
    mock_session.get.return_value.content = SAMPLE_CONTENT

    mocker.patch("Scripts.helpers.Path.write_bytes", side_effect=IOError())

    with pytest.raises(IOError):
        cache_if_missing(cache_file_path, SAMPLE_URL, session=mock_session)

    assert not cache_file_path.exists()
