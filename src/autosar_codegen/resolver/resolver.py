"""
autosar_codegen.resolver.resolver
=================================

Resolver framework.

Provides the infrastructure for running resolver passes
against the AUTOSAR Intermediate Representation (IR).

Resolvers are executed after parsing and before validation
or code generation.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from threading import RLock
from time import perf_counter
from typing import Iterable

from autosar_codegen.model.workspace import Workspace
from autosar_codegen.core.diagnostics import DiagnosticEngine


# ============================================================================
# Resolver Statistics
# ============================================================================


@dataclass(slots=True)
class ResolverStatistics:
    """
    Resolver execution statistics.
    """

    resolvers_run: int = 0

    successful: int = 0

    failed: int = 0

    execution_time_ms: float = 0.0



# ============================================================================
# Resolver Interface
# ============================================================================


class Resolver(ABC):
    """
    Base resolver interface.

    Every resolver pass derives from this class.

    Example:

        class SignalResolver(Resolver):

            def resolve(self, workspace):
                ...

    """

    name: str = "Resolver"


    def __init__(
        self,
    ) -> None:

        self.enabled = True



    @abstractmethod
    def resolve(
        self,
        workspace: Workspace,
        diagnostics: DiagnosticEngine,
    ) -> bool:
        """
        Execute resolver.

        Returns
        -------
        bool

            True if successful.
        """

        raise NotImplementedError



    def initialize(
        self,
        workspace: Workspace,
    ) -> None:
        """
        Optional initialization hook.
        """



    def finalize(
        self,
        workspace: Workspace,
    ) -> None:
        """
        Optional cleanup hook.
        """



# ============================================================================
# Resolver Manager
# ============================================================================


class ResolverManager:
    """
    Executes resolver passes.

    Controls:

    - Resolver order
    - Execution lifecycle
    - Statistics
    - Error handling
    """

    def __init__(
        self,
        diagnostics: DiagnosticEngine,
    ) -> None:

        self._diagnostics = diagnostics

        self._resolvers: list[Resolver] = []

        self._statistics = ResolverStatistics()

        self._lock = RLock()



    # -------------------------------------------------------------------------
    # Registration
    # -------------------------------------------------------------------------


    def register(
        self,
        resolver: Resolver,
    ) -> None:
        """
        Register resolver pass.
        """

        with self._lock:

            self._resolvers.append(
                resolver
            )



    def unregister(
        self,
        resolver: Resolver,
    ) -> None:
        """
        Remove resolver.
        """

        with self._lock:

            self._resolvers.remove(
                resolver
            )



    # -------------------------------------------------------------------------
    # Execution
    # -------------------------------------------------------------------------


    def resolve(
        self,
        workspace: Workspace,
    ) -> bool:
        """
        Execute all resolver passes.
        """

        start = perf_counter()

        success = True


        for resolver in self._resolvers:


            if not resolver.enabled:

                continue


            self._statistics.resolvers_run += 1


            try:

                resolver.initialize(
                    workspace
                )


                result = resolver.resolve(
                    workspace,
                    self._diagnostics,
                )


                resolver.finalize(
                    workspace
                )


                if result:

                    self._statistics.successful += 1

                else:

                    self._statistics.failed += 1

                    success = False



            except Exception as exc:


                self._statistics.failed += 1

                success = False


                self._diagnostics.error(
                    f"Resolver '{resolver.name}' failed: {exc}"
                )



        elapsed = (
            perf_counter() - start
        ) * 1000


        self._statistics.execution_time_ms += elapsed


        return success



    # -------------------------------------------------------------------------
    # Information
    # -------------------------------------------------------------------------


    @property
    def statistics(
        self,
    ) -> ResolverStatistics:
        """
        Return resolver statistics.
        """

        return self._statistics



    def __iter__(
        self,
    ) -> Iterable[Resolver]:

        return iter(
            self._resolvers
        )