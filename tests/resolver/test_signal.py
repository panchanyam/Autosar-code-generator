"""
Tests signal resolver.
"""

from autosar_codegen.resolver.signal import (
    SignalResolver,
)



def test_signal_resolver():

    resolver = SignalResolver()

    assert resolver is not None



def test_signal_resolution():

    resolver = SignalResolver()


    result = resolver.resolve(None)


    assert result is not None