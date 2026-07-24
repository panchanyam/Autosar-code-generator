"""
Tests for XML namespace handling.
"""

from autosar_codegen.xml.namespace import (
    NamespaceManager,
)



def test_namespace_manager_creation():

    manager = NamespaceManager()


    assert manager is not None



def test_register_namespace():

    manager = NamespaceManager()


    manager.register(
        "autosar",
        "http://autosar.org/schema"
    )


    assert manager.get(
        "autosar"
    ) == "http://autosar.org/schema"



def test_namespace_lookup_missing():

    manager = NamespaceManager()


    assert manager.get(
        "unknown"
    ) is None