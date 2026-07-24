"""
autosar_codegen.validator.context
=================================

Validation execution context.

Provides shared state and reporting
services for validators.
"""

from __future__ import annotations


from dataclasses import dataclass, field


from typing import Any


from autosar_codegen.validator.base import (
    ValidationMessage,
    ValidationSeverity,
)



# ============================================================================
# Validation Summary
# ============================================================================


@dataclass(slots=True)
class ValidationSummary:
    """
    Validation result summary.
    """

    total: int = 0

    info: int = 0

    warnings: int = 0

    errors: int = 0

    fatal: int = 0



# ============================================================================
# Validation Context
# ============================================================================


@dataclass(slots=True)
class ValidationContext:
    """
    Runtime environment for validation.
    """

    workspace: Any


    messages: list[ValidationMessage] = field(

        default_factory=list

    )


    metadata: dict[str, Any] = field(

        default_factory=dict

    )


    disabled_rules: set[str] = field(

        default_factory=set

    )


    # ------------------------------------------------------------------
    # Message Handling
    # ------------------------------------------------------------------


    def add(
        self,
        severity: ValidationSeverity,
        message: str,
        validator: str = "",
        object_name: str | None = None,
        code: str | None = None,
    ) -> None:
        """
        Add validation message.
        """

        self.messages.append(

            ValidationMessage(

                severity=severity,

                message=message,

                validator=validator,

                object_name=object_name,

                code=code,

            )

        )



    def info(
        self,
        message: str,
        **kwargs,
    ) -> None:
        """
        Add information message.
        """

        self.add(

            ValidationSeverity.INFO,

            message,

            **kwargs

        )



    def warning(
        self,
        message: str,
        **kwargs,
    ) -> None:
        """
        Add warning message.
        """

        self.add(

            ValidationSeverity.WARNING,

            message,

            **kwargs

        )



    def error(
        self,
        message: str,
        **kwargs,
    ) -> None:
        """
        Add error message.
        """

        self.add(

            ValidationSeverity.ERROR,

            message,

            **kwargs

        )



    def fatal(
        self,
        message: str,
        **kwargs,
    ) -> None:
        """
        Add fatal message.
        """

        self.add(

            ValidationSeverity.FATAL,

            message,

            **kwargs

        )



    # ------------------------------------------------------------------
    # Rule Control
    # ------------------------------------------------------------------


    def disable_rule(
        self,
        rule_name: str,
    ) -> None:
        """
        Disable validation rule.
        """

        self.disabled_rules.add(

            rule_name

        )



    def enable_rule(
        self,
        rule_name: str,
    ) -> None:
        """
        Enable validation rule.
        """

        self.disabled_rules.discard(

            rule_name

        )



    def is_enabled(
        self,
        rule_name: str,
    ) -> bool:
        """
        Check rule status.
        """

        return (

            rule_name

            not in

            self.disabled_rules

        )



    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------


    def set(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store runtime metadata.
        """

        self.metadata[key] = value



    def get(
        self,
        key: str,
        default=None,
    ):
        """
        Retrieve metadata.
        """

        return self.metadata.get(

            key,

            default

        )



    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------


    def summary(
        self,
    ) -> ValidationSummary:
        """
        Generate validation summary.
        """

        result = ValidationSummary()



        for message in self.messages:


            result.total += 1



            match message.severity:


                case ValidationSeverity.INFO:

                    result.info += 1


                case ValidationSeverity.WARNING:

                    result.warnings += 1


                case ValidationSeverity.ERROR:

                    result.errors += 1


                case ValidationSeverity.FATAL:

                    result.fatal += 1



        return result



    def has_errors(
        self,
    ) -> bool:
        """
        Check if validation failed.
        """

        return any(

            message.severity in (

                ValidationSeverity.ERROR,

                ValidationSeverity.FATAL,

            )

            for message in self.messages

        )



    def clear(
        self,
    ) -> None:
        """
        Clear validation messages.
        """

        self.messages.clear()