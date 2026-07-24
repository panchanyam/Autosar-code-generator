"""
autosar_codegen.parser.datatype
===============================

AUTOSAR Implementation Data Type parser.

Parses:

    IMPLEMENTATION-DATA-TYPE

"""

from __future__ import annotations


from autosar_codegen.parser.base import (
    Parser,
    ParserMetadata,
)

from autosar_codegen.xml.walker import (
    XmlNode,
)

from autosar_codegen.model.datatype import (
    DataType,
)



class DataTypeParser(Parser):
    """
    Parses AUTOSAR IMPLEMENTATION-DATA-TYPE.
    """


    metadata = ParserMetadata(

        name="DataTypeParser",

        version="1.0.0",

        description=(
            "Parses AUTOSAR implementation data types"
        ),

        supported_tags=(
            "IMPLEMENTATION-DATA-TYPE",
        ),

        priority=20,

    )


    # ---------------------------------------------------------------------
    # Parse
    # ---------------------------------------------------------------------


    def parse(
        self,
        node: XmlNode,
        workspace,
        diagnostics,
    ) -> bool:
        """
        Parse datatype definition.
        """

        try:

            context = workspace.context

            xpath = context.xpath



            #
            # SHORT-NAME
            #
            name = xpath.find_short_name(
                node.element
            )


            if not name:

                diagnostics.error(
                    "IMPLEMENTATION-DATA-TYPE missing SHORT-NAME"
                )

                return False



            #
            # CATEGORY
            #
            category_node = xpath.find_one(

                node.element,

                "./autosar:CATEGORY"

            )


            category = xpath.text(
                category_node
            )


            #
            # BASE-TYPE-REF
            #
            base_type_node = xpath.find_one(

                node.element,

                ".//autosar:BASE-TYPE-REF"

            )


            base_type = xpath.text(
                base_type_node
            )



            #
            # Create model
            #
            datatype = DataType(

                name=name,

                category=category,

                base_type=base_type,

                path=node.path,

            )


            workspace.add_datatype(
                datatype
            )


            self.success()


            return True



        except Exception as exc:


            diagnostics.error(

                f"Datatype parser failed: {exc}"

            )


            self.failure()


            return False