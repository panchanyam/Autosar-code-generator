"""
autosar_codegen.parser.dispatcher
=================================

AUTOSAR parser execution engine.

Routes XML nodes to registered parsers.

"""

from __future__ import annotations

from dataclasses import dataclass

from autosar_codegen.parser.registry import (
    ParserRegistry,
)

from autosar_codegen.parser.context import (
    ParserContext,
)

from autosar_codegen.parser.base import (
    Parser,
)

from autosar_codegen.xml.walker import (
    XmlWalker,
    XmlNode,
)



# ============================================================================
# Dispatcher Statistics
# ============================================================================


@dataclass(slots=True)
class DispatcherStatistics:
    """
    Dispatcher execution statistics.
    """

    nodes_processed: int = 0

    parser_calls: int = 0

    successful: int = 0

    failed: int = 0

    skipped: int = 0



# ============================================================================
# Parser Dispatcher
# ============================================================================


class ParserDispatcher:
    """
    Executes registered AUTOSAR parsers.

    """

    def __init__(
        self,
        registry: ParserRegistry,
        walker: XmlWalker | None = None,
    ) -> None:


        self.registry = registry


        self.walker = (
            walker
            or XmlWalker()
        )


        self.statistics = (
            DispatcherStatistics()
        )



    # -------------------------------------------------------------------------
    # Main parse entry
    # -------------------------------------------------------------------------


    def parse(
        self,
        root,
        context: ParserContext,
    ) -> DispatcherStatistics:
        """
        Parse XML tree.

        """

        self.statistics = (
            DispatcherStatistics()
        )


        #
        # Initialize parsers
        #
        self._initialize(
            context
        )


        #
        # Walk XML
        #
        for node in self.walker.walk(
            root
        ):

            self._dispatch(
                node,
                context,
            )


        #
        # Finalize
        #
        self._finalize(
            context
        )


        return self.statistics



    # -------------------------------------------------------------------------
    # Dispatch node
    # -------------------------------------------------------------------------


    def _dispatch(
        self,
        node: XmlNode,
        context: ParserContext,
    ) -> None:
        """
        Execute matching parsers.
        """

        self.statistics.nodes_processed += 1


        parsers = self.registry.find(
            node
        )


        if not parsers:

            self.statistics.skipped += 1

            return



        for parser in parsers:


            self.statistics.parser_calls += 1


            self._execute_parser(
                parser,
                node,
                context,
            )



    # -------------------------------------------------------------------------
    # Parser execution
    # -------------------------------------------------------------------------


    def _execute_parser(
        self,
        parser: Parser,
        node: XmlNode,
        context: ParserContext,
    ) -> None:
        """
        Execute one parser safely.
        """

        try:

            result = parser.parse(
                node,
                context.workspace,
                context.diagnostics,
            )


            if result:

                parser.success()

                self.statistics.successful += 1


            else:

                parser.failure()

                self.statistics.failed += 1



        except Exception as exc:


            parser.failure()


            self.statistics.failed += 1


            context.error(
                f"{parser.name} failed "
                f"at {node.path}: {exc}"
            )



    # -------------------------------------------------------------------------
    # Lifecycle
    # -------------------------------------------------------------------------


    def _initialize(
        self,
        context: ParserContext,
    ) -> None:
        """
        Initialize all parsers.
        """

        for parser in self.registry:

            parser.initialize(
                context.workspace
            )



    def _finalize(
        self,
        context: ParserContext,
    ) -> None:
        """
        Finalize all parsers.
        """

        for parser in self.registry:

            parser.finalize(
                context.workspace
            )