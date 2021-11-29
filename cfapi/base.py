from abc import ABC, abstractproperty


class Base(ABC):

    BASE_URL = "https://codeforces.com/"

    @abstractproperty
    def url(self):
        """The URL to the page where the information is scraped from."""
