"""
tests.generator.test_c_generator
================================

End-to-end test for AUTOSAR C generation pipeline.
"""

from __future__ import annotations


from pathlib import Path


import tempfile



from autosar_codegen.generator.bootstrap import (
    create_default_registry,
)


from autosar_codegen.generator.context import (
    GeneratorContext,
)


from autosar_codegen.generator.dispatcher import (
    GeneratorDispatcher,
)



# ============================================================================
# Mock AUTOSAR Model
# ============================================================================


class MockDatatype:
    """
    Minimal datatype model.
    """

    def __init__(
        self,
        name,
        base_type,
    ):

        self.name = name

        self.base_type = base_type



class MockSignal:
    """
    Minimal signal model.
    """

    def __init__(
        self,
        name,
        datatype,
    ):

        self.name = name

        self.datatype = datatype



class MockPdu:
    """
    Minimal PDU model.
    """

    def __init__(
        self,
        name,
        signals,
    ):

        self.name = name

        self.signals = signals



class MockWorkspace:
    """
    Minimal workspace.
    """

    def __init__(self):

        datatype = MockDatatype(

            "EngineSpeedType",

            "uint16"

        )


        signal = MockSignal(

            "EngineSpeed",

            datatype

        )


        pdu = MockPdu(

            "EngineData",

            [

                type(

                    "Mapping",

                    (),

                    {

                        "signal": signal

                    }

                )()

            ]

        )


        self.datatypes = [

            datatype

        ]


        self.signals = [

            signal

        ]


        self.pdus = [

            pdu

        ]



# ============================================================================
# Test
# ============================================================================


def test_c_generator_end_to_end():

    """
    Validate complete C generation.
    """

    with tempfile.TemporaryDirectory() as tmp:


        output = Path(tmp)



        workspace = MockWorkspace()



        context = GeneratorContext(

            workspace=workspace,

            output_dir=output

        )



        registry = create_default_registry()



        dispatcher = GeneratorDispatcher(

            registry

        )



        result = dispatcher.generate(

            context,

            language="C"

        )



        # Generation succeeded

        assert result.successful == 1

        assert result.failed == 0



        # Verify generated files

        datatype_file = (

            output /

            "include" /

            "datatypes.h"

        )


        signal_file = (

            output /

            "include" /

            "signals.h"

        )


        pdu_file = (

            output /

            "include" /

            "pdus.h"

        )



        assert datatype_file.exists()

        assert signal_file.exists()

        assert pdu_file.exists()



        # Verify content

        datatype_content = (

            datatype_file
            .read_text()

        )


        assert "EngineSpeedType" in datatype_content



        signal_content = (

            signal_file
            .read_text()

        )


        assert "EngineSpeed" in signal_content



        pdu_content = (

            pdu_file
            .read_text()

        )


        assert "EngineData" in pdu_content