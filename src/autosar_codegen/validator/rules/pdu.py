"""
AUTOSAR PDU validation rules.
"""

from autosar_codegen.validator.base import (
    Validator,
    ValidatorMetadata,
)



class PduValidator(Validator):

    metadata = ValidatorMetadata(

        name="PduValidator",

        description="Validates AUTOSAR PDUs",

        priority=30,

    )


    def validate(
        self,
        context,
    ) -> bool:


        valid = True


        for pdu in context.workspace.pdus:


            self.processed()



            if not getattr(
                pdu,
                "signals",
                None
            ):


                context.warning(

                    f"PDU '{pdu.name}' "
                    "contains no signals",

                    validator=self.name,

                    object_name=pdu.name,

                )



        return valid