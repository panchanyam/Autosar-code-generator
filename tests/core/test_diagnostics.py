"""
Tests for diagnostic framework.
"""

from autosar_codegen.core.diagnostics import (
    Diagnostic,
    Severity,
    Category,
)



def test_create_diagnostic():

    diagnostic = Diagnostic(

        message="Test error",

        severity=Severity.ERROR,

        category=Category.PARSER,

    )


    assert diagnostic.message == (
        "Test error"
    )


    assert diagnostic.severity == (
        Severity.ERROR
    )



def test_diagnostic_location():

    diagnostic = Diagnostic(

        message="Invalid XML",

        severity=Severity.ERROR,

        category=Category.XML,

    )


    diagnostic.location = (

        "vehicle.arxml"

    )


    assert diagnostic.location == (
        "vehicle.arxml"
    )



def test_warning_diagnostic():

    diagnostic = Diagnostic(

        message="Deprecated attribute",

        severity=Severity.WARNING,

        category=Category.VALIDATION,

    )


    assert diagnostic.severity == (
        Severity.WARNING
    )