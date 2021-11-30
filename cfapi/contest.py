import re
from urllib.parse import urljoin

from .base import Base
from .problem import Problem


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, Tuple
    from bs4 import BeautifulSoup


class Contest(Base):
    # TODO: Contest, ProblemSet, and GroupContest should all share the same base class.

    _FROM_URL_REGEX = re.compile("contests?/(?P<id>[0-9]{1,})")

    @classmethod
    def identifier_from_url(cls, url: str) -> "Optional[int]":
        result = re.search(cls._FROM_URL_REGEX, url)
        if result:
            return int(result.group("id"))

    @property
    def url(self) -> str:
        """The URL to the page where the information is scraped from."""
        return urljoin(self.BASE_URL, f"contest/{self.identifier}")

    @property
    def _problems_table(self) -> "BeautifulSoup":
        return self.data.find("table", {"class": "problems"})

    def problems(self) -> "Tuple[Problem]":
        """Returns a tuple containing lazy-loaded instances that represent
        the problems in the contest."""

        # Extract all data rows from the problems table,
        # and ignore the first row which contains the headers.

        rows = self._problems_table.find_all("tr")[1:]
        links = [row.find("a", href=True)["href"] for row in rows]
        return tuple(Problem.from_url(link) for link in links)
