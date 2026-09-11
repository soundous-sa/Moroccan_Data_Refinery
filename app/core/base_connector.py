from abc import ABC, abstractmethod

from app.core.connector_result import ConnectorResult


class BaseConnector(ABC):

    def __init__(self, name: str):

        self.name = name

    @abstractmethod
    def discover(self) -> ConnectorResult:
        pass

    @abstractmethod
    def crawl(self):
        pass

    @abstractmethod
    def download(self):
        pass

    @abstractmethod
    def parse(self):
        pass