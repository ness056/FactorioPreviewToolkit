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


## 🌍 Host the Viewer with GitHub Pages

You can host your own copy of the Factorio Map Viewer using GitHub Pages. Here’s how:

### ✅ Step 1: Fork This Repository

Make sure you’re logged in at [github.com](https://github.com).

- Go to **[https://github.com/AntiElitz/FactorioPreviewToolkit](https://github.com/AntiElitz/FactorioPreviewToolkit)**.
- In the top-right of the page, click **“Fork”**.
- Choose your GitHub account to fork it into.
- You now have your own copy of the repository.

### 🛠️ Step 2: Enable GitHub Pages for the Viewer

- Go to your new **forked repository**.
- Click the **“Settings”** tab.
- In the left sidebar, click **“Pages”**.
- Under **“Source”**, select:
  - **Branch:** `main`
  - **Folder:** `/viewer`
- Click **“Save”**.

### 🎉 Done!

GitHub will provide you with a link like:
https://your-username.github.io/FactorioPreviewToolkit/


Open that link in your browser to view your hosted preview!

> ℹ️ GitHub Pages works only for **public repositories**. Your fork is public by default unless you changed it.


