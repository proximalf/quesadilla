from datetime import datetime
from typing import Optional


class DateTemplate:
    """Template object."""

    def __init__(self, time: Optional[datetime] = None) -> None:
        """
        Time is an optional arg, as class will initialise with current time if no arg
        is provided.

        Parameters
        ----------
        time: Optional[datetime]
            A datetime object of a specified date.
        """
        self.time = datetime.now() if time is None else time

    def format(self, format: str) -> str:
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


def zettelkasten(format: str = "%y%m_%d%H%M") -> str:
    """
    Returns a datetime string in the format of a zettelkasten title.
    Queries the current time.

    Parameters
    ----------
    format: str
        A format to generate datetime strings.

    Returns
    ----------
    str
        Datetime object as string of format.
    """
    return datetime.now().strftime(format)
