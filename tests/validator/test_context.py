"""
Tests validator context.
"""

from autosar_codegen.validator.context import (
    ValidatorContext,
)



def test_context_creation():

    context = ValidatorContext()


    assert context is not None



def test_context_storage():

    context = ValidatorContext()


    context.set(
        "key",
        "value",
    )


    assert context.get(
        "key"
    ) == "value"



def test_missing_context_value():

    context = ValidatorContext()


    assert context.get(
        "missing"
    ) is None