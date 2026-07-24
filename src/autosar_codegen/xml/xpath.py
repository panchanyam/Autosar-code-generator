"""
autosar_codegen.xml.xpath
=========================

AUTOSAR XPath utilities.

Provides a safe abstraction around lxml XPath operations.

"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from lxml import etree

from autosar_codegen.xml.namespace import NamespaceContext



# ============================================================================
# XPath Result
# ============================================================================


@dataclass(slots=True)
class XPathResult:
    """
    XPath execution result.
    """

    nodes: list[Any]

    @property
    def count(self) -> int:
        return len(self.nodes)

    @property
    def empty(self) -> bool:
        return len(self.nodes) == 0



# ============================================================================
# XPath Engine
# ============================================================================


class XPathEngine:
    """
    Namespace-aware XPath executor.

    """

    def __init__(
        self,
        context: NamespaceContext,
    ) -> None:

        self.context = context

        self.namespaces = (
            context.xpath_map()
        )



    # -------------------------------------------------------------------------
    # Execute XPath
    # -------------------------------------------------------------------------


    def execute(
        self,
        node: etree._Element | etree._ElementTree,
        expression: str,
    ) -> XPathResult:
        """
        Execute XPath expression.
        """

        result = node.xpath(
            expression,
            namespaces=self.namespaces,
        )

        return XPathResult(
            nodes=list(result)
        )



    # -------------------------------------------------------------------------
    # Find helpers
    # -------------------------------------------------------------------------


    def find(
        self,
        node: etree._Element | etree._ElementTree,
        expression: str,
    ) -> list[etree._Element]:
        """
        Find elements.
        """

        result = self.execute(
            node,
            expression,
        )

        return [
            item
            for item in result.nodes
            if isinstance(
                item,
                etree._Element,
            )
        ]



    def find_one(
        self,
        node: etree._Element | etree._ElementTree,
        expression: str,
    ) -> etree._Element | None:
        """
        Return first element.
        """

        elements = self.find(
            node,
            expression,
        )

        if elements:
            return elements[0]

        return None



    # -------------------------------------------------------------------------
    # Value helpers
    # -------------------------------------------------------------------------


    def text(
        self,
        node: etree._Element | None,
    ) -> str | None:
        """
        Extract element text.
        """

        if node is None:
            return None


        value = node.text


        if value is None:
            return None


        return value.strip()



    def attribute(
        self,
        node: etree._Element | None,
        name: str,
    ) -> str | None:
        """
        Read attribute.
        """

        if node is None:
            return None


        return node.get(
            name
        )



    # -------------------------------------------------------------------------
    # AUTOSAR common queries
    # -------------------------------------------------------------------------


    def find_packages(
        self,
        root: etree._Element,
    ) -> list[etree._Element]:
        """
        Find AR-PACKAGE elements.
        """

        return self.find(
            root,
            "//autosar:AR-PACKAGE",
        )



    def find_elements(
        self,
        root: etree._Element,
    ) -> list[etree._Element]:
        """
        Find all ARXML elements.
        """

        return self.find(
            root,
            "//autosar:ELEMENTS/*",
        )



    def find_short_name(
        self,
        element: etree._Element,
    ) -> str | None:
        """
        Extract SHORT-NAME.
        """

        node = self.find_one(
            element,
            "./autosar:SHORT-NAME",
        )

        return self.text(
            node
        )



    def find_reference(
        self,
        element: etree._Element,
        tag: str,
    ) -> str | None:
        """
        Extract AUTOSAR reference.

        Example:

        DATA-TYPE-REF

        """

        node = self.find_one(
            element,
            f"./autosar:{tag}",
        )

        return self.text(
            node
        )