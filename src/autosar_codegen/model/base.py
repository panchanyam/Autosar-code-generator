"""
autosar_codegen.model.base
==========================

Base classes for the AUTOSAR Intermediate Representation (IR).

Every AUTOSAR object derives from AutosarElement.

The design intentionally mirrors compiler object models:
    Workspace
        └── Package
              └── Signal
              └── PDU
              └── Frame
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator
from uuid import uuid4


# =============================================================================
# Source Information
# =============================================================================


@dataclass(slots=True)
class SourceInfo:
    """
    Location of an AUTOSAR element inside an ARXML file.
    """

    file: Path | None = None

    line: int | None = None

    column: int | None = None


# =============================================================================
# Base Element
# =============================================================================


@dataclass(slots=True)
class AutosarElement:
    """
    Root AUTOSAR object.

    Every model object inherits from this class.
    """

    uuid: str = field(default_factory=lambda: str(uuid4()))

    parent: AutosarElement | None = field(
        default=None,
        repr=False,
    )

    children: list[AutosarElement] = field(
        default_factory=list,
        repr=False,
    )

    source: SourceInfo = field(
        default_factory=SourceInfo,
    )

    admin_data: dict[str, str] = field(
        default_factory=dict,
        repr=False,
    )

    variation_point: str | None = None

    # -----------------------------------------------------------------

    def add_child(
        self,
        child: AutosarElement,
    ) -> None:
        """
        Add a child element.
        """

        child.parent = self

        self.children.append(child)

    # -----------------------------------------------------------------

    def remove_child(
        self,
        child: AutosarElement,
    ) -> None:
        """
        Remove child.
        """

        self.children.remove(child)

        child.parent = None

    # -----------------------------------------------------------------

    def walk(self) -> Iterator[AutosarElement]:
        """
        Depth-first traversal.
        """

        yield self

        for child in self.children:
            yield from child.walk()

    # -----------------------------------------------------------------

    @property
    def root(self) -> AutosarElement:
        """
        Return workspace root.
        """

        node = self

        while node.parent is not None:
            node = node.parent

        return node

    # -----------------------------------------------------------------

    @property
    def depth(self) -> int:
        """
        Tree depth.
        """

        level = 0

        node = self.parent

        while node is not None:
            level += 1
            node = node.parent

        return level

    # -----------------------------------------------------------------

    @property
    def path(self) -> str:
        """
        Absolute AUTOSAR path.

        Overridden by NamedElement.
        """

        return "/"

    # -----------------------------------------------------------------

    def find(
        self,
        cls: type,
    ) -> Iterator[AutosarElement]:
        """
        Find descendants by type.
        """

        for node in self.walk():

            if isinstance(node, cls):
                yield node


# =============================================================================
# Named Element
# =============================================================================


@dataclass(slots=True)
class NamedElement(AutosarElement):
    """
    AUTOSAR object having SHORT-NAME.
    """

    short_name: str = ""

    long_name: str | None = None

    description: str | None = None

    category: str | None = None

    # -----------------------------------------------------------------

    @property
    def path(self) -> str:
        """
        AUTOSAR absolute path.
        """

        if self.parent is None:
            return f"/{self.short_name}"

        if isinstance(self.parent, NamedElement):
            return f"{self.parent.path}/{self.short_name}"

        return f"/{self.short_name}"

    # -----------------------------------------------------------------

    def __str__(self) -> str:

        return self.path

    # -----------------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(short_name='{self.short_name}')"
        )