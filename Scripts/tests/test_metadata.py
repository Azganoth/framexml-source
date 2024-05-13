from Scripts.metadata import parse_framexml_metadata

# Data sample
html_content = """<table id='filelist'>
    <tbody class='folder'>
        <tr>
            <td>
                <span>Blizzard_AzeriteEssenceUI</span>
            </td>
            <td>10.1.0.49426</td>
            <td></td>
        </tr>
        <tr>
            <td>
                <a>Blizzard_AzeriteEssenceUI.lua</a>
            </td>
            <td>10.1.0.49426</td>
            <td>
                <a>Compare</a>
            </td>
        </tr>
        <tr>
            <td>
                <a>Blizzard_AzeriteEssenceUI.toc</a>
            </td>
            <td>8.2.0.30920</td>
            <td></td>
        </tr>
        <tr>
            <td>
                <a>Blizzard_AzeriteEssenceUI.xml</a>
            </td>
            <td>10.1.0.49426</td>
            <td>
                <a>Compare</a>
            </td>
        </tr>
    </tbody>
    <tbody class='folder'>
        <tr>
            <td>
                <span>Helix</span>
            </td>
            <td>10.2.6.53840</td>
            <td></td>
        </tr>
        <tr>
            <td>
                <a>ArtTextureID.lua</a>
            </td>
            <td>10.2.6.53840</td>
            <td>
                <a>Compare</a>
            </td>
        </tr>
        <tr>
            <td>
                <a>AtlasInfo.lua</a>
            </td>
            <td>10.2.6.53840</td>
            <td>
                <a>Compare</a>
            </td>
        </tr>
        <tr>
            <td>
                <a>GlobalColors.lua</a>
            </td>
            <td>10.2.6.53840</td>
            <td>
                <a>Compare</a>
            </td>
        </tr>
    </tbody>
    <tbody class='root'>
        <tr>
            <td>
                <a>AutoComplete.lua</a>
            </td>
            <td>10.2.6.53840</td>
            <td>
                <a>Compare</a>
            </td>
        </tr>
        <tr>
            <td>
                <a>Localization.lua</a>
                <span>
                    (<a><span>BR</span></a>, <a><span>CN</span></a>, <a><span>DE</span></a>, <a><span>ES</span></a>, <a><span>FR</span></a>, <a><span>IT</span></a>, <a><span>KR</span></a>, <a><span>MX</span></a>, <a><span>PT</span></a>, <a><span>RU</span></a>, <a><span>TW</span></a>, <a><span>US</span></a>)
                </span>
            </td>
            <td>6.1.0.19702</td>
            <td>
                <a>Compare</a>
            </td>
        </tr>
        <tr>
            <td>
                <a>ProjectConstants.lua</a>
            </td>
            <td>10.2.6.53840</td>
            <td></td>
        </tr>
    </tbody>
</table>
"""


def test_parse_framexml_metadata():
    """
    Test parsing of the FrameXML metadata from a HTML.
    """
    metadata = parse_framexml_metadata(html_content)

    expected_metadata = {
        "Blizzard_AzeriteEssenceUI/Blizzard_AzeriteEssenceUI.lua": "10.1.0.49426",
        "Blizzard_AzeriteEssenceUI/Blizzard_AzeriteEssenceUI.toc": "8.2.0.30920",
        "Blizzard_AzeriteEssenceUI/Blizzard_AzeriteEssenceUI.xml": "10.1.0.49426",
        "Helix/ArtTextureID.lua": "10.2.6.53840",
        "Helix/AtlasInfo.lua": "10.2.6.53840",
        "Helix/GlobalColors.lua": "10.2.6.53840",
        "AutoComplete.lua": "10.2.6.53840",
        "Localization.lua": "6.1.0.19702",
        "ProjectConstants.lua": "10.2.6.53840",
    }

    assert metadata == expected_metadata
