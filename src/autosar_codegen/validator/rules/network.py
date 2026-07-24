"""
AUTOSAR network validation rules.
"""

from autosar_codegen.validator.base import (
    Validator,
    ValidatorMetadata,
)



class NetworkValidator(Validator):

    metadata = ValidatorMetadata(

        name="NetworkValidator",

        description="Validates AUTOSAR networks",

        priority=50,

    )


    def validate(
        self,
        context,
    ) -> bool:


        valid = True


        for network in getattr(
            context.workspace,
            "networks",
            []
        ):


            self.processed()



            if not getattr(
                network,
                "frames",
                None
            ):


                context.warning(

                    f"Network '{network.name}' "
                    "contains no frames",

                    validator=self.name,

                    object_name=network.name,

                )



        return valid