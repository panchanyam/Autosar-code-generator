# Installation Guide

## Requirements

Recommended:

- Python >= 3.11
- pip
- virtual environment


## Clone Repository

```bash
git clone <repository-url>

cd autosar-codegen
Create Virtual Environment

Linux/macOS:

python3 -m venv .venv

source .venv/bin/activate

Windows:

python -m venv .venv

.venv\Scripts\activate
Install Package

Development installation:

pip install -e .

Install development tools:

pip install -e ".[dev]"
Verify Installation

Run:

autosar-codegen --version

Expected:

1.0.0

---

# 4. docs/quickstart.md

```markdown
# Quick Start

## 1. Prepare ARXML

Example:


vehicle.arxml


---

## 2. Validate Input

```bash
autosar-codegen vehicle.arxml --validate