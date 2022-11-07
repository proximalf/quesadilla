from datetime import datetime


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
