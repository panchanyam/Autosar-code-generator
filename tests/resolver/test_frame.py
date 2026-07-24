"""
Tests frame resolver.
"""

from autosar_codegen.resolver.frame import (
    FrameResolver,
)



def test_frame_resolver():

    resolver = FrameResolver()

    assert resolver is not None



def test_frame_resolution():

    resolver = FrameResolver()


    result = resolver.resolve(None)


    assert result is not None