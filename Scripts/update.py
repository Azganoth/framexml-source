import json
import zipfile
from typing import Optional

import requests

from Scripts.check import fetch_latest_version, write_local_version
from Scripts.constants import (
    CACHE_PATH,
    FILE_VERSIONS_PATH,
    FRAMEXML_PATH,
    FRAMEXML_URL,
)
from Scripts.file_versions import parse_file_versions
from Scripts.helpers import cache_if_missing


def update_framexml_files(
    version: str, *, session: Optional[requests.Session] = None
) -> None:
    """
    Update the FrameXML files to the specified version.

    Downloads and extracts the FrameXML files from the specified version.
    The FrameXML files are stored in a ZIP file and extracted to the FRAMEXML_PATH directory.

    Args:
        version: The version of the FrameXML files to update to.
        session: An optional requests session to use for the HTTP request.
            If None, a new session will be created. Defaults to None.
    """
    framexml_zip_path = CACHE_PATH / f"{version}.zip"
    cache_if_missing(
        framexml_zip_path, f"{FRAMEXML_URL}/{version}/get", session=session
    )

    FRAMEXML_PATH.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(framexml_zip_path, "r") as framexml_zip:
        framexml_zip.extractall(FRAMEXML_PATH)


def update_file_versions(
    version: str, *, session: Optional[requests.Session] = None
) -> None:
    """
    Update the version control file of the specified World of Warcraft version source files.

    Downloads the HTML file containing file versions from the specified World of Warcraft version.
    Parses the HTML content to extract file names and its api versions.
    Stores the file versions in a JSON file.

    Args:
        version: The version of the file versions to update to.
        session: An optional requests session to use for the HTTP request.
            If None, a new session will be created. Defaults to None.
    """
    file_versions_html_path = CACHE_PATH / f"{version}.html"
    cache_if_missing(
        file_versions_html_path, f"{FRAMEXML_URL}/{version}", session=session
    )

    file_versions = parse_file_versions(file_versions_html_path.read_text())

    FILE_VERSIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with FILE_VERSIONS_PATH.open("w") as file_versions_file:
        json.dump(file_versions, file_versions_file)


if __name__ == "__main__":
    session = requests.session()

    latest_version = fetch_latest_version(session=session)

    update_framexml_files(latest_version)
    update_file_versions(latest_version)
    write_local_version(latest_version)
