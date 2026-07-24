"""
autosar_codegen.resolver.registry
=================================

Resolver plugin registry.

Maintains AUTOSAR reference resolvers.
"""

from __future__ import annotations


from dataclasses import dataclass

from threading import RLock


from autosar_codegen.resolver.base import (
    Resolver,
)



# ============================================================================
# Statistics
# ============================================================================


@dataclass(slots=True)
class RegistryStatistics:
    """
    Resolver registry statistics.
    """

    resolvers: int = 0



# ============================================================================
# Resolver Registry
# ============================================================================


class ResolverRegistry:
    """
    Registry for resolver plugins.
    """


    def __init__(
        self,
    ) -> None:


        self._resolvers: list[Resolver] = []


        self._map: dict[
            str,
            Resolver
        ] = {}


        self._lock = RLock()



    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------


    def register(
        self,
        resolver: Resolver,
    ) -> bool:
        """
        Register resolver.

        Returns:

            True  registered
            False duplicate
        """

        with self._lock:


            if resolver.name in self._map:

                return False



            self._resolvers.append(
                resolver
            )


            self._map[
                resolver.name
            ] = resolver



            #
            # Priority ordering
            #
            self._resolvers.sort(

                key=lambda item:
                item.priority

            )


        return True



    def unregister(
        self,
        resolver: Resolver,
    ) -> None:
        """
        Remove resolver.
        """

        with self._lock:


            if resolver.name in self._map:

                del self._map[
                    resolver.name
                ]


            if resolver in self._resolvers:

                self._resolvers.remove(
                    resolver
                )



    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------


    def get(
        self,
        name: str,
    ) -> Resolver | None:
        """
        Find resolver by name.
        """

        resolver = self._map.get(
            name
        )


        if resolver and resolver.enabled:

            return resolver


        return None



    def all(
        self,
    ) -> list[Resolver]:
        """
        Return enabled resolvers.
        """

        return [

            resolver

            for resolver in self._resolvers

            if resolver.enabled

        ]



    # ------------------------------------------------------------------
    # Dependency Ordering
    # ------------------------------------------------------------------


    def ordered(
        self,
    ) -> list[Resolver]:
        """
        Return resolvers ordered by dependency.

        Uses dependency names declared
        in ResolverMetadata.
        """

        result: list[Resolver] = []

        visited: set[str] = set()



        def visit(
            resolver: Resolver,
        ):


            if resolver.name in visited:

                return



            visited.add(
                resolver.name
            )


            for dependency in resolver.dependencies:


                dependency_resolver = self.get(
                    dependency
                )


                if dependency_resolver:

                    visit(
                        dependency_resolver
                    )


            result.append(
                resolver
            )



        for resolver in self.all():

            visit(
                resolver
            )


        return result



    # ------------------------------------------------------------------
    # Information
    # ------------------------------------------------------------------


    def statistics(
        self,
    ) -> RegistryStatistics:
        """
        Registry statistics.
        """

        return RegistryStatistics(

            resolvers=len(
                self._resolvers
            )

        )



    def clear(
        self,
    ) -> None:
        """
        Remove all resolvers.
        """

        with self._lock:

            self._resolvers.clear()

            self._map.clear()



    def __iter__(
        self,
    ):
        """
        Iterate resolvers.
        """

        return iter(
            self.ordered()
        )