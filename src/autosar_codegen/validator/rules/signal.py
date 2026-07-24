"""
AUTOSAR signal validation rules.
"""

from autosar_codegen.validator.base import (
    Validator,
    ValidatorMetadata,
)



class SignalValidator(Validator):

    metadata = ValidatorMetadata(

        name="SignalValidator",

        description="Validates AUTOSAR signals",

        priority=20,

    )


    def validate(
        self,
        context,
    ) -> bool:


        valid = True


        for signal in context.workspace.signals:


            self.processed()



            if not getattr(
                signal,
                "datatype",
                None
            ):


                context.error(

                    f"Signal '{signal.name}' "
                    "has no datatype",

                    validator=self.name,

                    object_name=signal.name,

                )


                valid = False



        return valid