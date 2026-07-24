"""
autosar_codegen.core.diagnostics
================================

Diagnostic infrastructure for the AUTOSAR Code Generator.

This module provides immutable diagnostic objects, source location
tracking, severity levels, categories and statistics used throughout
the framework.

All parser, resolver, validator and generator components report
problems through this API.

The DiagnosticEngine implementation is provided in Part 2.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional


# ============================================================================
# Severity
# ============================================================================


class DiagnosticSeverity(str, Enum):
    """
    Diagnostic severity.

    Ordered from lowest to highest severity.
    """

    INFO = "INFO"

    HINT = "HINT"

    WARNING = "WARNING"

    ERROR = "ERROR"

    FATAL = "FATAL"


# ============================================================================
# Category
# ============================================================================


class DiagnosticCategory(str, Enum):
    """
    Diagnostic category.

    Allows filtering diagnostics by subsystem.
    """

    GENERAL = "GENERAL"

    CONFIGURATION = "CONFIGURATION"

    XML = "XML"

    PARSER = "PARSER"

    RESOLVER = "RESOLVER"

    VALIDATION = "VALIDATION"

    GENERATOR = "GENERATOR"

    SIMULATOR = "SIMULATOR"

    NETWORK = "NETWORK"

    SIGNAL = "SIGNAL"

    PDU = "PDU"

    FRAME = "FRAME"

    DATATYPE = "DATATYPE"


# ============================================================================
# Source Location
# ============================================================================


@dataclass(slots=True, frozen=True)
class SourceLocation:
    """
    Source code location.

    Attributes
    ----------
    file:
        ARXML file.

    line:
        Line number.

    column:
        Column number.
    """

    file: Optional[Path] = None

    line: Optional[int] = None

    column: Optional[int] = None

    @property
    def has_location(self) -> bool:
        """
        True if file information is available.
        """
        return self.file is not None

    def __str__(self) -> str:
        if self.file is None:
            return "<unknown>"

        if self.line is None:
            return str(self.file)

        if self.column is None:
            return f"{self.file}:{self.line}"

        return f"{self.file}:{self.line}:{self.column}"


# ============================================================================
# Diagnostic
# ============================================================================


@dataclass(slots=True, frozen=True)
class Diagnostic:
    """
    Immutable diagnostic object.

    Parameters
    ----------
    severity
        Diagnostic severity.

    category
        Diagnostic category.

    message
        Human readable description.

    location
        Source location.

    code
        Internal diagnostic code.

    symbol
        AUTOSAR object name.

    reference
        AUTOSAR reference path.
    """

    severity: DiagnosticSeverity

    category: DiagnosticCategory

    message: str

    location: SourceLocation = SourceLocation()

    code: Optional[str] = None

    symbol: Optional[str] = None

    reference: Optional[str] = None

    @property
    def is_error(self) -> bool:
        return self.severity in (
            DiagnosticSeverity.ERROR,
            DiagnosticSeverity.FATAL,
        )

    @property
    def is_warning(self) -> bool:
        return self.severity == DiagnosticSeverity.WARNING

    @property
    def is_info(self) -> bool:
        return self.severity == DiagnosticSeverity.INFO

    @property
    def is_hint(self) -> bool:
        return self.severity == DiagnosticSeverity.HINT

    def __str__(self) -> str:

        text = f"[{self.severity}] {self.message}"

        if self.symbol:
            text += f" ({self.symbol})"

        if self.location.has_location:
            text += f" @ {self.location}"

        return text


# ============================================================================
# Statistics
# ============================================================================


@dataclass(slots=True)
class DiagnosticStatistics:
    """
    Running diagnostic statistics.

    Updated by DiagnosticEngine.
    """

    infos: int = 0

    hints: int = 0

    warnings: int = 0

    errors: int = 0

    fatals: int = 0

    def clear(self) -> None:
        """
        Reset counters.
        """

        self.infos = 0
        self.hints = 0
        self.warnings = 0
        self.errors = 0
        self.fatals = 0

    @property
    def total(self) -> int:
        """
        Total diagnostics.
        """
        return (
            self.infos
            + self.hints
            + self.warnings
            + self.errors
            + self.fatals
        )

    @property
    def has_errors(self) -> bool:
        """
        True if any error/fatal exists.
        """
        return (self.errors + self.fatals) > 0

    def update(self, diagnostic: Diagnostic) -> None:
        """
        Update counters.
        """

        match diagnostic.severity:

            case DiagnosticSeverity.INFO:
                self.infos += 1

            case DiagnosticSeverity.HINT:
                self.hints += 1

            case DiagnosticSeverity.WARNING:
                self.warnings += 1

            case DiagnosticSeverity.ERROR:
                self.errors += 1

            case DiagnosticSeverity.FATAL:
                self.fatals += 1

    def as_dict(self) -> dict[str, int]:
        """
        Export statistics.
        """

        return {
            "info": self.infos,
            "hint": self.hints,
            "warning": self.warnings,
            "error": self.errors,
            "fatal": self.fatals,
            "total": self.total,
        }

# ============================================================================
# Diagnostic Engine
# ============================================================================

from threading import RLock
from typing import Iterable


class DiagnosticEngine:
    """
    Central diagnostics manager.

    Collects diagnostics from every subsystem of the framework.

    The engine is intentionally thread-safe because future parser
    implementations may parse multiple ARXML files concurrently.
    """

    def __init__(self) -> None:

        self._diagnostics: list[Diagnostic] = []

        self._statistics = DiagnosticStatistics()

        self._lock = RLock()

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _add(self, diagnostic: Diagnostic) -> None:
        """
        Add a diagnostic.

        Parameters
        ----------
        diagnostic
            Diagnostic object.
        """

        with self._lock:

            self._diagnostics.append(diagnostic)

            self._statistics.update(diagnostic)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def info(
        self,
        message: str,
        *,
        category: DiagnosticCategory = DiagnosticCategory.GENERAL,
        location: SourceLocation = SourceLocation(),
        code: str | None = None,
        symbol: str | None = None,
        reference: str | None = None,
    ) -> None:

        self._add(
            Diagnostic(
                severity=DiagnosticSeverity.INFO,
                category=category,
                message=message,
                location=location,
                code=code,
                symbol=symbol,
                reference=reference,
            )
        )

    def hint(
        self,
        message: str,
        *,
        category: DiagnosticCategory = DiagnosticCategory.GENERAL,
        location: SourceLocation = SourceLocation(),
        code: str | None = None,
        symbol: str | None = None,
        reference: str | None = None,
    ) -> None:

        self._add(
            Diagnostic(
                severity=DiagnosticSeverity.HINT,
                category=category,
                message=message,
                location=location,
                code=code,
                symbol=symbol,
                reference=reference,
            )
        )

    def warning(
        self,
        message: str,
        *,
        category: DiagnosticCategory = DiagnosticCategory.GENERAL,
        location: SourceLocation = SourceLocation(),
        code: str | None = None,
        symbol: str | None = None,
        reference: str | None = None,
    ) -> None:

        self._add(
            Diagnostic(
                severity=DiagnosticSeverity.WARNING,
                category=category,
                message=message,
                location=location,
                code=code,
                symbol=symbol,
                reference=reference,
            )
        )

    def error(
        self,
        message: str,
        *,
        category: DiagnosticCategory = DiagnosticCategory.GENERAL,
        location: SourceLocation = SourceLocation(),
        code: str | None = None,
        symbol: str | None = None,
        reference: str | None = None,
    ) -> None:

        self._add(
            Diagnostic(
                severity=DiagnosticSeverity.ERROR,
                category=category,
                message=message,
                location=location,
                code=code,
                symbol=symbol,
                reference=reference,
            )
        )

    def fatal(
        self,
        message: str,
        *,
        category: DiagnosticCategory = DiagnosticCategory.GENERAL,
        location: SourceLocation = SourceLocation(),
        code: str | None = None,
        symbol: str | None = None,
        reference: str | None = None,
    ) -> None:

        self._add(
            Diagnostic(
                severity=DiagnosticSeverity.FATAL,
                category=category,
                message=message,
                location=location,
                code=code,
                symbol=symbol,
                reference=reference,
            )
        )

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    @property
    def diagnostics(self) -> tuple[Diagnostic, ...]:
        """
        Return an immutable view of diagnostics.
        """
        return tuple(self._diagnostics)

    @property
    def statistics(self) -> DiagnosticStatistics:
        """
        Return current statistics.
        """
        return self._statistics

    def has_errors(self) -> bool:
        """
        True if any error or fatal exists.
        """
        return self._statistics.has_errors

    def clear(self) -> None:
        """
        Clear diagnostics and statistics.
        """
        with self._lock:

            self._diagnostics.clear()

            self._statistics.clear()

    def by_severity(
        self,
        severity: DiagnosticSeverity,
    ) -> list[Diagnostic]:
        """
        Return diagnostics matching a severity.
        """
        return [
            diagnostic
            for diagnostic in self._diagnostics
            if diagnostic.severity == severity
        ]

    def by_category(
        self,
        category: DiagnosticCategory,
    ) -> list[Diagnostic]:
        """
        Return diagnostics matching a category.
        """
        return [
            diagnostic
            for diagnostic in self._diagnostics
            if diagnostic.category == category
        ]

    def find_symbol(
        self,
        symbol: str,
    ) -> list[Diagnostic]:
        """
        Return diagnostics for a symbol.
        """
        return [
            diagnostic
            for diagnostic in self._diagnostics
            if diagnostic.symbol == symbol
        ]

    def __len__(self) -> int:
        return len(self._diagnostics)

    def __iter__(self) -> Iterable[Diagnostic]:
        return iter(self._diagnostics)