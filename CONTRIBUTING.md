# 🛠️ Contributing to Factorio Preview Toolkit

Thank you for your interest in contributing! This toolkit helps automate the generation of map previews for Factorio speedrunners. Whether you're fixing bugs, improving the UI, adding features, or updating documentation — we welcome all contributions.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/AntiElitz/FactorioPreviewToolkit.git
cd FactorioPreviewToolkit
```

### 2. Set Up a Virtual Environment

We recommend using a virtual environment to isolate dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Development Dependencies

Install everything needed for development, testing, and building:

```bash
pip install .[dev]
```

If you're on Linux or macOS and using GUI features (like tkinter), you may need to manually install additional system packages (e.g. `sudo apt install python3-tk` on Debian/Ubuntu).

---

## 💻 Running the Toolkit Locally

To launch the main tool, use the following command **from the project root**:

```bash
python -m src.FactorioPreviewToolkit
```

This ensures Python locates the main module correctly inside the `src` directory.

---

## 🛠️ Building a Standalone Executable

You can generate a one-file executable using PyInstaller by running:

```bash
python -m toolkit_build.build
```

This creates a zipped bundle with platform-specific binaries, configurations, and a viewer UI, ready to distribute.


## 🧪 Formatting, Linting, and Type Checking

This project uses:

- [`black`](https://black.readthedocs.io/) for auto-formatting
- [`mypy`](http://mypy-lang.org/) for static type checking
- [`pre-commit`](https://pre-commit.com/) for running checks before each commit

### Set up the pre-commit hooks:

```bash
pre-commit install
```

### Run all checks manually:

```bash
pre-commit run --all-files
```

---

## 🏗️ Project Structure

```
toolkit_build/               → Build and release logic (zip, PyInstaller, tag push)
src/FactorioPreviewToolkit/  → Main application logic
viewer/                      → HTML/JS map viewer (Zoom, Tabs, Dropbox URLs)
.github/workflows/           → GitHub Actions (CI for cross-platform builds)
```

---

## 🚢 Releasing

Use the release command to:

- Bump the version
- Build the executable
- Tag the release
- Push to GitHub (which triggers the cross-platform build pipeline)

```bash
python -m toolkit_build.release
```

This triggers GitHub Actions to build the toolkit for Windows, Linux, and macOS and (if configured) attach the zip files to a GitHub release.

---

## 🌐 Contributing to the Viewer

The HTML+JS viewer is located in the `viewer/` folder. It supports:

- Dynamic tab generation
- Zoom & pan
- Dropbox-compatible preview image URLs
- Local + remote planet name loading via `.js` or `.json`

You can test it by opening `viewer/index.html` in a browser (local file access works).

---

## ❤️ How to Contribute

1. Fork this repository
2. Create a new branch: `git checkout -b my-fix`
3. Make your changes
4. Run lint/type checks
5. Push to your fork and open a Pull Request

---

## 🧩 Need Help?

- Open an [Issue](https://github.com/AntiElitz/FactorioPreviewToolkit/issues)
- Or start a [Discussion](https://github.com/AntiElitz/FactorioPreviewToolkit/discussions)
- Or ping @AntiElitz on GitHub

Thanks for making this toolkit better!
