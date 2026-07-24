"""
autosar_codegen.parser.registry
===============================

AUTOSAR parser registry.

Maintains parser plugins and routes
XML nodes to matching parsers.

"""

from __future__ import annotations

from dataclasses import dataclass
from threading import RLock

from autosar_codegen.parser.base import Parser
from autosar_codegen.xml.walker import XmlNode



# ============================================================================
# Statistics
# ============================================================================


@dataclass(slots=True)
class RegistryStatistics:
    """
    Parser registry statistics.
    """

    parsers: int = 0

    tags: int = 0



# ============================================================================
# Parser Registry
# ============================================================================


class ParserRegistry:
    """
    Registry for AUTOSAR parsers.

    Example:

        registry.register(
            SignalParser()
        )

    """

    def __init__(
        self,
    ) -> None:

        self._parsers: list[Parser] = []


        self._tag_map: dict[
            str,
            list[Parser]
        ] = {}


        self._lock = RLock()



    # -------------------------------------------------------------------------
    # Registration
    # -------------------------------------------------------------------------


    def register(
        self,
        parser: Parser,
    ) -> bool:
        """
        Register parser.

        Returns:

            True  registered
            False duplicate
        """

        with self._lock:


            #
            # Duplicate parser name
            #
            for existing in self._parsers:

                if existing.name == parser.name:

                    return False



            self._parsers.append(
                parser
            )


            #
            # Register supported tags
            #
            for tag in parser.metadata.supported_tags:


                self._tag_map.setdefault(
                    tag,
                    [],
                ).append(
                    parser
                )


                #
                # Higher priority first
                #
                self._tag_map[tag].sort(
                    key=lambda item:
                    item.priority
                )



        return True



    def unregister(
        self,
        parser: Parser,
    ) -> None:
        """
        Remove parser.
        """

        with self._lock:


            if parser in self._parsers:

                self._parsers.remove(
                    parser
                )


            for tag in parser.metadata.supported_tags:


                parsers = self._tag_map.get(
                    tag,
                    [],
                )


                if parser in parsers:

                    parsers.remove(
                        parser
                    )



    # -------------------------------------------------------------------------
    # Lookup
    # -------------------------------------------------------------------------


    def find(
        self,
        node: XmlNode,
    ) -> list[Parser]:
        """
        Find parsers supporting XML node.
        """

        parsers = self._tag_map.get(
            node.tag,
            [],
        )


        return [
            parser
            for parser in parsers
            if parser.enabled
        ]



    def find_by_tag(
        self,
        tag: str,
    ) -> list[Parser]:
        """
        Find parsers by tag.
        """

        return [
            parser
            for parser in self._tag_map.get(
                tag,
                [],
            )
            if parser.enabled
        ]



    # -------------------------------------------------------------------------
    # Information
    # -------------------------------------------------------------------------


    def statistics(
        self,
    ) -> RegistryStatistics:
        """
        Return registry statistics.
        """

        return RegistryStatistics(

            parsers=len(
                self._parsers
            ),

            tags=len(
                self._tag_map
            ),
        )



    def clear(
        self,
    ) -> None:
        """
        Remove all parsers.
        """

        with self._lock:

            self._parsers.clear()

            self._tag_map.clear()



    def __iter__(
        self,
    ):
        """
        Iterate parsers.
        """

        return iter(
            self._parsers
        )