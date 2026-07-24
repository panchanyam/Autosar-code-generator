"""
Tests resolver context.
"""

from autosar_codegen.resolver.context import (
    ResolverContext,
)



def test_context_creation():

    context = ResolverContext()

    assert context is not None



def test_context_storage():

    context = ResolverContext()


    context.set(
        "datatype",
        "uint8",
    )


    assert context.get(
        "datatype"
    ) == "uint8"



def test_missing_value():

    context = ResolverContext()


    assert context.get(
        "unknown"
    ) is None