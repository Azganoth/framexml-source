from pathlib import Path

import pytest

from Scripts.check import (
    InvalidVersionError,
    VersionControlNotFoundError,
    fetch_latest_version,
    read_local_version,
)

# Example test data
SAMPLE_VERSION = "54205"


@pytest.fixture
def version_control_path(mocker, tmp_path) -> Path:
    """Fixture to create a temporary version control file path."""
    file_path = tmp_path / "version.txt"
    mocker.patch("Scripts.check.VERSION_CONTROL_PATH", file_path)
    return file_path


def test_fetch_latest_version_with_valid_response(mocker):
    """Test fetching the latest version with a valid response from the server."""
    # Mocking requests.Session().get() to return a valid response
    mock_session = mocker.Mock()
    mock_session.get.return_value.text = (
        f'<meta itemprop="build-tags" content="{SAMPLE_VERSION}">'
    )

    assert fetch_latest_version(session=mock_session) == SAMPLE_VERSION


def test_fetch_latest_version_with_invalid_response(mocker):
    """Test fetching the latest version with an invalid response from the server."""
    # Mocking requests.Session().get() to return a invalid response
    mock_session = mocker.Mock()
    mock_session.get.return_value.text = '<title title="43121">'

    with pytest.raises(InvalidVersionError):
        fetch_latest_version(session=mock_session)


def test_read_local_version_with_missing_file(version_control_path):
    """Test reading the local version when the version control file is missing."""

    with pytest.raises(VersionControlNotFoundError):
        read_local_version()


def test_read_local_version_with_valid_file(version_control_path):
    """Test reading the local version from a version control file with a valid version string."""

    version_control_path.write_text(SAMPLE_VERSION)

    assert read_local_version() == SAMPLE_VERSION


def test_read_local_version_with_invalid_version(version_control_path):
    """Test reading the local version from a version control file with an invalid version string."""

    version_control_path.write_text("10.2.7")

    with pytest.raises(InvalidVersionError):
        read_local_version()
