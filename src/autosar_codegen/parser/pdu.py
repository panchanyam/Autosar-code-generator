"""
autosar_codegen.parser.pdu
==========================

AUTOSAR I-PDU parser.

Parses:

    I-PDU

and signal mappings:

    I-SIGNAL-I-PDU

"""

from __future__ import annotations


from autosar_codegen.parser.base import (
    Parser,
    ParserMetadata,
)

from autosar_codegen.xml.walker import (
    XmlNode,
)

from autosar_codegen.model.pdu import (
    Pdu,
    PduSignalMapping,
)



class PduParser(Parser):
    """
    Parses AUTOSAR I-PDU objects.
    """


    metadata = ParserMetadata(

        name="PduParser",

        version="1.0.0",

        description=(
            "Parses AUTOSAR I-PDU definitions"
        ),

        supported_tags=(
            "I-PDU",
        ),

        priority=40,

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
        Parse I-PDU.
        """

        try:

            context = workspace.context

            xpath = context.xpath



            #
            # PDU Name
            #
            name = xpath.find_short_name(
                node.element
            )


            if not name:

                diagnostics.error(
                    "I-PDU missing SHORT-NAME"
                )

                return False



            #
            # PDU Length
            #
            length = None


            length_node = xpath.find_one(

                node.element,

                "./autosar:LENGTH"

            )


            if length_node:


                value = xpath.text(
                    length_node
                )


                if value:

                    length = int(value)



            #
            # Create PDU
            #
            pdu = Pdu(

                name=name,

                length=length,

                path=node.path,

            )



            #
            # Parse signal mappings
            #
            mappings = xpath.find(

                node.element,

                ".//autosar:I-SIGNAL-I-PDU"

            )


            for mapping_node in mappings:


                signal_ref = self._read_ref(

                    xpath,

                    mapping_node,

                    "I-SIGNAL-REF"

                )


                start_position = self._read_int(

                    xpath,

                    mapping_node,

                    "START-POSITION"

                )


                signal_mapping = PduSignalMapping(

                    signal_ref=signal_ref,

                    start_bit=start_position,

                )


                pdu.add_signal(
                    signal_mapping
                )



            workspace.add_pdu(
                pdu
            )


            self.success()


            return True



        except Exception as exc:


            diagnostics.error(

                f"PDU parsing failed: {exc}"

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