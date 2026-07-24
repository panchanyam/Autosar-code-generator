"""
Tests resolver base interface.
"""

from autosar_codegen.resolver.base import (
    Resolver,
)


class DummyResolver(Resolver):

    name = "dummy"


    def resolve(self, context):
        return "resolved"



def test_resolver_creation():

    resolver = DummyResolver()

    assert resolver is not None



def test_resolver_name():

    resolver = DummyResolver()

    assert resolver.name == "dummy"



def test_resolve_execution():

    resolver = DummyResolver()

    result = resolver.resolve(None)

    assert result == "resolved"