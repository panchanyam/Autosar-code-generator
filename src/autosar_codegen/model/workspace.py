"""
autosar_codegen.model.workspace
===============================

Central AUTOSAR Intermediate Representation (IR) workspace.

The Workspace owns all parsed AUTOSAR objects and provides
a common access point for parsers, resolvers, validators,
generators and simulators.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from threading import RLock
from typing import Iterator, TypeVar

from autosar_codegen.model.base import AutosarElement


T = TypeVar("T", bound=AutosarElement)


@dataclass(slots=True)
class WorkspaceStatistics:
    """
    Workspace object statistics.
    """

    total_objects: int = 0

    packages: int = 0

    signals: int = 0

    pdus: int = 0

    frames: int = 0

    datatypes: int = 0

    networks: int = 0


class Workspace:
    """
    Root container for the AUTOSAR model.

    The workspace represents the complete parsed
    AUTOSAR system.

    Example
    -------

    workspace = Workspace()

    workspace.add(signal)

    """

    def __init__(
        self,
    ) -> None:

        self._root_objects: list[AutosarElement] = []

        self._lock = RLock()

        self._statistics = WorkspaceStatistics()

        #
        # SymbolTable will be injected
        # in Commit 0004.2.4
        #
        self.symbol_table = None


    # ==============================================================
    # Object Management
    # ==============================================================


    def add(
        self,
        element: AutosarElement,
    ) -> None:
        """
        Add an AUTOSAR object.

        Root objects have no parent.
        """

        with self._lock:

            if element.parent is None:

                self._root_objects.append(element)

            self._update_statistics(element)


    def remove(
        self,
        element: AutosarElement,
    ) -> None:
        """
        Remove an object.
        """

        with self._lock:

            if element in self._root_objects:

                self._root_objects.remove(element)

            self._recalculate_statistics()



    # ==============================================================
    # Traversal
    # ==============================================================


    def walk(
        self,
    ) -> Iterator[AutosarElement]:
        """
        Iterate over the complete model.
        """

        for root in self._root_objects:

            yield from root.walk()



    # ==============================================================
    # Searching
    # ==============================================================


    def find_by_type(
        self,
        cls: type[T],
    ) -> list[T]:
        """
        Find objects by class type.
        """

        result: list[T] = []

        for element in self.walk():

            if isinstance(element, cls):

                result.append(element)

        return result



    def find_first(
        self,
        cls: type[T],
    ) -> T | None:
        """
        Return first object matching type.
        """

        for element in self.walk():

            if isinstance(element, cls):

                return element

        return None



    # ==============================================================
    # Statistics
    # ==============================================================


    @property
    def statistics(
        self,
    ) -> WorkspaceStatistics:
        """
        Return workspace statistics.
        """

        return self._statistics



    def _update_statistics(
        self,
        element: AutosarElement,
    ) -> None:
        """
        Update counters.
        """

        self._statistics.total_objects += 1


    def _recalculate_statistics(
        self,
    ) -> None:
        """
        Rebuild statistics.

        Used after removal.
        """

        stats = WorkspaceStatistics()

        for _ in self.walk():

            stats.total_objects += 1


        self._statistics = stats



    # ==============================================================
    # Utility
    # ==============================================================


    def clear(
        self,
    ) -> None:
        """
        Remove all objects.
        """

        with self._lock:

            self._root_objects.clear()

            self._statistics = WorkspaceStatistics()



    def __len__(
        self,
    ) -> int:
        """
        Number of model objects.
        """

        return self._statistics.total



    def __iter__(
        self,
    ):
        """
        Iterate workspace.
        """

        return self.walk()