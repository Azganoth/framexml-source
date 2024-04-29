import re
from typing import Optional

import requests
from lxml import html

from Scripts.constants import FRAMEXML_URL, VERSION_CONTROL_PATH


class InvalidVersionError(Exception):
    """Raised when a version string is invalid."""


class VersionControlNotFoundError(FileNotFoundError):
    """Raised when the version control file is not found."""


VERSION_PATTERN = re.compile(r"\d+")


def fetch_latest_version(*, session: Optional[requests.Session] = None) -> str:
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
        return version

    raise InvalidVersionError()


def write_local_version(version: str) -> None:
    """
    Writes the specified World of Warcraft build version to the version control file.

    Args:
        build_version: The World of Warcraft build version to write.

    Raises:
        InvalidVersionError: If the provided version string is invalid.
    """
    VERSION_CONTROL_PATH.parent.mkdir(parents=True, exist_ok=True)

    if not VERSION_PATTERN.fullmatch(version):
        raise InvalidVersionError()

    VERSION_CONTROL_PATH.write_text(version)


def read_local_version() -> str:
    """
    Reads the local World of Warcraft build version from the version control file.

    Returns:
        The local World of Warcraft build version string.

    Raises:
        VersionControlNotFoundError: If the version control file is not found.
        InvalidVersionError: If the local version string is invalid.
    """
    try:
        build_version = VERSION_CONTROL_PATH.read_text()
    except FileNotFoundError:
        raise VersionControlNotFoundError()

    if VERSION_PATTERN.fullmatch(build_version):
        return build_version

    raise InvalidVersionError()


if __name__ == "__main__":
    latest_version = fetch_latest_version()
    current_version = read_local_version()

    if latest_version != current_version:
        print(
            f"Latest: {latest_version}, Current: {current_version}; (Update available)"
        )
    else:
        print(f"Build: {current_version}; (Up to date)")
