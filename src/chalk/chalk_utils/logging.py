import logging

from rich.logging import RichHandler


def get_rich_logger(
    level: int = logging.INFO, format: str = "{funcName} - {message}"
) -> logging.Logger:
    logging.basicConfig(
        format=format,
        level=level,
        datefmt="%Y-%m-%d %H:%M",
        style="{",
        handlers=[RichHandler()],
    )

    return logging.getLogger("rich")
