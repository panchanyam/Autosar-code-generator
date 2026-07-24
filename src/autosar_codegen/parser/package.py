"""
autosar_codegen.parser.package
==============================

AUTOSAR AR-PACKAGE parser.

Extracts package hierarchy from ARXML.

"""

from __future__ import annotations

from autosar_codegen.parser.base import (
    Parser,
    ParserMetadata,
)

from autosar_codegen.parser.context import (
    ParserContext,
)

from autosar_codegen.xml.walker import (
    XmlNode,
)

from autosar_codegen.model.package import (
    Package,
)



# ============================================================================
# Package Parser
# ============================================================================


class PackageParser(Parser):
    """
    Parses AUTOSAR AR-PACKAGE elements.
    """

    metadata = ParserMetadata(

        name="PackageParser",

        version="1.0.0",

        description=(
            "Parses AUTOSAR AR-PACKAGE hierarchy"
        ),

        supported_tags=(
            "AR-PACKAGE",
        ),

        priority=10,

    )


    # -------------------------------------------------------------------------
    # Parse
    # -------------------------------------------------------------------------


    def parse(
        self,
        node: XmlNode,
        workspace,
        diagnostics,
    ) -> bool:
        """
        Parse AR-PACKAGE.
        """

        try:

            context = workspace.context


            xpath = context.xpath


            #
            # Extract package name
            #
            name = xpath.find_short_name(
                node.element
            )


            if not name:

                diagnostics.error(
                    "AR-PACKAGE missing SHORT-NAME"
                )

                return False



            #
            # Build package object
            #
            package = Package(

                name=name,

                path=node.path,

            )


            #
            # Add to workspace
            #
            workspace.add_package(
                package
            )


            self.success()


            return True



        except Exception as exc:


            diagnostics.error(
                f"Package parsing failed: {exc}"
            )


            self.failure()


            return False