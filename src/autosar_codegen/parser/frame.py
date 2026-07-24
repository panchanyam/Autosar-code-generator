"""
autosar_codegen.parser.frame
============================

AUTOSAR CAN Frame parser.

Parses:

    CAN-FRAME

and:

    PDU-TO-FRAME-MAPPING

"""

from __future__ import annotations


from autosar_codegen.parser.base import (
    Parser,
    ParserMetadata,
)

from autosar_codegen.xml.walker import (
    XmlNode,
)

from autosar_codegen.model.frame import (
    Frame,
)



class FrameParser(Parser):
    """
    Parses AUTOSAR CAN-FRAME definitions.
    """


    metadata = ParserMetadata(

        name="FrameParser",

        version="1.0.0",

        description=(
            "Parses AUTOSAR CAN frame definitions"
        ),

        supported_tags=(
            "CAN-FRAME",
        ),

        priority=50,

    )


    # ------------------------------------------------------------------
    # Parse
    # ------------------------------------------------------------------

    def parse(
        self,
        node: XmlNode,
        workspace,
        diagnostics,
    ) -> bool:
        """
        Parse CAN-FRAME.
        """

        try:

            context = workspace.context

            xpath = context.xpath



            #
            # Frame name
            #
            name = xpath.find_short_name(
                node.element
            )


            if not name:

                diagnostics.error(
                    "CAN-FRAME missing SHORT-NAME"
                )

                return False



            #
            # Frame length
            #
            length = self._read_int(

                xpath,

                node.element,

                "FRAME-LENGTH"

            )



            #
            # Create Frame model
            #
            frame = Frame(

                name=name,

                length=length,

                frame_type="CAN",

                path=node.path,

            )



            #
            # Find mapped PDUs
            #
            mappings = xpath.find(

                node.element,

                ".//autosar:PDU-TO-FRAME-MAPPING"

            )


            for mapping in mappings:


                pdu_ref = self._read_ref(

                    xpath,

                    mapping,

                    "I-PDU-REF"

                )


                if pdu_ref:

                    frame.add_pdu(
                        pdu_ref
                    )



            workspace.add_frame(
                frame
            )


            self.success()


            return True



        except Exception as exc:


            diagnostics.error(

                f"Frame parsing failed: {exc}"

            )


            self.failure()


            return False



    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------


    def _read_ref(
        self,
        xpath,
        node,
        tag,
    ):

        element = xpath.find_one(

            node,

            f"./autosar:{tag}"

        )


        return xpath.text(
            element
        )



    def _read_int(
        self,
        xpath,
        node,
        tag,
    ):

        element = xpath.find_one(

            node,

            f"./autosar:{tag}"

        )


        value = xpath.text(
            element
        )


        if value:

            return int(value)


        return None