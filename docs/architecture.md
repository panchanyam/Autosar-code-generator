# Architecture Overview

## High Level Design

AUTOSAR CodeGen is designed as a layered processing pipeline.

             CLI

              |
              v

      Application Layer

              |
    +---------+---------+

    |                   |

 Parser              Validator

    |

    v

 Resolver

    |

    v

  Model

    |

+------+-------+

| |

Generator Simulator


---

# Core Layers

## XML Layer

Location:


src/autosar_codegen/xml


Responsibilities:

- XML loading
- Namespace handling
- XPath processing
- Tree traversal
- Cache management


---

## Model Layer

Location:


src/autosar_codegen/model


Contains:

- Workspace
- Datatypes
- Signals
- PDUs
- Frames
- Networks

---

## Parser Layer

Location:


src/autosar_codegen/parser


Transforms:


ARXML → Model Objects


---

## Resolver Layer

Location:


src/autosar_codegen/resolver


Responsibilities:

- Reference resolution
- Dependency linking
- Symbol lookup

---

## Generator Layer

Location:


src/autosar_codegen/generator


Transforms:


Model → Source Code


Current target:


C language


---

## Simulator Layer

Location:


src/autosar_codegen/simulator


Provides:

- ECU simulation
- Signal flow
- PDU communication
- Network execution