"""
Configuration manager for AUTOSAR Code Generator.

Loads YAML configuration and exposes strongly typed accessors.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from autosar_codegen.core.exceptions import ConfigurationError


class Config:
    """
    Configuration manager.

    Example
    -------
    >>> cfg = Config("config.yaml")
    >>> cfg.get("language")
    'cpp'
    """

    def __init__(self, file_path: str | Path | None = None):

        self._data: dict[str, Any] = {}

        if file_path is not None:
            self.load(file_path)

    def load(self, file_path: str | Path) -> None:
        """
        Load YAML configuration.
        """

        path = Path(file_path)

        if not path.exists():
            raise ConfigurationError(
                f"Configuration file not found: {path}"
            )

        try:

            with path.open(
                "r",
                encoding="utf-8",
            ) as fp:

                self._data = yaml.safe_load(fp) or {}

        except yaml.YAMLError as exc:
            raise ConfigurationError(str(exc)) from exc

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Return config value.
        """

        return self._data.get(key, default)

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:

        self._data[key] = value

    def save(
        self,
        file_path: str | Path,
    ) -> None:

        path = Path(file_path)

        with path.open(
            "w",
            encoding="utf-8",
        ) as fp:

            yaml.safe_dump(
                self._data,
                fp,
                sort_keys=False,
            )

    @property
    def data(self) -> dict[str, Any]:

        return self._data