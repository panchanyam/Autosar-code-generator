"""
Tests for plugin registry.
"""

from autosar_codegen.core.registry import (
    Registry,
)



class DummyPlugin:

    name = "dummy"



def test_registry_creation():

    registry = Registry()


    assert registry is not None



def test_register_plugin():

    registry = Registry()


    plugin = DummyPlugin()


    registry.register(
        plugin
    )


    assert registry.get(
        "dummy"
    ) == plugin



def test_unregister_plugin():

    registry = Registry()


    plugin = DummyPlugin()


    registry.register(
        plugin
    )


    registry.unregister(
        "dummy"
    )


    assert registry.get(
        "dummy"
    ) is None



def test_registry_iteration():

    registry = Registry()


    registry.register(
        DummyPlugin()
    )


    items = list(
        registry
    )


    assert len(items) == 1