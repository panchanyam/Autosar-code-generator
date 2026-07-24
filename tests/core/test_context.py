"""
Tests for application context.
"""

from autosar_codegen.core.context import (
    ApplicationContext,
)



def test_context_creation():

    context = ApplicationContext()


    assert context is not None



def test_context_metadata():

    context = ApplicationContext()


    context.metadata["project"] = (
        "AUTOSAR"
    )


    assert (
        context.metadata["project"]
        ==
        "AUTOSAR"
    )



def test_context_storage():

    context = ApplicationContext()


    context.set(
        "test",
        100,
    )


    assert context.get(
        "test"
    ) == 100