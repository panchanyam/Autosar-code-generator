"""
autosar_codegen.validator.dispatcher
====================================

Validator execution engine.

Runs registered AUTOSAR validation rules.
"""

from __future__ import annotations


from dataclasses import dataclass


from autosar_codegen.validator.registry import (
    ValidatorRegistry,
)


from autosar_codegen.validator.context import (
    ValidationContext,
)



# ============================================================================
# Dispatcher Statistics
# ============================================================================


@dataclass(slots=True)
class DispatcherStatistics:
    """
    Validator dispatcher statistics.
    """

    validators_executed: int = 0

    successful: int = 0

    failed: int = 0



# ============================================================================
# Validator Dispatcher
# ============================================================================


class ValidatorDispatcher:
    """
    Executes validator plugins.
    """


    def __init__(
        self,
        registry: ValidatorRegistry,
    ) -> None:

        self.registry = registry

        self.statistics = DispatcherStatistics()



    # ------------------------------------------------------------------
    # Execute Validation
    # ------------------------------------------------------------------


    def validate(
        self,
        context: ValidationContext,
    ) -> DispatcherStatistics:
        """
        Execute all registered validators.

        Returns:
            DispatcherStatistics
        """

        self.statistics = DispatcherStatistics()



        validators = self.registry.all()



        self._initialize(
            validators,
            context
        )



        for validator in validators:

            self._execute(

                validator,

                context

            )



        self._finalize(

            validators,

            context

        )



        return self.statistics



    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------


    def _execute(
        self,
        validator,
        context,
    ) -> None:
        """
        Execute single validator.
        """

        if not validator.enabled:

            return



        #
        # Check rule suppression
        #
        if not context.is_enabled(

            validator.name

        ):

            return



        self.statistics.validators_executed += 1



        try:

            result = validator.validate(

                context

            )


            if result:

                validator.passed()

                self.statistics.successful += 1


            else:

                validator.failed()

                self.statistics.failed += 1



        except Exception as exc:


            validator.failed()


            self.statistics.failed += 1



            context.error(

                f"Validator '{validator.name}' failed: {exc}",

                validator=validator.name,

            )



    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------


    def _initialize(
        self,
        validators,
        context,
    ) -> None:
        """
        Initialize validators.
        """

        for validator in validators:

            validator.initialize(

                context

            )



    def _finalize(
        self,
        validators,
        context,
    ) -> None:
        """
        Finalize validators.
        """

        for validator in validators:

            validator.finalize(

                context

            )



    # ------------------------------------------------------------------
    # Result
    # ------------------------------------------------------------------


    def is_valid(
        self,
        context: ValidationContext,
    ) -> bool:
        """
        Check validation result.

        Returns:

            True  no errors

            False validation failed
        """

        return not context.has_errors()