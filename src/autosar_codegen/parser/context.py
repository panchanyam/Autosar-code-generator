"""
autosar_codegen.parser.context
==============================

Shared context passed to AUTOSAR parsers.

Contains all services required during parsing.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from autosar_codegen.model.workspace import Workspace

from autosar_codegen.xml.loader import XmlDocument

from autosar_codegen.xml.namespace import (
    NamespaceContext,
)

from autosar_codegen.xml.xpath import (
    XPathEngine,
)

from autosar_codegen.core.diagnostics import (
    DiagnosticEngine,
)

from autosar_codegen.core.config import (
    Config,
)



# ============================================================================
# Parser Context
# ============================================================================


@dataclass(slots=True)
class ParserContext:
    """
    Environment for parser execution.

    """

    workspace: Workspace

    diagnostics: DiagnosticEngine


    #
    # XML related services
    #

    document: XmlDocument | None = None


    namespace: NamespaceContext | None = None


    xpath: XPathEngine | None = None



    #
    # Configuration
    #

    config: Config | None = None



    #
    # Current source file
    #

    source_file: Path | None = None



    #
    # Extension storage
    #

    metadata: dict[str, Any] = field(
        default_factory=dict
    )



    # -------------------------------------------------------------------------
    # XML Helpers
    # -------------------------------------------------------------------------


    def set_document(
        self,
        document: XmlDocument,
        namespace: NamespaceContext,
    ) -> None:
        """
        Attach XML document.

        Creates XPath engine.
        """

        self.document = document

        self.namespace = namespace


        self.xpath = XPathEngine(
            namespace
        )



    # -------------------------------------------------------------------------
    # State Management
    # -------------------------------------------------------------------------


    def set(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store parser state.
        """

        self.metadata[key] = value



    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieve parser state.
        """

        return self.metadata.get(
            key,
            default,
        )



    # -------------------------------------------------------------------------
    # Diagnostics Helpers
    # -------------------------------------------------------------------------


    def error(
        self,
        message: str,
    ) -> None:
        """
        Report parsing error.
        """

        self.diagnostics.error(
            message
        )



    def warning(
        self,
        message: str,
    ) -> None:
        """
        Report warning.
        """

        self.diagnostics.warning(
            message
        )



    # -------------------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------------------


    @property
    def ready(
        self,
    ) -> bool:
        """
        Check whether context is usable.
        """

        return (

            self.workspace is not None

            and

            self.diagnostics is not None

        )