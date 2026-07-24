"""
autosar_codegen.resolver.base
=============================

Base resolver framework for AUTOSAR references.

Resolvers convert unresolved references
into linked model objects.

"""

from __future__ import annotations


from abc import ABC, abstractmethod

from dataclasses import dataclass



# ============================================================================
# Resolver Metadata
# ============================================================================


@dataclass(frozen=True, slots=True)
class ResolverMetadata:
    """
    Resolver identification information.
    """

    name: str

    version: str = "1.0.0"

    description: str = ""

    priority: int = 100

    dependencies: tuple[str, ...] = ()



# ============================================================================
# Resolver Statistics
# ============================================================================


@dataclass(slots=True)
class ResolverStatistics:
    """
    Resolver execution statistics.
    """

    processed: int = 0

    resolved: int = 0

    failed: int = 0



# ============================================================================
# Resolver Base
# ============================================================================


class Resolver(ABC):
    """
    Abstract AUTOSAR resolver.

    Example:

        DatatypeResolver
        SignalResolver
        PduResolver

    """

    metadata = ResolverMetadata(
        name="BaseResolver"
    )


    def __init__(
        self,
    ) -> None:


        self.statistics = (
            ResolverStatistics()
        )


        self.enabled = True



    # ---------------------------------------------------------------------
    # Properties
    # ---------------------------------------------------------------------


    @property
    def name(
        self,
    ) -> str:
        """
        Resolver name.
        """

        return self.metadata.name



    @property
    def priority(
        self,
    ) -> int:
        """
        Resolver execution priority.
        """

        return self.metadata.priority



    @property
    def dependencies(
        self,
    ) -> tuple[str, ...]:
        """
        Resolver dependencies.
        """

        return self.metadata.dependencies



    # ---------------------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------------------


    def initialize(
        self,
        context,
    ) -> None:
        """
        Initialization hook.
        """



    @abstractmethod
    def resolve(
        self,
        context,
    ) -> bool:
        """
        Execute resolution.

        Returns:

            True  success
            False failure
        """

        raise NotImplementedError



    def finalize(
        self,
        context,
    ) -> None:
        """
        Finalization hook.
        """



    # ---------------------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------------------


    def success(
        self,
    ) -> None:
        """
        Record successful resolution.
        """

        self.statistics.processed += 1

        self.statistics.resolved += 1



    def failure(
        self,
    ) -> None:
        """
        Record failed resolution.
        """

        self.statistics.processed += 1

        self.statistics.failed += 1