"""
autosar_codegen.core.constants
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Global constants used throughout the AUTOSAR Code Generator.

The goal of this module is to keep "magic strings" and
commonly used values centralized.

Supported AUTOSAR versions:
    - 4.2.2
    - 4.3.1
    - 4.4.0
"""

from __future__ import annotations

from enum import Enum
from pathlib import Path

###############################################################################
# Project Information
###############################################################################

PROJECT_NAME: str = "autosar-code-generator"

DEFAULT_ENCODING: str = "utf-8"

SUPPORTED_FILE_EXTENSION: str = ".arxml"

###############################################################################
# AUTOSAR
###############################################################################

SUPPORTED_AUTOSAR_VERSIONS: tuple[str, ...] = (
    "4.2.2",
    "4.3.1",
    "4.4.0",
)

###############################################################################
# Generator Languages
###############################################################################

class Language(str, Enum):
    """Supported output languages."""

    C = "c"

    CPP = "cpp"

###############################################################################
# Supported Networks
###############################################################################

class NetworkType(str, Enum):
    """Supported communication technologies."""

    CAN = "CAN"

    CANFD = "CANFD"

    FLEXRAY = "FLEXRAY"

    ETHERNET = "ETHERNET"

###############################################################################
# Byte Order
###############################################################################

class ByteOrder(str, Enum):

    LITTLE_ENDIAN = "little"

    BIG_ENDIAN = "big"

###############################################################################
# Logging
###############################################################################

DEFAULT_LOG_LEVEL: str = "INFO"

###############################################################################
# Project Directories
###############################################################################

ROOT_DIR = Path.cwd()

GENERATED_DIRECTORY = ROOT_DIR / "generated"

TEMPLATE_DIRECTORY = ROOT_DIR / "templates"

EXAMPLE_DIRECTORY = ROOT_DIR / "examples"

###############################################################################
# XML Tags
###############################################################################

SHORT_NAME = "SHORT-NAME"

LONG_NAME = "LONG-NAME"

UUID = "UUID"

ELEMENTS = "ELEMENTS"

SUB_PACKAGES = "SUB-PACKAGES"

AR_PACKAGE = "AR-PACKAGE"

AR_PACKAGES = "AR-PACKAGES"

###############################################################################
# Common AUTOSAR XML Element Names
###############################################################################

IMPLEMENTATION_DATA_TYPE = "IMPLEMENTATION-DATA-TYPE"

APPLICATION_PRIMITIVE_DATA_TYPE = "APPLICATION-PRIMITIVE-DATA-TYPE"

COMPU_METHOD = "COMPU-METHOD"

UNIT = "UNIT"

I_SIGNAL = "I-SIGNAL"

I_SIGNAL_GROUP = "I-SIGNAL-GROUP"

I_PDU = "I-PDU"

CAN_FRAME = "CAN-FRAME"

FLEXRAY_FRAME = "FLEXRAY-FRAME"

ETHERNET_CLUSTER = "ETHERNET-CLUSTER"

###############################################################################
# Default Values
###############################################################################

DEFAULT_PDU_LENGTH = 8

DEFAULT_CAN_DLC = 8

DEFAULT_TIMEOUT_MS = 100

DEFAULT_CYCLE_TIME_MS = 10