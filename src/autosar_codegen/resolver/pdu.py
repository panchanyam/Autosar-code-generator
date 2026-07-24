"""
autosar_codegen.resolver.pdu
============================

AUTOSAR PDU reference resolver.

Resolves:

    PDU -> Signal mappings

"""

from __future__ import annotations


from autosar_codegen.resolver.base import (
    Resolver,
    ResolverMetadata,
)



class PduResolver(Resolver):
    """
    Resolves AUTOSAR PDU dependencies.
    """


    metadata = ResolverMetadata(

        name="PduResolver",

        version="1.0.0",

        description=(

            "Resolves PDU signal references"

        ),

        priority=30,

        dependencies=(

            "SignalResolver",

        ),

    )


    # ------------------------------------------------------------------
    # Resolve
    # ------------------------------------------------------------------

    def resolve(
        self,
        context,
    ) -> bool:
        """
        Resolve PDU signal references.
        """

        workspace = context.workspace


        success = True



        for pdu in workspace.pdus:


            self.statistics.processed += 1



            #
            # Resolve each signal mapping
            #
            for mapping in pdu.signals:


                if getattr(
                    mapping,
                    "signal",
                    None
                ) is not None:

                    continue



                if not mapping.signal_ref:


                    context.warning(

                        f"PDU '{pdu.name}' "
                        "has empty signal reference"

                    )


                    self.statistics.failed += 1

                    success = False

                    continue



                signal = context.lookup(

                    mapping.signal_ref

                )



                if signal is None:


                    context.error(

                        f"PDU '{pdu.name}' "
                        f"signal not found: "
                        f"{mapping.signal_ref}"

                    )


                    self.statistics.failed += 1

                    success = False

                    continue



                #
                # Link signal
                #
                mapping.signal = signal



            self.statistics.resolved += 1



        return success