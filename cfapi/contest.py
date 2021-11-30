import re
from urllib.parse import urljoin
from .base import Base


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional


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
