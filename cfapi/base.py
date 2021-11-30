from abc import ABC, abstractmethod
from functools import lru_cache as cache

import requests
from bs4 import BeautifulSoup


from .exceptions import InvalidIdentifierException, InvalidURL

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Type, TypeVar
    from re import Pattern

    T = TypeVar("T")


class Base(ABC):

    BASE_URL = "https://codeforces.com/"

    def __init__(self, identifier) -> None:
        self.__id = identifier

    @property
    def identifier(self):
        """A unique identifier that is used to generaate the content URL."""
        return self.__id

    @abstractmethod
    @property
    @classmethod
    def FROM_URL_REGEX(cls) -> "Pattern":
        """A pattern that contains a group named 'id'. This pattern should be
        able to accept all valid URLs of the current object."""

    @classmethod
    def from_url(cls: "Type[T]", url: str) -> "T":
        """Recives a URL as a string, and returns an instance of the of API
        object that represents the information in the given URL."""

        result = cls.FROM_URL_REGEX.search(url)

        if result:
            return cls(result.group("id"))
        else:
            raise InvalidURL(f"Invalid URL {url!r} for {cls.__name__!r}")

    @abstractmethod
    @property
    def url(self):
        """The URL to the page where the information is scraped from."""

    @property
    @cache
    def data(self) -> BeautifulSoup:
        """Sends a https request to scrape the data of the object. By default,
        the data is lazy-loaded, and this method is called only when required
        by other methods."""

        data = requests.get(self.url, allow_redirects=False)
        if data.status_code != 200:
            raise InvalidIdentifierException(
                f"Invalid identifier {self.identifier!r} for {type(self).__name__!r}",
                "(Resource doesn't exist or isn't public).",
            )

        return BeautifulSoup(data.content, "lxml")
