4. Run Simulation
autosar-codegen vehicle.arxml \
    --simulate
Python API Example
from autosar_codegen.cli.integration import (
    create_application,
)


app = create_application()


workspace = app.load_workspace(
    "vehicle.arxml"
)


app.validate(
    workspace
)


app.generate(
    workspace,
    "generated"
)

---

# 5. docs/development.md

```markdown
# Development Guide

## Project Structure


src/autosar_codegen/

├── core
├── model
├── xml
├── parser
├── resolver
├── generator
├── validator
├── simulator
└── cli


---

# Running Tests

Execute all tests:

```bash
pytest

Run specific module:

pytest tests/parser
Code Style

The project uses:

Black
Ruff
MyPy

Format:

black src tests

Lint:

ruff check .