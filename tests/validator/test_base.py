"""
Tests validator base interface.
"""

from autosar_codegen.validator.base import (
    Validator,
)



class DummyValidator(Validator):

    name = "dummy"


    def validate(
        self,
        context,
    ):

        return True



def test_validator_creation():

    validator = DummyValidator()

    assert validator is not None



def test_validator_name():

    validator = DummyValidator()

    assert validator.name == "dummy"



def test_validate_execution():

    validator = DummyValidator()


    result = validator.validate(
        None
    )


    assert result is True