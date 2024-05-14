from pathlib import Path

# URLs
FRAMEXML_URL = "https://www.townlong-yak.com/framexml"

# Paths
ROOT_PATH = Path.cwd()
CACHE_PATH = ROOT_PATH / "Cache"
SOURCE_PATH = ROOT_PATH / "Source"

VERSION_PATH = SOURCE_PATH / "version.txt"

FRAMEXML_PATH = SOURCE_PATH / "FrameXML"
FRAMEXML_METADATA_PATH = SOURCE_PATH / "metadata.json"
FRAMEXML_DOCUMENTATION_PATH = SOURCE_PATH / "documentation.json"
