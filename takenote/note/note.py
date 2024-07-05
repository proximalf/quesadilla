import yaml
from typing import Dict, Optional
from datetime import datetime

from .template.objects import DateTemplate


class Note:
    """
    A note class. This object is passed to the template renderer, refer to templating for more information.
    """

    def __init__(
        self,
        front_matter: Optional[Dict[str, str]] = None,
        title: Optional[str] = None,
        content: Optional[str] = None,
        date: Optional[datetime] = None,
    ) -> None:
        """

        Parameters
        ----------
        front_matter: Dict[str, any]
            Metadata information found at the top of a file.
        title: Optional[str]
            File can have a title.
        content: Option[str]
            File can have content.
        date: datetime
            Datetime object, can be None, if so format_datetime returns result from `datetime.now()`

        """
        self.front_matter = front_matter
        self.title = title
        self.content = content
        self._date = date

    @property
    def yaml(self) -> str:
        """Returns a YAML String"""
        if self.front_matter is None:
            return ""
        return yaml.dump(self.front_matter, sort_keys=True)

    @property
    def date(self) -> DateTemplate:
        """Returns a DateTemplate object for use in templates"""
        return DateTemplate(self._date)

    @date.setter
    def date(self, value: datetime) -> None:
        """Set internal datetime object"""
        self._date = value

    @property
    def datetime(self) -> datetime:
        """Return datetime object"""
        return self._date

    def __str__(self):
        """Return String Note Component"""
        return "---\n" f"{self.yaml}\n" "---\n" f"{self.title}\n" f"{self.date}\n" f"{self.content}\n"
