from datetime import datetime

from app.domain.category import Category

from app.services.discovery.hcp_listing_parser import HCPListingParser


FIXTURE_HTML = """
<html><body>
<div class="cel1">
  <div class="classeur">Tags (2) : Emploi</div>

  <div class="delimiter">
    <div class="photo">
      <a href="/file/1/"><img src="/_images/download_defaut.png"></a>
    </div>
    <div>
      <div class="titre_fichier">
        <a href="/file/1/">Enquête nationale sur l'emploi 2025</a>
      </div>
      <div class="information">
        <a href="/file/1/"><img class="image" src="/_images/ext/icon_pdf.gif"></a>
        Publié le : 04/08/2026
      </div>
      <div class="information">
        <span>Tags :</span>
        <a class="lien" href="/downloads/?tag=Emploi">Emploi</a>
      </div>
    </div>
  </div>

  <div class="delimiter">
    <div class="photo">
      <a href="/file/2/"><img src="/photo/thumb/2.png"></a>
    </div>
    <div>
      <div class="titre_fichier">
        <a href="/file/2/">Annuaire statistique régional</a>
      </div>
      <div class="information">
        <a href="/file/2/"><img class="image" src="/_images/ext/icon_xlsx.gif"></a>
        Publié le : 12/01/2025
      </div>
      <div class="information">
        <span>Tags :</span>
        <a class="lien" href="/downloads/?tag=Emploi">Emploi</a>
      </div>
    </div>
  </div>
</div>
</body></html>
"""

PAGE_URL = "https://www.hcp.ma/downloads/?tag=Emploi"


def test_parse_extracts_every_publication():

    parser = HCPListingParser()

    result = parser.parse(FIXTURE_HTML, PAGE_URL, "hcp", "Emploi")

    assert len(result.publications) == 2

    first = result.publications.all()[0]

    assert first.title == "Enquête nationale sur l'emploi 2025"
    assert first.url == "https://www.hcp.ma/file/1/"
    assert first.publication_date == datetime(2026, 8, 4)
    assert first.source_id == "hcp"
    assert first.category == Category.EMPLOYMENT


def test_parse_counts_formats_from_the_download_icon():

    parser = HCPListingParser()

    result = parser.parse(FIXTURE_HTML, PAGE_URL, "hcp", "Emploi")

    assert result.format_counts["pdf_count"] == 1
    assert result.format_counts["excel_count"] == 1


def test_parse_filters_out_publications_with_disallowed_formats():

    parser = HCPListingParser()

    result = parser.parse(
        FIXTURE_HTML,
        PAGE_URL,
        "hcp",
        "Emploi",
        allowed_formats=["xlsx"]
    )

    assert len(result.publications) == 1
    assert result.publications.all()[0].title == "Annuaire statistique régional"


def test_parse_defaults_unmapped_categories_to_other():

    parser = HCPListingParser()

    result = parser.parse(
        FIXTURE_HTML,
        PAGE_URL,
        "hcp",
        "Comptes nationaux"
    )

    assert all(
        publication.category == Category.OTHER
        for publication in result.publications
    )
