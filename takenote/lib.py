from datetime import datetime


def zettelkasten():
    """
    Returns a datetime string in the format of a zettelkasten title.
    """
    return datetime.now().strftime("%y%m_%d%H%M")
