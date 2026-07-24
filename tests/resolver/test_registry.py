"""
Tests resolver registry.
"""

from autosar_codegen.resolver.registry import (
    ResolverRegistry,
)



class DummyResolver:

    name = "dummy"



def test_register_resolver():

    registry = ResolverRegistry()


    resolver = DummyResolver()


    registry.register(
        resolver
    )


    assert registry.get(
        "dummy"
    ) == resolver



def test_registry_count():

    registry = ResolverRegistry()


    registry.register(
        DummyResolver()
    )


    assert len(
        registry.all()
    ) == 1



def test_remove_resolver():

    registry = ResolverRegistry()


    registry.register(
        DummyResolver()
    )


    registry.remove(
        "dummy"
    )


    assert registry.get(
        "dummy"
    ) is None