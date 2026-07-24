"""
autosar_codegen.xml.namespace
=============================

AUTOSAR XML namespace management.

Provides:

- Namespace extraction
- AUTOSAR version detection
- XPath namespace mapping
- Vendor namespace handling

"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from lxml import etree



# ============================================================================
# AUTOSAR Versions
# ============================================================================


class AutosarVersion(str, Enum):
    """
    Supported AUTOSAR versions.
    """

    V4_2_2 = "4.2.2"

    V4_3_1 = "4.3.1"

    V4_4_0 = "4.4.0"

    UNKNOWN = "unknown"



# ============================================================================
# Namespace Information
# ============================================================================


@dataclass(slots=True)
class NamespaceInfo:
    """
    XML namespace information.
    """

    uri: str

    prefix: str | None = None



# ============================================================================
# Namespace Context
# ============================================================================


@dataclass(slots=True)
class NamespaceContext:
    """
    Complete namespace context.
    """

    autosar_version: AutosarVersion

    namespaces: dict[str, str] = field(
        default_factory=dict
    )


    def xpath_map(
        self,
    ) -> dict[str, str]:
        """
        Namespace map for XPath.

        Example:

            autosar:AR-PACKAGE

        """

        return self.namespaces.copy()



# ============================================================================
# Namespace Manager
# ============================================================================


class NamespaceManager:
    """
    Handles AUTOSAR XML namespaces.

    """

    AUTOSAR_NAMESPACE = (
        "http://autosar.org/schema/r4.0"
    )


    def analyze(
        self,
        root: etree._Element,
    ) -> NamespaceContext:
        """
        Analyze XML root element.
        """

        namespaces = self._extract_namespaces(
            root
        )


        version = self._detect_version(
            root,
            namespaces,
        )


        return NamespaceContext(

            autosar_version=version,

            namespaces=namespaces,

        )



    # -------------------------------------------------------------------------
    # Namespace extraction
    # -------------------------------------------------------------------------


    def _extract_namespaces(
        self,
        root: etree._Element,
    ) -> dict[str, str]:
        """
        Extract namespaces.

        """

        result = {}


        for prefix, uri in root.nsmap.items():


            if prefix is None:

                prefix = "autosar"


            result[prefix] = uri



        #
        # Ensure AUTOSAR namespace exists
        #
        if "autosar" not in result:


            result["autosar"] = (
                self.AUTOSAR_NAMESPACE
            )


        return result



    # -------------------------------------------------------------------------
    # Version detection
    # -------------------------------------------------------------------------


    def _detect_version(
        self,
        root: etree._Element,
        namespaces: dict[str, str],
    ) -> AutosarVersion:
        """
        Detect AUTOSAR version.

        """

        uri = namespaces.get(
            "autosar"
        )


        if uri == self.AUTOSAR_NAMESPACE:


            #
            # AUTOSAR 4.x all use same namespace.
            #
            #
            # Exact version may require
            # schema metadata.
            #

            return AutosarVersion.V4_4_0



        return AutosarVersion.UNKNOWN



    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------


    def qualify(
        self,
        tag: str,
        context: NamespaceContext,
    ) -> str:
        """
        Convert:

            AR-PACKAGE

        into:

            {namespace}AR-PACKAGE
        """

        return (
            "{"
            + context.namespaces["autosar"]
            + "}"
            + tag
        )