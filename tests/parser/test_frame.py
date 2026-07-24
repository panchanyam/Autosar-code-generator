"""
Tests frame parser.
"""

from autosar_codegen.parser.frame import (
    FrameParser,
)



def test_frame_parser():

    parser = FrameParser()

    assert parser is not None



def test_frame_parse():

    parser = FrameParser()


    result = parser.parse(None)


    assert result is not None