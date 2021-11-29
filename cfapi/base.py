from abc import ABC, abstractproperty
from functools import lru_cache as cache

import requests
from bs4 import BeautifulSoup


class InvalidIdentifierException(ValueError):
    """Raised when trying to load data from an invalid URL (probably because the
    data doesn't exist or isn't public)."""


class Base(ABC):

    BASE_URL = "https://codeforces.com/"

    @abstractproperty
    def url(self):
        """The URL to the page where the information is scraped from."""

    @abstractproperty
    def identifier(self):
        """A unique identifier that is used to generaate the content URL."""

    @property
    @cache
    def data(self) -> BeautifulSoup:
        """Sends a https request to scrape the data of the object. By default,
        the data is lazy-loaded, and this method is called only when required
        by other methods."""

        data = requests.get(self.url)
        if data.status_code != 200:
            raise InvalidIdentifierException(
                f"Invalid identifier {self.identifier!r} for {type(self).__name__!r}",
                "(Resource doesn't exist or isn't public).",
            )

        return BeautifulSoup(data.content, "lxml")
