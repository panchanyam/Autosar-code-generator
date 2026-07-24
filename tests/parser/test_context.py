"""
Tests parser context.
"""

from autosar_codegen.parser.context import (
    ParserContext,
)



def test_context_creation():

    context = ParserContext()

    assert context is not None



def test_context_storage():

    context = ParserContext()


    context.set(
        "key",
        "value",
    )


    assert context.get(
        "key"
    ) == "value"