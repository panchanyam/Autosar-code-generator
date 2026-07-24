# AUTOSAR Code Generator

A production-grade AUTOSAR ARXML parser and C/C++ code generator.

## Features

- AUTOSAR 4.2.2
- AUTOSAR 4.3.1
- AUTOSAR 4.4.0

### Supported Networks

- CAN
- CAN FD
- FlexRay
- Ethernet

### Generated Code

- C
- C++17

### Generated Artifacts

- PDU
- Signal
- Signal Groups
- Frames
- Metadata
- Encoder
- Decoder
- Validation
- Simulation APIs

---

## Architecture

```
ARXML

↓

Parser

↓

Intermediate Representation

↓

Generators

↓

C/C++

JSON

DBC

HTML
```

---

## Build

```bash
pip install -e .
```

---

## Run

```bash
autosar-codegen --help
```

---

## Project Status

Development Started

Version 0.1.0