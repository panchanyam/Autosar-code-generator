"""
Tests signal parser.
"""

from autosar_codegen.parser.signal import (
    SignalParser,
)



def test_signal_parser():

    parser = SignalParser()

    assert parser is not None



def test_signal_parse():

    parser = SignalParser()


    result = parser.parse(None)


    assert result is not None