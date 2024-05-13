import re
from typing import TypeAlias

from lxml import html


class HTMLError(Exception):
    """
    Raised for errors related to HTML processing.
    """


API_VERSION_PATTERN = re.compile(r"\d+\.\d+\.\d+\.\d+")


def _parse_table_row(row: html.HtmlElement) -> tuple[str, str]:
    """
    Parses a single HTML table row to extract file information.

    Args:
        row: The HTML element representing a table row.

    Returns:
        A tuple containing the file name and its World of Warcraft version.

    Raises:
        HTMLError: If there are parsing errors in the table row.
    """
    data_cells = row.xpath(".//td")
    if len(data_cells) < 2:
        raise HTMLError("Insufficient data in table row.")

    name, version = [td.text_content().strip() for td in data_cells[:2]]
    if not name:
        raise HTMLError("Entry name missing from table row.")

    # Remove any localization information, e.g. 'Localization.lua (CN,KR,RU)' -> 'Localization.lua'.
    localization_start_index = name.find("(")
    if localization_start_index != -1:
        name = name[:localization_start_index].strip()

    if not API_VERSION_PATTERN.fullmatch(version):
        raise HTMLError(
            "Version missing or invalid in table row. "
            f"Filename: {name}, Version: {version}"
        )

    return name, version


FrameXMLMetadata: TypeAlias = dict[str, str]


def parse_framexml_metadata(html_content: str) -> FrameXMLMetadata:
    """
    Parses HTML content to extract file names and their corresponding versions.

    Args:
        html_content: The HTML content to parse.

    Returns:
        A dictionary mapping file names to their corresponding versions.

    Raises:
        HTMLError: If there are errors in parsing the HTML content.
    """
    document_tree = html.fromstring(html_content)

    try:
        entry_table = document_tree.xpath('//*[@id="filelist"]')[0]
    except IndexError:
        raise HTMLError("'#filelist' missing in the provided HTML content.")

    metadata: FrameXMLMetadata = {}

    for dir_table in entry_table.xpath('.//tbody[contains(@class, "folder")]'):
        dir_row, *file_rows = dir_table.xpath(".//tr")

        # Prepend the directory name for each filename.
        dir_name, _ = _parse_table_row(dir_row)
        dir_path = dir_name
        for file_row in file_rows:
            filename, version = _parse_table_row(file_row)
            metadata[f"{dir_path}/{filename}"] = version

    for file_row in entry_table.xpath('.//tbody[contains(@class, "root")]/tr'):
        filename, version = _parse_table_row(file_row)
        metadata[filename] = version

    return metadata
