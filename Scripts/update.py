import requests

from Scripts.check import fetch_latest_version, write_local_version
from Scripts.sync import sync_framexml_files, sync_framexml_metadata

if __name__ == "__main__":
    session = requests.session()

    latest_version = fetch_latest_version(session=session)

    sync_framexml_files(latest_version, session=session)
    sync_framexml_metadata(latest_version, session=session)
    write_local_version(latest_version)
