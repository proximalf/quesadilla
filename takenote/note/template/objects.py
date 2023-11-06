from datetime import datetime
from typing import Optional


class DateTemplate:
    """Template object."""

    DEFAULT_FORMAT: str = "%A %d %B %Y %H:%M:%S"

    def __init__(self, time: Optional[datetime] = None, format: Optional[str] = None) -> None:
        """
        Time is an optional arg, as class will initialise with current time if no arg
        is provided.

        Parameters
        ----------
        time: Optional[datetime]
            A datetime object of a specified date.
        format: Optional[str]
            A datetime format string, eg: "%A %d %B %Y, %H:%M:%S".
        """

        self.time = datetime.now() if time is None else time
        self.format = format if format is not None else self.DEFAULT_FORMAT

    def as_format(self, format: str = DEFAULT_FORMAT) -> str:
        """
        Returns a datetime string in the format described.
        Queries the current time.
        `format= "%y%m_%d%H%M"`

        Parameters
        ----------
        format: str
            A format to generate datetime strings.

        Returns
        ----------
        str
            Datetime object as string of format.
        """
        return self.time.strftime(format)

    def __str__(self) -> str:
        """Returns a string of the provided date time format, uses internally set format."""
        return self.as_format(self.format)
