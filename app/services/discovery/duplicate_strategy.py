from enum import Enum


class DuplicateStrategy(Enum):

    URL = "url"

    TITLE = "title"

    URL_AND_TITLE = "url_and_title"