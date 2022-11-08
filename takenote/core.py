from datetime import datetime
from typing import Optional


class DateTemplate:
    def __init__(self, time: Optional[datetime] = None):
        self.time = datetime.now() if time is None else time

    def format(self, format):
        """
        Returns a datetime string in the format described.
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
