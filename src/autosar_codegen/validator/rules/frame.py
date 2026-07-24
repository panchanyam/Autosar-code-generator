"""
AUTOSAR frame validation rules.
"""

from autosar_codegen.validator.base import (
    Validator,
    ValidatorMetadata,
)



class FrameValidator(Validator):

    metadata = ValidatorMetadata(

        name="FrameValidator",

        description="Validates AUTOSAR frames",

        priority=40,

    )


    def validate(
        self,
        context,
    ) -> bool:


        valid = True


        for frame in getattr(
            context.workspace,
            "frames",
            []
        ):


            self.processed()



            if not getattr(
                frame,
                "pdus",
                None
            ):

                context.warning(

                    f"Frame '{frame.name}' "
                    "has no PDUs",

                    validator=self.name,

                    object_name=frame.name,

                )



        return valid