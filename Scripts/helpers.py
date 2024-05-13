from pathlib import Path
from typing import Optional

import requests


def cache_if_missing(
    cache_file_path: Path, url: str, *, session: Optional[requests.Session] = None
) -> None:
    """
    Downloads and caches a file from the specified URL if it doesn't exist locally.

    Args:
        cache_file_path: The path to the local cache file.
        url: The URL of the file to download if it's missing.
        session: An optional requests session to use for the HTTP request.
            If None, a new session will be created. Defaults to None.

    Raises:
        requests.HTTPError: If an HTTP error occurs during the download.
        IOError: If an I/O error occurs while writing the file.

    Notes:
        If the parent directory of the cache file does not exist, it will be created.
    """
    cache_file_path.parent.mkdir(parents=True, exist_ok=True)

    if not cache_file_path.exists():
        session = session or requests.Session()

        response = session.get(url)
        response.raise_for_status()

        cache_file_path.write_bytes(response.content)
