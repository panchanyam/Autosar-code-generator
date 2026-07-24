"""
autosar_codegen.generator.dispatcher
====================================

Generator execution engine.

Runs registered code generators.
"""

from __future__ import annotations


from dataclasses import dataclass


from autosar_codegen.generator.registry import (
    GeneratorRegistry,
)


from autosar_codegen.generator.context import (
    GeneratorContext,
)


from autosar_codegen.generator.base import (
    Generator,
)



# ============================================================================
# Statistics
# ============================================================================


@dataclass(slots=True)
class DispatcherStatistics:
    """
    Generator dispatcher statistics.
    """

    generators_executed: int = 0

    successful: int = 0

    failed: int = 0



# ============================================================================
# Generator Dispatcher
# ============================================================================


class GeneratorDispatcher:
    """
    Executes generator plugins.
    """


    def __init__(
        self,
        registry: GeneratorRegistry,
    ) -> None:


        self.registry = registry


        self.statistics = (
            DispatcherStatistics()
        )



    # ------------------------------------------------------------------
    # Generate
    # ------------------------------------------------------------------


    def generate(
        self,
        context: GeneratorContext,
        language: str | None = None,
    ) -> DispatcherStatistics:
        """
        Execute generation pipeline.

        Args:

            context:
                Generator execution context

            language:
                Optional target language filter

        """

        self.statistics = (
            DispatcherStatistics()
        )


        context.initialize()



        generators = (

            self.registry.all()

            if language is None

            else self.registry.get_language(
                language
            )

        )



        self._initialize(
            generators,
            context
        )


        for generator in generators:

            self._execute(

                generator,

                context

            )


        self._finalize(

            generators,

            context

        )


        return self.statistics



    # ------------------------------------------------------------------
    # Execute
    # ------------------------------------------------------------------


    def _execute(
        self,
        generator: Generator,
        context: GeneratorContext,
    ) -> None:
        """
        Execute one generator safely.
        """

        if not generator.enabled:

            return



        self.statistics.generators_executed += 1



        try:

            result = generator.generate(

                context

            )


            if result:


                self.statistics.successful += 1



            else:


                generator.failure()


                self.statistics.failed += 1



        except Exception as exc:


            generator.failure()


            self.statistics.failed += 1



            self._report_error(

                context,

                generator,

                exc

            )



    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------


    def _initialize(
        self,
        generators,
        context,
    ) -> None:
        """
        Initialize generators.
        """

        for generator in generators:

            generator.initialize(
                context
            )



    def _finalize(
        self,
        generators,
        context,
    ) -> None:
        """
        Finalize generators.
        """

        for generator in generators:

            generator.finalize(
                context
            )



    # ------------------------------------------------------------------
    # Error Handling
    # ------------------------------------------------------------------


    def _report_error(
        self,
        context,
        generator,
        error,
    ) -> None:
        """
        Report generator failure.
        """

        if hasattr(
            context,
            "diagnostics"
        ):

            context.diagnostics.error(

                f"{generator.name} failed: {error}"

            )