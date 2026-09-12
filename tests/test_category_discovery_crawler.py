from app.services.discovery.category_discovery_crawler import (
    CategoryDiscoveryCrawler
)


PAGE_1 = """
<html><body>
<div class="delimiter">
  <div class="titre_fichier"><a href="/file/1/">Doc page 1</a></div>
  <div class="information">
    <a href="/file/1/"><img class="image" src="/_images/ext/icon_pdf.gif"></a>
    Publié le : 01/01/2026
  </div>
</div>
<div class="pager">
  <a class="sel" href="/downloads/?tag=Emploi">1</a>
  <a href="/downloads/?tag=Emploi&amp;p=20">»</a>
</div>
</body></html>
"""

PAGE_2 = """
<html><body>
<div class="delimiter">
  <div class="titre_fichier"><a href="/file/2/">Doc page 2</a></div>
  <div class="information">
    <a href="/file/2/"><img class="image" src="/_images/ext/icon_pdf.gif"></a>
    Publié le : 02/01/2026
  </div>
</div>
<div class="pager">
  <a href="/downloads/?tag=Emploi">1</a>
  <a class="sel" href="/downloads/?tag=Emploi&amp;p=20">2</a>
</div>
</body></html>
"""


class FakeResponse:

    def __init__(self, url, text):
        self.url = url
        self.text = text


class FakeHTTPClient:

    def __init__(self, pages):
        self.pages = pages
        self.requested_urls = []

    def get(self, url):
        self.requested_urls.append(url)
        return FakeResponse(url, self.pages[url])


class FakeConnector:

    def get_id(self):
        return "hcp"

    def get_base_url(self):
        return "https://www.hcp.ma"

    def get_categories(self):
        return ["Emploi"]

    def get_allowed_formats(self):
        return ["pdf"]


def test_crawl_follows_pagination_across_a_category():

    pages = {
        "https://www.hcp.ma/downloads/?tag=Emploi": PAGE_1,
        "https://www.hcp.ma/downloads/?tag=Emploi&p=20": PAGE_2,
    }

    http_client = FakeHTTPClient(pages)

    crawler = CategoryDiscoveryCrawler(http_client=http_client)

    result = crawler.crawl(FakeConnector())

    assert result.pages_visited == 2
    assert result.categories_visited == 1

    titles = sorted(
        publication.title for publication in result.publications
    )

    assert titles == ["Doc page 1", "Doc page 2"]
    assert result.format_counts["pdf_count"] == 2


class InfiniteHTTPClient:
    """
    Simule un site dont le lien "suivant" change à chaque appel :
    sans garde-fou, la pagination ne s'arrêterait jamais.
    """

    def __init__(self):
        self.calls = 0

    def get(self, url):

        self.calls += 1

        offset = self.calls * 20

        html = f"""
        <html><body>
        <div class="delimiter">
          <div class="titre_fichier"><a href="/file/{self.calls}/">Doc {self.calls}</a></div>
          <div class="information">
            <a href="/file/{self.calls}/"><img class="image" src="/_images/ext/icon_pdf.gif"></a>
            Publié le : 01/01/2026
          </div>
        </div>
        <div class="pager">
          <a href="/downloads/?tag=Emploi&amp;p={offset}">»</a>
        </div>
        </body></html>
        """

        return FakeResponse(url, html)


def test_crawl_stops_at_max_pages_to_avoid_an_infinite_loop():

    http_client = InfiniteHTTPClient()

    crawler = CategoryDiscoveryCrawler(
        http_client=http_client,
        max_pages_per_category=3
    )

    result = crawler.crawl(FakeConnector())

    assert http_client.calls == 3
    assert result.pages_visited == 3
