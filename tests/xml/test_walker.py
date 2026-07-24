"""
Tests for XML tree walker.
"""

from autosar_codegen.xml.loader import (
    XmlLoader,
)


from autosar_codegen.xml.walker import (
    XmlWalker,
)



def test_walker_creation():

    walker = XmlWalker()


    assert walker is not None



def test_walk_document(
    sample_arxml,
):

    loader = XmlLoader()

    document = loader.load(
        sample_arxml
    )


    walker = XmlWalker()


    nodes = list(
        walker.walk(
            document
        )
    )


    assert len(nodes) > 0