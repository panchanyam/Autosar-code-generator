"""
autosar_codegen.resolver.context
================================

Shared context for AUTOSAR reference resolution.

Contains services required by resolvers.
"""

from __future__ import annotations


from dataclasses import dataclass, field
from typing import Any


from autosar_codegen.model.workspace import (
    Workspace,
)


from autosar_codegen.core.diagnostics import (
    DiagnosticEngine,
)


from autosar_codegen.core.config import (
    Config,
)



@dataclass(slots=True)
class ResolverContext:
    """
    Environment passed to resolver plugins.
    """


    workspace: Workspace


    diagnostics: DiagnosticEngine



    #
    # Symbol resolution
    #

    symbol_table: Any = None



    #
    # Reference graph
    #

    reference_graph: Any = None



    #
    # Configuration
    #

    config: Config | None = None



    #
    # Resolver shared state
    #

    metadata: dict[str, Any] = field(

        default_factory=dict

    )



    # ------------------------------------------------------------------
    # State management
    # ------------------------------------------------------------------


    def set(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store resolver state.
        """

        self.metadata[key] = value



    def get(
        self,
        key: str,
        default=None,
    ):
        """
        Retrieve resolver state.
        """

        return self.metadata.get(
            key,
            default,
        )



    # ------------------------------------------------------------------
    # Symbol lookup helpers
    # ------------------------------------------------------------------


    def lookup(
        self,
        reference: str,
    ):
        """
        Resolve symbol reference.

        Delegates to symbol table.
        """

        if self.symbol_table is None:

            return None


        return self.symbol_table.lookup(
            reference
        )



    # ------------------------------------------------------------------
    # Diagnostics helpers
    # ------------------------------------------------------------------


    def error(
        self,
        message: str,
    ) -> None:
        """
        Report resolver error.
        """

        self.diagnostics.error(
            message
        )



    def warning(
        self,
        message: str,
    ) -> None:
        """
        Report resolver warning.
        """

        self.diagnostics.warning(
            message
        )



    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------


    @property
    def ready(
        self,
    ) -> bool:
        """
        Check resolver environment.
        """

        return (

            self.workspace is not None

            and

            self.diagnostics is not None

        )