"""
autosar_codegen.resolver.validation
===================================

AUTOSAR model validation after reference resolution.

Checks model integrity before generation.
"""

from __future__ import annotations

from dataclasses import dataclass

from autosar_codegen.model.workspace import Workspace
from autosar_codegen.model.base import AutosarElement

from autosar_codegen.core.diagnostics import DiagnosticEngine



# ============================================================================
# Statistics
# ============================================================================


@dataclass(slots=True)
class ValidationStatistics:
    """
    Validation results.
    """

    checks: int = 0

    errors: int = 0

    warnings: int = 0



# ============================================================================
# Validator
# ============================================================================


class WorkspaceValidator:
    """
    Validates AUTOSAR workspace.

    """

    def __init__(
        self,
    ):

        self.statistics = ValidationStatistics()



    # -------------------------------------------------------------------------

    def validate(
        self,
        workspace: Workspace,
        diagnostics: DiagnosticEngine,
    ) -> bool:
        """
        Run all validations.
        """

        result = True


        checks = [

            self.validate_references,

            self.validate_duplicates,

            self.validate_graph,

        ]


        for check in checks:


            self.statistics.checks += 1


            if not check(
                workspace,
                diagnostics,
            ):

                result = False



        return result



    # -------------------------------------------------------------------------
    # Reference Validation
    # -------------------------------------------------------------------------


    def validate_references(
        self,
        workspace: Workspace,
        diagnostics: DiagnosticEngine,
    ) -> bool:

        success = True


        for element in workspace.walk():


            for value in vars(element).values():


                if hasattr(
                    value,
                    "is_resolved",
                ):


                    if not value.is_resolved:


                        diagnostics.error(
                            f"Unresolved reference: "
                            f"{value.path}"
                        )


                        self.statistics.errors += 1

                        success = False



        return success



    # -------------------------------------------------------------------------
    # Duplicate Validation
    # -------------------------------------------------------------------------


    def validate_duplicates(
        self,
        workspace: Workspace,
        diagnostics: DiagnosticEngine,
    ) -> bool:
        """
        Validate symbol uniqueness.
        """

        if workspace.symbol_table is None:

            return True



        stats = workspace.symbol_table.statistics()


        #
        # UUID and path counts should match
        #
        if stats.paths != stats.objects:


            diagnostics.warning(
                "Symbol table object count mismatch"
            )


            self.statistics.warnings += 1



        return True



    # -------------------------------------------------------------------------
    # Graph Validation
    # -------------------------------------------------------------------------


    def validate_graph(
        self,
        workspace: Workspace,
        diagnostics: DiagnosticEngine,
    ) -> bool:

        graph = getattr(
            workspace,
            "reference_graph",
            None,
        )


        if graph is None:

            return True



        #
        # Future extension:
        # cycle detection
        # orphan detection
        #

        return True