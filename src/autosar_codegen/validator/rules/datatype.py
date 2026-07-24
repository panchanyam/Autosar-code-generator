"""
AUTOSAR datatype validation rules.
"""

from autosar_codegen.validator.base import (
    Validator,
    ValidatorMetadata,
)



class DatatypeValidator(Validator):

    metadata = ValidatorMetadata(

        name="DatatypeValidator",

        description="Validates AUTOSAR datatypes",

        priority=10,

    )


    def validate(
        self,
        context,
    ) -> bool:


        valid = True


        for datatype in context.workspace.datatypes:


            self.processed()



            if not getattr(
                datatype,
                "name",
                None
            ):

                context.error(

                    "Datatype has no name",

                    validator=self.name,

                )

                valid = False



            if not getattr(
                datatype,
                "base_type",
                None
            ):

                context.warning(

                    f"Datatype '{datatype.name}' "
                    "has no base type",

                    validator=self.name,

                    object_name=datatype.name,

                )



        return valid