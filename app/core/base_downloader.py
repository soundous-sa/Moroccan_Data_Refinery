from abc import ABC, abstractmethod


class BaseDownloader(ABC):

    @abstractmethod
    def download(self, url: str, destination: str):
        pass