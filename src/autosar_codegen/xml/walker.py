"""
autosar_codegen.xml.walker
==========================

AUTOSAR XML tree walker.

Provides traversal services for parser modules.

"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterator

from lxml import etree



# ============================================================================
# XML Node
# ============================================================================


@dataclass(slots=True)
class XmlNode:
    """
    Represents one XML node during traversal.
    """

    element: etree._Element

    tag: str

    path: str

    depth: int

    line: int | None

    parent: "XmlNode | None" = None



    @property
    def text(
        self,
    ) -> str | None:
        """
        Get node text.
        """

        if self.element.text:

            return self.element.text.strip()

        return None



    def attribute(
        self,
        name: str,
    ) -> str | None:
        """
        Get attribute.
        """

        return self.element.get(
            name
        )



# ============================================================================
# Walker Statistics
# ============================================================================


@dataclass(slots=True)
class WalkerStatistics:
    """
    Walker execution statistics.
    """

    nodes: int = 0

    max_depth: int = 0



# ============================================================================
# XML Walker
# ============================================================================


class XmlWalker:
    """
    Recursive AUTOSAR XML walker.

    """

    def __init__(
        self,
    ) -> None:

        self.statistics = WalkerStatistics()



    # -------------------------------------------------------------------------
    # Public walk
    # -------------------------------------------------------------------------


    def walk(
        self,
        root: etree._Element,
    ) -> Iterator[XmlNode]:
        """
        Walk complete XML tree.
        """

        self.statistics = WalkerStatistics()


        yield from self._walk_node(
            root,
            parent=None,
            depth=0,
            path="",
        )



    # -------------------------------------------------------------------------
    # Recursive traversal
    # -------------------------------------------------------------------------


    def _walk_node(
        self,
        element: etree._Element,
        parent: XmlNode | None,
        depth: int,
        path: str,
    ) -> Iterator[XmlNode]:


        tag = self._clean_tag(
            element.tag
        )


        current_path = (
            f"{path}/{tag}"
        )


        node = XmlNode(

            element=element,

            tag=tag,

            path=current_path,

            depth=depth,

            line=element.sourceline,

            parent=parent,

        )


        self.statistics.nodes += 1


        self.statistics.max_depth = max(

            self.statistics.max_depth,

            depth,

        )


        yield node



        for child in element:


            yield from self._walk_node(

                child,

                parent=node,

                depth=depth + 1,

                path=current_path,

            )



    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------


    def _clean_tag(
        self,
        tag: str,
    ) -> str:
        """
        Remove XML namespace.

        Converts:

        {namespace}AR-PACKAGE

        to:

        AR-PACKAGE

        """

        if "}" in tag:

            return tag.split(
                "}",
                1
            )[1]


        return tag



    # -------------------------------------------------------------------------
    # Search helpers
    # -------------------------------------------------------------------------


    def find_tag(
        self,
        root: etree._Element,
        tag: str,
    ) -> list[XmlNode]:
        """
        Find all nodes with tag.
        """

        result = []


        for node in self.walk(root):

            if node.tag == tag:

                result.append(node)


        return result