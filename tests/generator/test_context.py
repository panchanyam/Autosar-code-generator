"""
Tests generator context.
"""

from autosar_codegen.generator.context import (
    GeneratorContext,
)



def test_context_creation():

    context = GeneratorContext()


    assert context is not None



def test_context_variables():

    context = GeneratorContext()


    context.set(
        "language",
        "c",
    )


    assert context.get(
        "language"
    ) == "c"



def test_missing_value():

    context = GeneratorContext()


    assert context.get(
        "unknown"
    ) is None