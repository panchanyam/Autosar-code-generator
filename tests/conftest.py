"""
tests.conftest

Shared pytest fixtures for AUTOSAR CodeGen.

Provides common test objects used by:

- parser tests
- resolver tests
- validator tests
- generator tests
- simulator tests
"""

from __future__ import annotations


import pytest


from pathlib import Path


from autosar_codegen.model.workspace import (
    Workspace,
)


from autosar_codegen.model.datatype import (
    Datatype,
)


from autosar_codegen.model.signal import (
    Signal,
)


from autosar_codegen.model.pdu import (
    Pdu,
)


from autosar_codegen.model.frame import (
    Frame,
)


from autosar_codegen.model.network import (
    Network,
)


from autosar_codegen.simulator.context import (
    SimulationContext,
)



# ============================================================================
# Temporary Directory
# ============================================================================


@pytest.fixture
def temp_directory(
    tmp_path: Path,
):
    """
    Provides temporary test directory.
    """

    return tmp_path



# ============================================================================
# Sample ARXML
# ============================================================================


@pytest.fixture
def sample_arxml(
    tmp_path: Path,
):
    """
    Creates minimal AUTOSAR XML file.
    """

    content = """
    <?xml version="1.0" encoding="UTF-8"?>

    <AUTOSAR>

        <AR-PACKAGES>

            <AR-PACKAGE>

                <SHORT-NAME>Vehicle</SHORT-NAME>

            </AR-PACKAGE>

        </AR-PACKAGES>

    </AUTOSAR>
    """

    file = tmp_path / "sample.arxml"


    file.write_text(

        content,

        encoding="utf-8"

    )


    return file



# ============================================================================
# Workspace Fixture
# ============================================================================


@pytest.fixture
def workspace():
    """
    Creates empty AUTOSAR workspace.
    """

    return Workspace()



# ============================================================================
# Complete Model Fixture
# ============================================================================


@pytest.fixture
def populated_workspace():
    """
    Creates sample AUTOSAR model.
    """

    ws = Workspace()



    datatype = Datatype(

        name="uint8",

    )


    signal = Signal(

        name="EngineSpeed",

        datatype=datatype,

    )


    pdu = Pdu(

        name="EngineData",

        signals=[

            signal

        ],

    )


    frame = Frame(

        name="EngineFrame",

        pdus=[

            pdu

        ],

    )


    network = Network(

        name="CAN",

        frames=[

            frame

        ],

    )



    ws.datatypes.append(

        datatype

    )


    ws.signals.append(

        signal

    )


    ws.pdus.append(

        pdu

    )


    ws.frames.append(

        frame

    )


    ws.networks.append(

        network

    )


    return ws



# ============================================================================
# Simulation Context
# ============================================================================


@pytest.fixture
def simulation_context(
    workspace,
):
    """
    Creates simulator runtime context.
    """

    return SimulationContext(

        workspace

    )



# ============================================================================
# Output Directory
# ============================================================================


@pytest.fixture
def output_directory(
    tmp_path: Path,
):
    """
    Creates generator output directory.
    """

    directory = tmp_path / "generated"


    directory.mkdir()


    return directory