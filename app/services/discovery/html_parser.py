from bs4 import BeautifulSoup

from app.services.discovery.html_element import HTMLElement


class HTMLParser:

    def parse(self, html: str):

        return BeautifulSoup(html, "lxml")

    def find_all(self, html: str, tag: str):

        soup = self.parse(html)

        elements = []

        for item in soup.find_all(tag):

            elements.append(self._create_element(item))

        return elements

    def select(self, html: str, selector: str):

        soup = self.parse(html)

        elements = []

        for item in soup.select(selector):

            elements.append(self._create_element(item))

        return elements

    def _create_element(self, tag):

        return HTMLElement(

            tag=tag.name,

            text=tag.get_text(strip=True),

            href=tag.get("href"),

            classes=tag.get("class", []),

            identifier=tag.get("id", ""),

            attributes=tag.attrs

        )