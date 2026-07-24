"""
Tests for XML cache.
"""

from autosar_codegen.xml.cache import (
    XmlCache,
)



def test_cache_creation():

    cache = XmlCache()


    assert cache is not None



def test_cache_store():

    cache = XmlCache()


    document = object()


    cache.set(
        "sample",
        document,
    )


    assert cache.get(
        "sample"
    ) == document



def test_cache_missing():

    cache = XmlCache()


    assert cache.get(
        "missing"
    ) is None



def test_cache_clear():

    cache = XmlCache()


    cache.set(
        "test",
        object()
    )


    cache.clear()


    assert cache.get(
        "test"
    ) is None