import click


class Output:
    """
    Object for writing using click.echo(), set level for verbosity.

    Level
    ----------
    0 : Minimum level, Errors
    1 : Info
    2 : Some Debug
    3 : Extra Debug
    """

    def __init__(self) -> None:
        """Initialises with a set level 0."""
        self._level = 0

    def echo(self, msg, level: int = 3, **kwargs) -> None:
        """
        Echos msg to output.

        Level
        ----------
        0 : Minimum level, Errors
        1 : Info
        2 : Some Debug
        3 : Extra Debug

        Parameters
        ----------
        msg: str
            Message to pass to echo.
        level: int
            The level the message is printed as.
        kwargs: Dict[str, Any]
            Kwargs to pass to echo
        """
        if level <= self._level:
            click.secho(msg, **kwargs)  # type: ignore

    @property
    def level(self) -> int:
        """
        Return set level.

        Returns
        ----------
        int
            Level as int.
        """
        return self._level

    @level.setter
    def level(self, level: int) -> None:
        """
        Set level. Refer to class doc for more on level.

        Parameters
        ----------
        level: int
            int to set level as.
        """
        self._level = level


output = Output()
