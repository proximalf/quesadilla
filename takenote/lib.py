from datetime import datetime


def zettelkasten(format: str = "%y%m_%d%H%M") -> str:
    """
    Returns a datetime string in the format of a zettelkasten title.
    """
    return datetime.now().strftime(format)
