"""
autosar_codegen.core.exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Custom exceptions used throughout the AUTOSAR Code Generator.

Every module should raise one of these exceptions instead of
using generic Python exceptions.
"""

from __future__ import annotations


class AutosarCodeGeneratorError(Exception):
    """
    Base exception for the project.
    """

    pass


###############################################################################
# Configuration
###############################################################################

class ConfigurationError(AutosarCodeGeneratorError):
    """
    Raised when configuration is invalid.
    """

    pass


###############################################################################
# XML
###############################################################################

class InvalidArxmlError(AutosarCodeGeneratorError):
    """
    Raised when an ARXML file is invalid.
    """

    pass


class UnsupportedAutosarVersionError(AutosarCodeGeneratorError):
    """
    Raised when an unsupported AUTOSAR version is detected.
    """

    pass


###############################################################################
# Reference Resolver
###############################################################################

class ReferenceResolutionError(AutosarCodeGeneratorError):
    """
    Raised when a REF cannot be resolved.
    """

    def __init__(self, reference: str):

        super().__init__(f"Unable to resolve reference: {reference}")

        self.reference = reference


class DuplicateReferenceError(AutosarCodeGeneratorError):
    """
    Duplicate AUTOSAR path.
    """

    def __init__(self, path: str):

        super().__init__(f"Duplicate AUTOSAR path: {path}")

        self.path = path


###############################################################################
# Parser
###############################################################################

class ParserError(AutosarCodeGeneratorError):
    """
    Base parser error.
    """

    pass


class UnsupportedElementError(ParserError):
    """
    Unsupported XML element.
    """

    def __init__(self, element: str):

        super().__init__(f"Unsupported AUTOSAR element: {element}")

        self.element = element


###############################################################################
# Generator
###############################################################################

class GeneratorError(AutosarCodeGeneratorError):
    """
    Base generator exception.
    """

    pass


class TemplateNotFoundError(GeneratorError):
    """
    Missing Jinja2 template.
    """

    def __init__(self, template: str):

        super().__init__(f"Template not found: {template}")

        self.template = template


###############################################################################
# Validation
###############################################################################

class ValidationError(AutosarCodeGeneratorError):
    """
    Validation failed.
    """

    pass


class SignalValidationError(ValidationError):
    """
    Invalid signal definition.
    """

    pass


class PduValidationError(ValidationError):
    """
    Invalid PDU definition.
    """

    pass