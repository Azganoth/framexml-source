from pathlib import Path

# Paths
ROOT_PATH = Path.cwd()
CACHE_PATH = ROOT_PATH / "Cache"
SOURCE_PATH = ROOT_PATH / "Source"

FRAMEXML_URL = "https://www.townlong-yak.com/framexml"
FRAMEXML_PATH = SOURCE_PATH / "FrameXML"

VERSION_CONTROL_PATH = SOURCE_PATH / "build.txt"
FILE_VERSIONS_PATH = SOURCE_PATH / "file_versions.json"
