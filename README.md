## 🛠️ For Developers

This project is structured using [PEP 621](https://peps.python.org/pep-0621/) with a modern `pyproject.toml` and a `src/` layout. It includes code formatting, static type checking, and pre-commit hooks to ensure consistency.

### 🔧 Setup Instructions

1. **Install in dev mode (with all tools)**  
   You'll need Python 3.10+ and `pip`.

   ```bash
   pip install .[dev]
   ```

2. **Install pre-commit hooks (runs checks before every commit)**

   ```bash
   pre-commit install
   ```

3. **Run checks manually**

   ```bash
   black .           # Format code
   mypy . --strict   # Type check
   ```

4. **Run the app (if using CLI entry point)**

   ```bash
   factorio-preview  # Or use: python -m your_main_module
   ```

> 🧪 All commits will be automatically checked with [Black](https://black.readthedocs.io/) and [mypy](http://mypy-lang.org/) via pre-commit hooks.
