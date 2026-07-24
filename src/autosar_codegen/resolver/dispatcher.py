"""
autosar_codegen.resolver.dispatcher
===================================

Resolver execution engine.

Executes AUTOSAR reference resolvers
in dependency order.
"""

from __future__ import annotations


from dataclasses import dataclass


from autosar_codegen.resolver.registry import (
    ResolverRegistry,
)

from autosar_codegen.resolver.context import (
    ResolverContext,
)

from autosar_codegen.resolver.base import (
    Resolver,
)



# ============================================================================
# Statistics
# ============================================================================


@dataclass(slots=True)
class DispatcherStatistics:
    """
    Resolver dispatcher statistics.
    """

    resolvers_executed: int = 0

    successful: int = 0

    failed: int = 0



# ============================================================================
# Resolver Dispatcher
# ============================================================================


class ResolverDispatcher:
    """
    Executes resolver plugins.
    """


    def __init__(
        self,
        registry: ResolverRegistry,
    ) -> None:

        self.registry = registry


        self.statistics = (
            DispatcherStatistics()
        )



    # ------------------------------------------------------------------
    # Execute
    # ------------------------------------------------------------------


    def resolve(
        self,
        context: ResolverContext,
    ) -> DispatcherStatistics:
        """
        Execute complete resolution pipeline.
        """

        self.statistics = (
            DispatcherStatistics()
        )


        self._initialize(
            context
        )


        for resolver in self.registry.ordered():

            self._execute(
                resolver,
                context,
            )


        self._finalize(
            context
        )


        return self.statistics



    # ------------------------------------------------------------------
    # Execute resolver
    # ------------------------------------------------------------------


    def _execute(
        self,
        resolver: Resolver,
        context: ResolverContext,
    ) -> None:
        """
        Execute single resolver safely.
        """

        if not resolver.enabled:

            return


        self.statistics.resolvers_executed += 1


        try:

            result = resolver.resolve(
                context
            )


            if result:

                resolver.success()

                self.statistics.successful += 1


            else:

                resolver.failure()

                self.statistics.failed += 1



        except Exception as exc:


            resolver.failure()


            self.statistics.failed += 1


            context.error(

                f"{resolver.name} failed: {exc}"

            )



    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------


    def _initialize(
        self,
        context: ResolverContext,
    ) -> None:
        """
        Initialize resolvers.
        """

        for resolver in self.registry.ordered():

            resolver.initialize(
                context
            )



    def _finalize(
        self,
        context: ResolverContext,
    ) -> None:
        """
        Finalize resolvers.
        """

        for resolver in self.registry.ordered():

            resolver.finalize(
                context
            )