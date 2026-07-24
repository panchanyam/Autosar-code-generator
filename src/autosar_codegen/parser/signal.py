"""
autosar_codegen.parser.signal
=============================

AUTOSAR I-SIGNAL parser.

Parses signal definitions from ARXML.

"""

from __future__ import annotations


from autosar_codegen.parser.base import (
    Parser,
    ParserMetadata,
)

from autosar_codegen.xml.walker import (
    XmlNode,
)

from autosar_codegen.model.signal import (
    Signal,
)



class SignalParser(Parser):
    """
    Parses AUTOSAR I-SIGNAL objects.
    """


    metadata = ParserMetadata(

        name="SignalParser",

        version="1.0.0",

        description=(
            "Parses AUTOSAR I-SIGNAL definitions"
        ),

        supported_tags=(
            "I-SIGNAL",
        ),

        priority=30,

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
        Parse I-SIGNAL.
        """

        try:

            context = workspace.context

            xpath = context.xpath



            #
            # Signal name
            #
            name = xpath.find_short_name(
                node.element
            )


            if not name:

                diagnostics.error(
                    "I-SIGNAL missing SHORT-NAME"
                )

                return False



            #
            # LENGTH
            #
            length_node = xpath.find_one(

                node.element,

                "./autosar:LENGTH"

            )


            length = None


            if length_node:

                text = xpath.text(
                    length_node
                )

                if text:

                    length = int(text)



            #
            # DATA-TYPE-REF
            #
            datatype_node = xpath.find_one(

                node.element,

                "./autosar:DATA-TYPE-REF"

            )


            datatype_ref = xpath.text(
                datatype_node
            )



            #
            # SYSTEM-SIGNAL-REF
            #
            system_signal_node = xpath.find_one(

                node.element,

                "./autosar:SYSTEM-SIGNAL-REF"

            )


            system_signal_ref = xpath.text(
                system_signal_node
            )



            #
            # INIT VALUE
            #
            init_node = xpath.find_one(

                node.element,

                ".//autosar:INIT-VALUE"

            )


            init_value = xpath.text(
                init_node
            )



            #
            # Create Signal Model
            #
            signal = Signal(

                name=name,

                length=length,

                datatype_ref=datatype_ref,

                system_signal_ref=system_signal_ref,

                init_value=init_value,

                path=node.path,

            )


            workspace.add_signal(
                signal
            )


            self.success()


            return True



        except Exception as exc:


            diagnostics.error(

                f"Signal parsing failed: {exc}"

            )


            self.failure()


            return False