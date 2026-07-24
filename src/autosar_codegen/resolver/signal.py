"""
autosar_codegen.resolver.signal
===============================

AUTOSAR signal reference resolver.

Resolves:

    Signal datatype references
    Signal system-signal references

"""

from __future__ import annotations


from autosar_codegen.resolver.base import (
    Resolver,
    ResolverMetadata,
)



class SignalResolver(Resolver):
    """
    Resolves AUTOSAR I-SIGNAL references.
    """


    metadata = ResolverMetadata(

        name="SignalResolver",

        version="1.0.0",

        description=(

            "Resolves signal dependencies"

        ),

        priority=20,

        dependencies=(

            "DataTypeResolver",

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
        Resolve signal references.
        """

        workspace = context.workspace


        success = True



        for signal in workspace.signals:


            self.statistics.processed += 1



            #
            # Datatype resolution
            #
            if signal.datatype is None:


                if signal.datatype_ref:


                    datatype = context.lookup(

                        signal.datatype_ref

                    )


                    if datatype:


                        signal.datatype = datatype


                    else:


                        context.error(

                            f"Signal '{signal.name}' "
                            f"datatype not found: "
                            f"{signal.datatype_ref}"

                        )


                        self.statistics.failed += 1

                        success = False



            #
            # System Signal resolution
            #
            if hasattr(
                signal,
                "system_signal_ref"
            ):


                if (

                    signal.system_signal is None

                    and

                    signal.system_signal_ref

                ):


                    system_signal = context.lookup(

                        signal.system_signal_ref

                    )


                    if system_signal:


                        signal.system_signal = (
                            system_signal
                        )


                    else:


                        context.warning(

                            f"System signal not found: "
                            f"{signal.system_signal_ref}"

                        )



            #
            # Statistics
            #
            if success:

                self.statistics.resolved += 1



        return success