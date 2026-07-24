"""
autosar_codegen.parser.network
==============================

AUTOSAR communication network parser.

Parses:

    CAN-CLUSTER
    CAN-CHANNEL

"""

from __future__ import annotations


from autosar_codegen.parser.base import (
    Parser,
    ParserMetadata,
)

from autosar_codegen.xml.walker import (
    XmlNode,
)

from autosar_codegen.model.network import (
    Network,
    NetworkChannel,
)



class NetworkParser(Parser):
    """
    Parses AUTOSAR network definitions.
    """


    metadata = ParserMetadata(

        name="NetworkParser",

        version="1.0.0",

        description=(
            "Parses AUTOSAR communication networks"
        ),

        supported_tags=(

            "CAN-CLUSTER",

            "CAN-CHANNEL",

        ),

        priority=60,

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
        Parse network object.
        """

        try:

            context = workspace.context

            xpath = context.xpath



            name = xpath.find_short_name(
                node.element
            )


            if not name:

                diagnostics.error(
                    f"{node.tag} missing SHORT-NAME"
                )

                return False



            #
            # CAN Cluster
            #
            if node.tag == "CAN-CLUSTER":

                network = Network(

                    name=name,

                    network_type="CAN",

                    path=node.path,

                )


                baudrate = self._read_int(

                    xpath,

                    node.element,

                    "BAUDRATE"

                )


                network.baudrate = baudrate



                workspace.add_network(
                    network
                )



            #
            # CAN Channel
            #
            elif node.tag == "CAN-CHANNEL":


                channel = NetworkChannel(

                    name=name,

                    channel_type="CAN",

                    path=node.path,

                )


                workspace.add_channel(
                    channel
                )



            self.success()


            return True



        except Exception as exc:


            diagnostics.error(

                f"Network parsing failed: {exc}"

            )


            self.failure()


            return False



    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------


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