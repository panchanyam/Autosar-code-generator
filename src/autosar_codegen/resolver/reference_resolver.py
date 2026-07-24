"""
autosar_codegen.resolver.reference_resolver
===========================================

AUTOSAR reference resolution pass.

Converts:

    AutosarReference(path="/DataTypes/UInt16")

into:

    AutosarReference(
        path="/DataTypes/UInt16",
        resolved=ImplementationDataType(...)
    )

Also updates the dependency graph.
"""

from __future__ import annotations

from dataclasses import dataclass

from autosar_codegen.model.workspace import Workspace
from autosar_codegen.model.reference import AutosarReference
from autosar_codegen.model.base import AutosarElement

from autosar_codegen.resolver.resolver import Resolver
from autosar_codegen.core.diagnostics import DiagnosticEngine


# ============================================================================
# Statistics
# ============================================================================


@dataclass(slots=True)
class ReferenceResolverStatistics:
    """
    Reference resolution statistics.
    """

    total_references: int = 0

    resolved: int = 0

    unresolved: int = 0



# ============================================================================
# Reference Resolver
# ============================================================================


class ReferenceResolver(Resolver):
    """
    Resolves AUTOSAR references.

    """

    name = "ReferenceResolver"


    def __init__(self):

        super().__init__()

        self.statistics = ReferenceResolverStatistics()



    # -------------------------------------------------------------------------

    def resolve(
        self,
        workspace: Workspace,
        diagnostics: DiagnosticEngine,
    ) -> bool:
        """
        Resolve all references.
        """

        success = True


        for element in workspace.walk():


            references = self._collect_references(
                element
            )


            for reference in references:

                self.statistics.total_references += 1


                if self._resolve_reference(
                    element,
                    reference,
                    workspace,
                    diagnostics,
                ):

                    self.statistics.resolved += 1


                else:

                    self.statistics.unresolved += 1

                    success = False



        return success



    # -------------------------------------------------------------------------

    def _collect_references(
        self,
        element: AutosarElement,
    ) -> list[AutosarReference]:
        """
        Collect references from object.

        Searches object attributes recursively.

        """

        result = []


        for value in vars(element).values():


            if isinstance(
                value,
                AutosarReference,
            ):

                result.append(value)



            elif isinstance(
                value,
                list,
            ):

                for item in value:

                    if isinstance(
                        item,
                        AutosarReference,
                    ):

                        result.append(item)



        return result



    # -------------------------------------------------------------------------

    def _resolve_reference(
        self,
        source: AutosarElement,
        reference: AutosarReference,
        workspace: Workspace,
        diagnostics: DiagnosticEngine,
    ) -> bool:
        """
        Resolve one reference.
        """

        if workspace.symbol_table is None:


            diagnostics.error(
                "SymbolTable not available during reference resolution"
            )

            return False



        target = workspace.symbol_table.find(
            reference.path
        )


        if target is None:


            diagnostics.error(
                f"Unresolved AUTOSAR reference: "
                f"{reference.path}"
            )


            return False



        reference.bind(
            target
        )


        #
        # Update dependency graph
        #
        if hasattr(
            workspace,
            "reference_graph",
        ):

            workspace.reference_graph.add_dependency(
                source,
                target,
            )


        return True