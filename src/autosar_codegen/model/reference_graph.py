"""
autosar_codegen.model.reference_graph
=====================================

Dependency graph for AUTOSAR objects.

Stores relationships between AUTOSAR model objects.

The graph supports:

    Object A depends on Object B

and reverse queries:

    Who depends on Object B?

"""

from __future__ import annotations

from dataclasses import dataclass
from threading import RLock
from typing import Iterator

from autosar_codegen.model.base import AutosarElement


# ============================================================================
# Statistics
# ============================================================================


@dataclass(slots=True)
class ReferenceGraphStatistics:
    """
    Dependency graph statistics.
    """

    objects: int = 0

    edges: int = 0



# ============================================================================
# Reference Graph
# ============================================================================


class ReferenceGraph:
    """
    AUTOSAR dependency graph.

    Example:

        Signal
          |
          v
        Datatype

    """

    def __init__(self) -> None:

        self._forward: dict[
            str,
            set[str]
        ] = {}


        self._reverse: dict[
            str,
            set[str]
        ] = {}


        self._objects: dict[
            str,
            AutosarElement
        ] = {}


        self._lock = RLock()



    # =========================================================================
    # Registration
    # =========================================================================


    def register(
        self,
        element: AutosarElement,
    ) -> None:
        """
        Register object in graph.
        """

        with self._lock:

            key = element.path

            self._objects[key] = element

            self._forward.setdefault(
                key,
                set(),
            )

            self._reverse.setdefault(
                key,
                set(),
            )



    # =========================================================================
    # Dependency Handling
    # =========================================================================


    def add_dependency(
        self,
        source: AutosarElement,
        target: AutosarElement,
    ) -> None:
        """
        Add:

        source --> target
        """

        with self._lock:


            self.register(source)

            self.register(target)


            source_key = source.path

            target_key = target.path


            self._forward[
                source_key
            ].add(
                target_key
            )


            self._reverse[
                target_key
            ].add(
                source_key
            )



    def remove_dependency(
        self,
        source: AutosarElement,
        target: AutosarElement,
    ) -> None:
        """
        Remove dependency.
        """

        with self._lock:

            self._forward.get(
                source.path,
                set(),
            ).discard(
                target.path
            )


            self._reverse.get(
                target.path,
                set(),
            ).discard(
                source.path
            )



    # =========================================================================
    # Queries
    # =========================================================================


    def dependencies(
        self,
        element: AutosarElement,
    ) -> list[AutosarElement]:
        """
        Objects used by this object.
        """

        result = []

        for path in self._forward.get(
            element.path,
            set(),
        ):

            obj = self._objects.get(path)

            if obj:
                result.append(obj)

        return result



    def dependents(
        self,
        element: AutosarElement,
    ) -> list[AutosarElement]:
        """
        Objects using this object.
        """

        result = []

        for path in self._reverse.get(
            element.path,
            set(),
        ):

            obj = self._objects.get(path)

            if obj:
                result.append(obj)

        return result



    # =========================================================================
    # Impact Analysis
    # =========================================================================


    def impact_analysis(
        self,
        element: AutosarElement,
    ) -> list[AutosarElement]:
        """
        Find all objects affected by a change.
        """

        visited: set[str] = set()

        result: list[AutosarElement] = []


        def visit(path: str):

            if path in visited:
                return

            visited.add(path)


            for dependent in self._reverse.get(
                path,
                set(),
            ):

                obj = self._objects.get(
                    dependent
                )

                if obj:

                    result.append(obj)

                    visit(dependent)



        visit(element.path)

        return result



    # =========================================================================
    # Statistics
    # =========================================================================


    def statistics(
        self,
    ) -> ReferenceGraphStatistics:
        """
        Return graph statistics.
        """

        return ReferenceGraphStatistics(

            objects=len(
                self._objects
            ),

            edges=sum(
                len(x)
                for x in self._forward.values()
            ),
        )



    # =========================================================================
    # Maintenance
    # =========================================================================


    def clear(
        self,
    ) -> None:

        with self._lock:

            self._forward.clear()

            self._reverse.clear()

            self._objects.clear()