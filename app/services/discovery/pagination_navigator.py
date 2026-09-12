from app.services.discovery.html_parser import HTMLParser
from app.services.discovery.url_manager import URLManager


class PaginationNavigator:
    """
    Trouve l'URL de la page suivante dans un pager HCP
    (<div class="pager"> avec un <a> par page).

    Le lien "»" (page suivante) n'est présent que lorsqu'il y a beaucoup
    de pages : sur un pager court (ex: 4 pages), il n'existe pas du tout,
    seuls les numéros de page sont affichés. La détection fiable consiste
    donc à repérer la page courante (<a class="sel">) puis à prendre le
    lien qui la suit immédiatement dans le pager, que ce soit un numéro
    de page ou le symbole "»" — les deux mènent à la même page suivante.
    """

    DEFAULT_PAGER_SELECTOR = "div.pager"

    DEFAULT_CURRENT_PAGE_SELECTOR = "a.sel"

    DEFAULT_NEXT_SYMBOL = "»"

    def __init__(
        self,
        pager_selector: str = DEFAULT_PAGER_SELECTOR,
        current_page_selector: str = DEFAULT_CURRENT_PAGE_SELECTOR,
        next_symbol: str = DEFAULT_NEXT_SYMBOL
    ):

        self.pager_selector = pager_selector

        self.current_page_selector = current_page_selector

        self.next_symbol = next_symbol

        self.html_parser = HTMLParser()

    # ==================================================
    # URL DE LA PAGE SUIVANTE
    # ==================================================

    def find_next_url(self, html: str, current_url: str) -> str | None:

        soup = self.html_parser.parse(html)

        pager = soup.select_one(self.pager_selector)

        if pager is None:

            return None

        next_href = self._find_next_after_current_page(pager)

        if next_href is None:

            next_href = self._find_next_symbol(pager)

        if next_href is None:

            return None

        return URLManager.join(current_url, next_href)

    def _find_next_after_current_page(self, pager):

        current = pager.select_one(self.current_page_selector)

        if current is None:

            return None

        next_link = current.find_next_sibling("a")

        if next_link is None or not next_link.get("href"):

            return None

        return next_link["href"]

    def _find_next_symbol(self, pager):

        for link in pager.find_all("a", href=True):

            if link.get_text(strip=True) == self.next_symbol:

                return link["href"]

        return None
