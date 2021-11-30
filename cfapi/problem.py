from .base import Base

import re
from urllib.parse import urljoin

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional


class Problem(Base):

    _FROM_URL_REGEX = re.compile(
        "/(?P<setid>[0-9]+)(/.*)*/(?P<problemid>[a-zA-Z]+[0-9]*)"
    )
    _SPLIT_IDENTIFIER_REGEX = re.compile(
        "(?P<setid>[0-9]+)(?P<problemid>[a-zA-Z]+[0-9]*)"
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

    def _get_header_entry(self, name: str) -> str:
        header = self.data.find("div", {"class": "header"})
        entry = header.find("div", {"class": name})
        return entry.find(text=True, recursive=False).get_text()

    # ------------------------------------------------------------ Metadata -- #

    @property
    def title(self) -> str:
        return self._get_header_entry("title")

    @property
    def time_limit(self) -> str:
        return self._get_header_entry("time-limit")

    @property
    def memory_limit(self) -> str:
        return self._get_header_entry("memory-limit")

    @property
    def input_file(self) -> str:
        return self._get_header_entry("input-file")

    @property
    def output_file(self) -> str:
        return self._get_header_entry("output-file")
