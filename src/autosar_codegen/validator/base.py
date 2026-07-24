"""
autosar_codegen.validator.base
==============================

Base validation framework.

Provides common infrastructure for
AUTOSAR model validation.
"""

from __future__ import annotations


from abc import ABC, abstractmethod


from dataclasses import dataclass, field


from enum import Enum


from typing import Any



# ============================================================================
# Validation Severity
# ============================================================================


class ValidationSeverity(Enum):
    """
    Validation message severity.
    """

    INFO = "info"

    WARNING = "warning"

    ERROR = "error"

    FATAL = "fatal"



# ============================================================================
# Validator Metadata
# ============================================================================


@dataclass(frozen=True, slots=True)
class ValidatorMetadata:
    """
    Validator identification.
    """

    name: str

    version: str = "1.0.0"

    description: str = ""

    priority: int = 100



# ============================================================================
# Validation Message
# ============================================================================


@dataclass(slots=True)
class ValidationMessage:
    """
    Validation result message.
    """

    severity: ValidationSeverity

    message: str

    validator: str = ""

    object_name: str | None = None

    code: str | None = None



# ============================================================================
# Validation Statistics
# ============================================================================


@dataclass(slots=True)
class ValidationStatistics:
    """
    Validation execution statistics.
    """

    processed: int = 0

    passed: int = 0

    warnings: int = 0

    errors: int = 0



# ============================================================================
# Validation Context
# ============================================================================


@dataclass(slots=True)
class ValidationContext:
    """
    Shared validation environment.
    """

    workspace: Any


    messages: list[ValidationMessage] = field(

        default_factory=list

    )


    metadata: dict[str, Any] = field(

        default_factory=dict

    )


    def add_message(
        self,
        severity: ValidationSeverity,
        message: str,
        validator: str = "",
        object_name: str | None = None,
        code: str | None = None,
    ) -> None:
        """
        Add validation result.
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



    def error(
        self,
        message: str,
        **kwargs,
    ) -> None:
        """
        Add error.
        """

        self.add_message(

            ValidationSeverity.ERROR,

            message,

            **kwargs

        )



    def warning(
        self,
        message: str,
        **kwargs,
    ) -> None:
        """
        Add warning.
        """

        self.add_message(

            ValidationSeverity.WARNING,

            message,

            **kwargs

        )



# ============================================================================
# Validator Base
# ============================================================================


class Validator(ABC):
    """
    Abstract AUTOSAR validator.

    Implementations:

        DatatypeValidator
        SignalValidator
        NetworkValidator
    """


    metadata = ValidatorMetadata(

        name="BaseValidator"

    )


    def __init__(
        self,
    ) -> None:


        self.statistics = ValidationStatistics()


        self.enabled = True



    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------


    @property
    def name(
        self,
    ) -> str:
        """
        Validator name.
        """

        return self.metadata.name



    @property
    def priority(
        self,
    ) -> int:
        """
        Execution priority.
        """

        return self.metadata.priority



    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------


    def initialize(
        self,
        context: ValidationContext,
    ) -> None:
        """
        Initialization hook.
        """



    @abstractmethod
    def validate(
        self,
        context: ValidationContext,
    ) -> bool:
        """
        Execute validation.

        Returns:

            True  validation successful

            False validation failed
        """

        raise NotImplementedError



    def finalize(
        self,
        context: ValidationContext,
    ) -> None:
        """
        Finalization hook.
        """



    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------


    def processed(
        self,
    ) -> None:
        """
        Increment processed count.
        """

        self.statistics.processed += 1



    def passed(
        self,
    ) -> None:
        """
        Increment passed count.
        """

        self.statistics.passed += 1



    def failed(
        self,
    ) -> None:
        """
        Increment error count.
        """

        self.statistics.errors += 1
        