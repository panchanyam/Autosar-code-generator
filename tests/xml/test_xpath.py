"""
Tests for XPath utilities.
"""

from autosar_codegen.xml.xpath import (
    XPathEvaluator,
)



def test_xpath_creation():

    evaluator = XPathEvaluator()


    assert evaluator is not None



def test_xpath_query(
    sample_arxml,
):

    from autosar_codegen.xml.loader import (
        XmlLoader,
    )


    loader = XmlLoader()


    document = loader.load(
        sample_arxml
    )


    xpath = XPathEvaluator()


    result = xpath.find(

        document,

        "//SHORT-NAME"

    )


    assert result is not None