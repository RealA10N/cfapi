from .base import Base

import re
from urllib.parse import urljoin

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional


class Problem(Base):

    _FROM_URL_REGEX = re.compile(
        "/(?P<setid>[0-9]+)(/.*)*/(?P<problemid>[a-zA-Z][0-9]?)"
    )
    _SPLIT_IDENTIFIER_REGEX = re.compile(
        "(?P<setid>[0-9]+)(?P<problemid>[a-zA-Z][0-9]?)"
    )

    @classmethod
    def identifier_from_url(cls, url: str) -> "Optional[str]":
        result = re.search(cls._FROM_URL_REGEX, url)
        if result:
            return result.group("setid") + result.group("problemid")

    @property
    def url(self) -> str:
        match = self._SPLIT_IDENTIFIER_REGEX.match(self.identifier)
        set, id = match.group("setid", "problemid")
        # TODO: add support for not only contests, but also problemsets, groups, etc.
        return urljoin(self.BASE_URL, f"contest/{set}/problem/{id}")
