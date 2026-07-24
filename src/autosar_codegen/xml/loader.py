"""
autosar_codegen.xml.loader
==========================

AUTOSAR XML document loader.

Provides:

- Single ARXML file loading
- Multiple ARXML loading
- Source location tracking
- XML parser configuration
- Diagnostic integration

Uses lxml because AUTOSAR ARXML requires:

- XPath support
- Namespace handling
- Line number tracking
- Large XML support

"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from lxml import etree

from autosar_codegen.core.diagnostics import DiagnosticEngine



# ============================================================================
# XML Source Information
# ============================================================================


@dataclass(slots=True)
class XmlSource:
    """
    Information about the XML source file.
    """

    path: Path

    size: int = 0

    encoding: str | None = None



# ============================================================================
# XML Document
# ============================================================================


@dataclass(slots=True)
class XmlDocument:
    """
    Loaded AUTOSAR XML document.

    Wraps lxml tree and source metadata.
    """

    tree: etree._ElementTree

    source: XmlSource


    @property
    def root(
        self,
    ) -> etree._Element:
        """
        Return XML root element.
        """

        return self.tree.getroot()



    def xpath(
        self,
        expression: str,
        namespaces: dict[str, str] | None = None,
    ):
        """
        Execute XPath query.
        """

        return self.tree.xpath(
            expression,
            namespaces=namespaces,
        )



# ============================================================================
# Loader Configuration
# ============================================================================


@dataclass(slots=True)
class XmlLoaderConfig:
    """
    XML parser configuration.
    """

    recover: bool = False

    remove_comments: bool = True

    huge_tree: bool = True

    resolve_entities: bool = False

    no_network: bool = True



# ============================================================================
# XML Loader
# ============================================================================


class XmlLoader:
    """
    AUTOSAR ARXML loader.

    Example:

        loader = XmlLoader()

        document = loader.load_file(
            "Vehicle.arxml"
        )

    """

    def __init__(
        self,
        config: XmlLoaderConfig | None = None,
        diagnostics: DiagnosticEngine | None = None,
    ) -> None:


        self.config = (
            config
            or XmlLoaderConfig()
        )


        self.diagnostics = diagnostics



    # -------------------------------------------------------------------------
    # Parser creation
    # -------------------------------------------------------------------------


    def _create_parser(
        self,
    ) -> etree.XMLParser:
        """
        Create lxml parser.
        """

        return etree.XMLParser(

            recover=self.config.recover,

            remove_comments=self.config.remove_comments,

            huge_tree=self.config.huge_tree,

            resolve_entities=self.config.resolve_entities,

            no_network=self.config.no_network,

        )



    # -------------------------------------------------------------------------
    # Single file loading
    # -------------------------------------------------------------------------


    def load_file(
        self,
        path: str | Path,
    ) -> XmlDocument | None:
        """
        Load one ARXML file.
        """

        file_path = Path(path)


        if not file_path.exists():

            self._error(
                f"ARXML file not found: {file_path}"
            )

            return None



        try:

            parser = self._create_parser()


            tree = etree.parse(
                str(file_path),
                parser,
            )


            source = XmlSource(

                path=file_path,

                size=file_path.stat().st_size,

                encoding=tree.docinfo.encoding,

            )


            return XmlDocument(
                tree=tree,
                source=source,
            )


        except etree.XMLSyntaxError as exc:


            self._error(
                f"XML syntax error in {file_path}: {exc}"
            )


        except Exception as exc:


            self._error(
                f"Failed loading {file_path}: {exc}"
            )


        return None



    # -------------------------------------------------------------------------
    # Multiple files
    # -------------------------------------------------------------------------


    def load_files(
        self,
        paths: Iterable[str | Path],
    ) -> list[XmlDocument]:
        """
        Load multiple ARXML files.
        """

        documents: list[XmlDocument] = []


        for path in paths:

            document = self.load_file(
                path
            )


            if document:

                documents.append(
                    document
                )


        return documents



    # -------------------------------------------------------------------------
    # Diagnostics helper
    # -------------------------------------------------------------------------


    def _error(
        self,
        message: str,
    ) -> None:
        """
        Report error.
        """

        if self.diagnostics:

            self.diagnostics.error(
                message
            )