"""
Tests for XML loader.
"""

from pathlib import Path


from autosar_codegen.xml.loader import (
    XmlLoader,
)



def test_loader_creation():

    loader = XmlLoader()


    assert loader is not None



def test_load_xml_file(
    sample_arxml,
):

    loader = XmlLoader()


    document = loader.load(
        sample_arxml
    )


    assert document is not None



def test_invalid_file():

    loader = XmlLoader()


    invalid = Path(
        "missing.arxml"
    )


    try:

        loader.load(
            invalid
        )

    except Exception:

        assert True

    else:

        assert False