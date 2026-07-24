"""
autosar_codegen.model.symbol_table
===================================

Symbol table implementation for AUTOSAR Intermediate Representation.

The symbol table provides fast lookup of AUTOSAR objects by:

    - Absolute AUTOSAR path
    - UUID
    - Object type

The Workspace owns objects.
The SymbolTable only indexes them.

"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from threading import RLock
from typing import Iterator, TypeVar

from autosar_codegen.model.base import AutosarElement


T = TypeVar(
    "T",
    bound=AutosarElement,
)


# ============================================================================
# Statistics
# ============================================================================


@dataclass(slots=True)
class SymbolStatistics:
    """
    Symbol table statistics.
    """

    paths: int = 0

    uuids: int = 0

    types: int = 0

    objects: int = 0



# ============================================================================
# Symbol Table
# ============================================================================


class SymbolTable:
    """
    AUTOSAR symbol table.

    Provides O(1) object lookup.

    Example
    -------

    table.register(signal)

    table.find(
        "/Communication/VehicleSpeed"
    )

    """

    def __init__(
        self,
    ) -> None:

        self._path_index: dict[
            str,
            AutosarElement
        ] = {}


        self._uuid_index: dict[
            str,
            AutosarElement
        ] = {}


        self._type_index: dict[
            type,
            set[AutosarElement]
        ] = defaultdict(set)


        self._lock = RLock()



    # =========================================================================
    # Registration
    # =========================================================================


    def register(
        self,
        element: AutosarElement,
    ) -> bool:
        """
        Register an AUTOSAR object.

        Returns
        -------
        bool

            True if registered successfully.
        """

        with self._lock:


            path = element.path


            #
            # Duplicate path protection
            #
            if path in self._path_index:

                return False



            #
            # Path index
            #
            self._path_index[path] = element



            #
            # UUID index
            #
            if element.uuid:

                self._uuid_index[
                    element.uuid
                ] = element



            #
            # Type index
            #
            self._type_index[
                type(element)
            ].add(element)



        return True



    def unregister(
        self,
        element: AutosarElement,
    ) -> None:
        """
        Remove object from indexes.
        """

        with self._lock:


            self._path_index.pop(
                element.path,
                None,
            )


            if element.uuid:

                self._uuid_index.pop(
                    element.uuid,
                    None,
                )


            objects = self._type_index.get(
                type(element),
            )


            if objects:

                objects.discard(
                    element,
                )



    # =========================================================================
    # Lookup
    # =========================================================================


    def find(
        self,
        path: str,
    ) -> AutosarElement | None:
        """
        Find object by absolute path.
        """

        return self._path_index.get(
            path,
        )



    def find_uuid(
        self,
        uuid: str,
    ) -> AutosarElement | None:
        """
        Find object by UUID.
        """

        return self._uuid_index.get(
            uuid,
        )



    def find_type(
        self,
        cls: type[T],
    ) -> list[T]:
        """
        Find objects by type.
        """

        return list(
            self._type_index.get(
                cls,
                set(),
            )
        )



    # =========================================================================
    # Queries
    # =========================================================================


    def contains(
        self,
        path: str,
    ) -> bool:
        """
        Check path existence.
        """

        return path in self._path_index



    def contains_uuid(
        self,
        uuid: str,
    ) -> bool:
        """
        Check UUID existence.
        """

        return uuid in self._uuid_index



    # =========================================================================
    # Statistics
    # =========================================================================


    def statistics(
        self,
    ) -> SymbolStatistics:
        """
        Return index statistics.
        """

        return SymbolStatistics(

            paths=len(
                self._path_index
            ),

            uuids=len(
                self._uuid_index
            ),

            types=len(
                self._type_index
            ),

            objects=sum(
                len(x)
                for x in self._type_index.values()
            ),
        )



    # =========================================================================
    # Maintenance
    # =========================================================================


    def clear(
        self,
    ) -> None:
        """
        Clear all indexes.
        """

        with self._lock:

            self._path_index.clear()

            self._uuid_index.clear()

            self._type_index.clear()



    def __len__(
        self,
    ) -> int:
        """
        Number of indexed objects.
        """

        return len(
            self._path_index
        )



    def __iter__(
        self,
    ) -> Iterator[AutosarElement]:
        """
        Iterate indexed objects.
        """

        return iter(
            self._path_index.values()
        )