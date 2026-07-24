"""
Tests package parser.
"""

from autosar_codegen.parser.package import (
    PackageParser,
)



def test_package_parser_creation():

    parser = PackageParser()

    assert parser is not None



def test_package_parser_name():

    parser = PackageParser()

    assert parser.name == "package"