from .base import Base

from urllib.parse import urljoin


class Profile(Base):
    @property
    def url(self) -> str:
        """The URL to the page where the information is scraped from."""
        return urljoin(self.BASE_URL, f"profile/{self.identifier}")
