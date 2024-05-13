import re
from typing import Optional

import requests
from lxml import html

from Scripts.constants import FRAMEXML_URL, VERSION_PATH


class InvalidVersionError(Exception):
    """Raised when a version string is invalid."""


class VersionFileNotFoundError(FileNotFoundError):
    """Raised when the local version file is not found."""


VERSION_PATTERN = re.compile(r"\d+")


def fetch_latest_version(*, session: Optional[requests.Session] = None) -> int:
    """
    Fetches the latest World of Warcraft build version.

    Args:
        A requests session to use for the HTTP request.
            If None, a new session will be created. Defaults to None.

    Returns:
        The latest World of Warcraft build version.

    Raises:
        InvalidVersionError: If the fetched version string is invalid.
    """
    session = session or requests.Session()

    index_response = session.get(f"{FRAMEXML_URL}/live")
    index_response.raise_for_status()

    index_tree = html.fromstring(index_response.text)
    version_data = index_tree.xpath('string(//meta[@itemprop="build-tags"]/@content)')

    version, _, _ = version_data.partition(";")
    if VERSION_PATTERN.fullmatch(version):
        return int(version)

    raise InvalidVersionError()


def write_local_version(version: int) -> None:
    """
    Stores the specified World of Warcraft build version in the version file.

    Args:
        version: The World of Warcraft build version to store.

    Raises:
        InvalidVersionError: If the provided version string is invalid.
    """
    VERSION_PATH.parent.mkdir(parents=True, exist_ok=True)

    version_str = str(version)
    if not VERSION_PATTERN.fullmatch(version_str):
        raise InvalidVersionError()

    VERSION_PATH.write_text(version_str)


def read_local_version() -> int:
    """
    Retrives the local World of Warcraft build version from the version file.

    Returns:
        The local World of Warcraft build version string.

    Raises:
        VersionFileNotFoundError: If the version file is not found.
        InvalidVersionError: If the local version string is invalid.
    """
    try:
        version = VERSION_PATH.read_text()
    except FileNotFoundError:
        raise VersionFileNotFoundError()

    if VERSION_PATTERN.fullmatch(version):
        return int(version)

    raise InvalidVersionError()


if __name__ == "__main__":
    latest_version = fetch_latest_version()
    current_version = read_local_version()

    if latest_version != current_version:
        print(
            f"Latest: {latest_version}, "
            f"Current: {current_version}; (Update available)"
        )
    else:
        print(f"Build: {current_version}; (Up to date)")
