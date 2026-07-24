"""
autosar_codegen.resolver.datatype
=================================

AUTOSAR datatype reference resolver.

Resolves:

    Signal.datatype_ref

into:

    Signal.datatype

"""

from __future__ import annotations


from autosar_codegen.resolver.base import (
    Resolver,
    ResolverMetadata,
)



class DataTypeResolver(Resolver):
    """
    Resolves AUTOSAR datatype references.
    """


    metadata = ResolverMetadata(

        name="DataTypeResolver",

        version="1.0.0",

        description=(

            "Resolves signal datatype references"

        ),

        priority=10,

    )


    # ------------------------------------------------------------------
    # Resolve
    # ------------------------------------------------------------------


    def resolve(
        self,
        context,
    ) -> bool:
        """
        Resolve datatype references.
        """


        workspace = context.workspace


        success = True



        for signal in workspace.signals:


            self.statistics.processed += 1



            #
            # Already resolved
            #
            if signal.datatype is not None:

                self.statistics.resolved += 1

                continue



            #
            # Missing reference
            #
            if not signal.datatype_ref:


                context.warning(

                    f"Signal '{signal.name}' "
                    "has no datatype reference"

                )


                self.statistics.failed += 1

                success = False

                continue



            #
            # Lookup datatype
            #
            datatype = context.lookup(

                signal.datatype_ref

            )



            if datatype is None:


                context.error(

                    f"Datatype not found: "
                    f"{signal.datatype_ref}"

                )


                self.statistics.failed += 1

                success = False

                continue



            #
            # Link object
            #
            signal.datatype = datatype



            self.statistics.resolved += 1



        return success