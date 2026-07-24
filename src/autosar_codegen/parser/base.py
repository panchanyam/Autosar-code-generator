"""
autosar_codegen.parser.base
===========================

Base parser framework for AUTOSAR ARXML parsing.

All AUTOSAR object parsers inherit from this module.

Examples:

    PackageParser
    SignalParser
    PduParser

"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Iterable

from autosar_codegen.xml.walker import XmlNode
from autosar_codegen.model.workspace import Workspace
from autosar_codegen.core.diagnostics import DiagnosticEngine



# ============================================================================
# Parser Metadata
# ============================================================================


@dataclass(slots=True)
class ParserMetadata:
    """
    Parser identification information.
    """

    name: str

    version: str = "1.0.0"

    description: str = ""

    supported_tags: tuple[str, ...] = ()

    priority: int = 100



# ============================================================================
# Parser Statistics
# ============================================================================


@dataclass(slots=True)
class ParserStatistics:
    """
    Parser execution statistics.
    """

    processed: int = 0

    created: int = 0

    failed: int = 0



# ============================================================================
# Parser Base Class
# ============================================================================


class Parser(ABC):
    """
    Abstract AUTOSAR parser.

    Every parser converts XML nodes into model objects.

    """

    metadata = ParserMetadata(
        name="BaseParser"
    )


    def __init__(
        self,
    ) -> None:


        self.enabled = True

        self.statistics = ParserStatistics()



    # -------------------------------------------------------------------------
    # Identification
    # -------------------------------------------------------------------------


    @property
    def name(
        self,
    ) -> str:
        """
        Parser name.
        """

        return self.metadata.name



    @property
    def priority(
        self,
    ) -> int:
        """
        Parser execution priority.
        """

        return self.metadata.priority



    # -------------------------------------------------------------------------
    # Matching
    # -------------------------------------------------------------------------


    def can_parse(
        self,
        node: XmlNode,
    ) -> bool:
        """
        Check whether parser supports XML node.
        """

        return (
            node.tag
            in
            self.metadata.supported_tags
        )



    # -------------------------------------------------------------------------
    # Lifecycle
    # -------------------------------------------------------------------------


    def initialize(
        self,
        workspace: Workspace,
    ) -> None:
        """
        Initialization hook.
        """



    @abstractmethod
    def parse(
        self,
        node: XmlNode,
        workspace: Workspace,
        diagnostics: DiagnosticEngine,
    ) -> bool:
        """
        Parse XML node.

        Returns:

            True  -> success
            False -> failure
        """

        raise NotImplementedError



    def finalize(
        self,
        workspace: Workspace,
    ) -> None:
        """
        Finalization hook.
        """



    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------


    def success(
        self,
    ) -> None:
        """
        Record successful parse.
        """

        self.statistics.processed += 1

        self.statistics.created += 1



    def failure(
        self,
    ) -> None:
        """
        Record failed parse.
        """

        self.statistics.processed += 1

        self.statistics.failed += 1