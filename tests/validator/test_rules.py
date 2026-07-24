"""
Tests AUTOSAR validation rules.
"""

from autosar_codegen.validator.rules.datatype import (
    DatatypeRule,
)

from autosar_codegen.validator.rules.signal import (
    SignalRule,
)

from autosar_codegen.validator.rules.pdu import (
    PduRule,
)

from autosar_codegen.validator.rules.frame import (
    FrameRule,
)

from autosar_codegen.validator.rules.network import (
    NetworkRule,
)



def test_datatype_rule_creation():

    rule = DatatypeRule()

    assert rule is not None



def test_signal_rule_creation():

    rule = SignalRule()

    assert rule is not None



def test_pdu_rule_creation():

    rule = PduRule()

    assert rule is not None



def test_frame_rule_creation():

    rule = FrameRule()

    assert rule is not None



def test_network_rule_creation():

    rule = NetworkRule()

    assert rule is not None



def test_rule_execution(
    populated_workspace,
):

    rules = [

        DatatypeRule(),

        SignalRule(),

        PduRule(),

        FrameRule(),

        NetworkRule(),

    ]


    for rule in rules:

        result = rule.validate(
            populated_workspace
        )


        assert result is not None