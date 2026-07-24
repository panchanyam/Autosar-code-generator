"""
autosar_codegen.resolver.network
================================

AUTOSAR network reference resolver.

Resolves:

    Network -> Frame references

"""

from __future__ import annotations


from autosar_codegen.resolver.base import (
    Resolver,
    ResolverMetadata,
)



class NetworkResolver(Resolver):
    """
    Resolves AUTOSAR network dependencies.
    """


    metadata = ResolverMetadata(

        name="NetworkResolver",

        version="1.0.0",

        description=(

            "Resolves network frame references"

        ),

        priority=50,

        dependencies=(

            "FrameResolver",

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
        Resolve network frame references.
        """

        workspace = context.workspace


        success = True



        for network in workspace.networks:


            self.statistics.processed += 1



            resolved_frames = []



            #
            # Resolve frame references
            #
            for frame_ref in network.frames:


                #
                # Already resolved
                #
                if not isinstance(
                    frame_ref,
                    str
                ):

                    resolved_frames.append(
                        frame_ref
                    )

                    continue



                frame = context.lookup(
                    frame_ref
                )



                if frame is None:


                    context.error(

                        f"Network '{network.name}' "
                        f"frame not found: "
                        f"{frame_ref}"

                    )


                    self.statistics.failed += 1

                    success = False

                    continue



                resolved_frames.append(
                    frame
                )



            #
            # Replace references
            #
            network.frames = resolved_frames



            #
            # Validate
            #
            self._validate_network(

                network,

                context

            )


            self.statistics.resolved += 1



        return success



    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------


    def _validate_network(
        self,
        network,
        context,
    ):
        """
        Validate network configuration.
        """


        if not network.frames:


            context.warning(

                f"Network '{network.name}' "
                "contains no frames"

            )



        if (

            hasattr(network, "baudrate")

            and

            network.baudrate is not None

        ):


            if network.baudrate <= 0:


                context.error(

                    f"Invalid baudrate "
                    f"for network '{network.name}'"

                )