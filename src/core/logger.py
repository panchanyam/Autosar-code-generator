"""
Central logging utility.

Every module should obtain its logger using

get_logger(__name__)
"""

from __future__ import annotations

import logging
from pathlib import Path

from rich.logging import RichHandler

LOG_DIRECTORY = Path("logs")

LOG_DIRECTORY.mkdir(
    exist_ok=True,
)

LOG_FILE = LOG_DIRECTORY / "autosar_codegen.log"


def configure_logger(
    level: int = logging.INFO,
) -> None:
    """
    Configure global logging.
    """

    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                rich_tracebacks=True,
            ),
            logging.FileHandler(
                LOG_FILE,
                encoding="utf-8",
            ),
        ],
    )


def get_logger(
    name: str,
) -> logging.Logger:
    """
    Return logger.
    """

    return logging.getLogger(name)