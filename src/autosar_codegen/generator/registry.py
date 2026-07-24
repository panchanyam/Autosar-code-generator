"""
autosar_codegen.generator.registry
==================================

Generator plugin registry.

Maintains available AUTOSAR code generators.
"""

from __future__ import annotations


from dataclasses import dataclass


from threading import RLock


from autosar_codegen.generator.base import (
    Generator,
)



# ============================================================================
# Statistics
# ============================================================================


@dataclass(slots=True)
class RegistryStatistics:
    """
    Generator registry statistics.
    """

    generators: int = 0



# ============================================================================
# Generator Registry
# ============================================================================


class GeneratorRegistry:
    """
    Registry for generator plugins.
    """


    def __init__(
        self,
    ) -> None:


        self._generators: list[Generator] = []


        self._map: dict[
            str,
            Generator
        ] = {}


        self._lock = RLock()



    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------


    def register(
        self,
        generator: Generator,
    ) -> bool:
        """
        Register generator.

        Returns:

            True  registered

            False duplicate
        """

        with self._lock:


            if generator.name in self._map:

                return False



            self._generators.append(
                generator
            )


            self._map[
                generator.name
            ] = generator



            #
            # Priority ordering
            #
            self._generators.sort(

                key=lambda item:
                item.priority

            )


        return True



    def unregister(
        self,
        generator: Generator,
    ) -> None:
        """
        Remove generator.
        """

        with self._lock:


            if generator.name in self._map:

                del self._map[
                    generator.name
                ]


            if generator in self._generators:

                self._generators.remove(
                    generator
                )



    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------


    def get(
        self,
        name: str,
    ) -> Generator | None:
        """
        Get generator by name.
        """

        generator = self._map.get(
            name
        )


        if generator and generator.enabled:

            return generator


        return None



    def get_language(
        self,
        language: str,
    ) -> list[Generator]:
        """
        Return generators for language.
        """

        return [

            generator

            for generator in self._generators

            if (

                generator.enabled

                and

                generator.language.lower()
                ==
                language.lower()

            )

        ]



    def all(
        self,
    ) -> list[Generator]:
        """
        Return enabled generators.
        """

        return [

            generator

            for generator in self._generators

            if generator.enabled

        ]



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

            generators=len(
                self._generators
            )

        )



    def clear(
        self,
    ) -> None:
        """
        Remove all generators.
        """

        with self._lock:

            self._generators.clear()

            self._map.clear()



    def __iter__(
        self,
    ):
        """
        Iterate generators.
        """

        return iter(
            self.all()
        )