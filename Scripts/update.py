import requests

from Scripts.check import fetch_latest_version, write_local_version
from Scripts.sync import sync_file_versions, sync_framexml_files

if __name__ == "__main__":
    session = requests.session()

    latest_version = fetch_latest_version(session=session)

    sync_framexml_files(latest_version)
    sync_file_versions(latest_version)
    write_local_version(latest_version)
