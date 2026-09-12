from app.services.discovery.pagination_navigator import PaginationNavigator


PAGE_WITH_NEXT = """
<html><body>
<div class="pager">
    <a class="sel" href="/downloads/?tag=Emploi">1</a>
    <a href="/downloads/?tag=Emploi&amp;p=20">2</a>
    <a href="/downloads/?tag=Emploi&amp;p=20">»</a>
</div>
</body></html>
"""

LAST_PAGE = """
<html><body>
<div class="pager">
    <a href="/downloads/?tag=Emploi&amp;">1</a>
    <a href="/downloads/?tag=Emploi&amp;p=200">«</a>
    <a class="sel" href="/downloads/?tag=Emploi&amp;p=220">12</a>
</div>
</body></html>
"""

SHORT_PAGER_WITHOUT_NEXT_SYMBOL = """
<html><body>
<div class="pager">
    <a class="sel" href="/downloads/?tag=Comptes+nationaux">1</a>
    <a href="/downloads/?tag=Comptes+nationaux&amp;p=20">2</a>
    <a href="/downloads/?tag=Comptes+nationaux&amp;p=40">3</a>
    <a href="/downloads/?tag=Comptes+nationaux&amp;p=60">4</a>
</div>
</body></html>
"""

SHORT_PAGER_LAST_PAGE = """
<html><body>
<div class="pager">
    <a href="/downloads/?tag=Comptes+nationaux">1</a>
    <a href="/downloads/?tag=Comptes+nationaux&amp;p=20">2</a>
    <a href="/downloads/?tag=Comptes+nationaux&amp;p=40">3</a>
    <a class="sel" href="/downloads/?tag=Comptes+nationaux&amp;p=60">4</a>
</div>
</body></html>
"""

NO_PAGER = "<html><body><div class='content'>Rien ici</div></body></html>"


def test_find_next_url_returns_the_next_page():

    navigator = PaginationNavigator()

    next_url = navigator.find_next_url(
        PAGE_WITH_NEXT,
        "https://www.hcp.ma/downloads/?tag=Emploi"
    )

    assert next_url == "https://www.hcp.ma/downloads/?tag=Emploi&p=20"


def test_find_next_url_returns_none_on_the_last_page():

    navigator = PaginationNavigator()

    next_url = navigator.find_next_url(
        LAST_PAGE,
        "https://www.hcp.ma/downloads/?tag=Emploi&p=220"
    )

    assert next_url is None


def test_find_next_url_works_on_a_short_pager_without_a_next_symbol():

    # Régression : sur un pager de 4 pages, HCP n'affiche jamais le
    # symbole "»", seulement des numéros de page.
    navigator = PaginationNavigator()

    next_url = navigator.find_next_url(
        SHORT_PAGER_WITHOUT_NEXT_SYMBOL,
        "https://www.hcp.ma/downloads/?tag=Comptes+nationaux"
    )

    assert next_url == (
        "https://www.hcp.ma/downloads/?tag=Comptes+nationaux&p=20"
    )


def test_find_next_url_returns_none_on_the_last_page_of_a_short_pager():

    navigator = PaginationNavigator()

    next_url = navigator.find_next_url(
        SHORT_PAGER_LAST_PAGE,
        "https://www.hcp.ma/downloads/?tag=Comptes+nationaux&p=60"
    )

    assert next_url is None


def test_find_next_url_returns_none_without_a_pager():

    navigator = PaginationNavigator()

    next_url = navigator.find_next_url(
        NO_PAGER,
        "https://www.hcp.ma/downloads/?tag=Emploi"
    )

    assert next_url is None
