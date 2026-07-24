"""
autosar_codegen.resolver.frame
==============================

AUTOSAR frame reference resolver.

Resolves:

    Frame -> PDU references

"""

from __future__ import annotations


from autosar_codegen.resolver.base import (
    Resolver,
    ResolverMetadata,
)



class FrameResolver(Resolver):
    """
    Resolves AUTOSAR frame dependencies.
    """


    metadata = ResolverMetadata(

        name="FrameResolver",

        version="1.0.0",

        description=(

            "Resolves frame PDU references"

        ),

        priority=40,

        dependencies=(

            "PduResolver",

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
        Resolve frame PDU references.
        """

        workspace = context.workspace


        success = True



        for frame in workspace.frames:


            self.statistics.processed += 1



            resolved_pdus = []



            #
            # Resolve PDU references
            #
            for pdu_ref in frame.pdus:


                #
                # Already resolved object
                #
                if not isinstance(
                    pdu_ref,
                    str
                ):

                    resolved_pdus.append(
                        pdu_ref
                    )

                    continue



                pdu = context.lookup(
                    pdu_ref
                )



                if pdu is None:


                    context.error(

                        f"Frame '{frame.name}' "
                        f"PDU not found: {pdu_ref}"

                    )


                    self.statistics.failed += 1

                    success = False

                    continue



                resolved_pdus.append(
                    pdu
                )



            #
            # Replace references
            #
            frame.pdus = resolved_pdus



            #
            # Validate frame size
            #
            self._validate_length(

                frame,

                context

            )



            self.statistics.resolved += 1



        return success



    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------


    def _validate_length(
        self,
        frame,
        context,
    ):
        """
        Validate payload size.
        """

        if not frame.length:

            return



        total = 0


        for pdu in frame.pdus:


            if hasattr(
                pdu,
                "length"
            ):

                if pdu.length:

                    total += pdu.length



        if total > frame.length:


            context.warning(

                f"Frame '{frame.name}' "
                f"payload size {total} exceeds "
                f"frame length {frame.length}"

            )