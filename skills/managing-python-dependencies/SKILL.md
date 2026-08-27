---
name: managing-python-dependencies
description: |
  Ensures proper Python dependency management, avoiding global `pip install` and
  adhering to project-specific tooling.

  Use this skill if any of the following are true:
    1. Attempting to run `pip install {package_name}`.
    2. Python packages or dependencies need to be added or modified.
    3. Initiating a new Python project.
    4. Creating a new notebook, even if just using BigQuery cells.
    5. Generating Python code that includes `import` statements for third-party libraries.
    6. Before executing Python scripts via the terminal to ensure the correct virtual environment is active.
license: Apache-2.0
metadata:
  version: v2
  publisher: google
---

# Python Dependency Management Rule

> [!CAUTION]
>
> **BEFORE any `pip install`**: You MUST first detect the project's existing
> dependency manager and use it correctly. Do NOT override the project's
> established tooling.

> [!NOTE]
>
> **Pre-Flight Environment Check Bundling**: You MUST NOT run multiple
> sequential 1-line shell check commands (e.g. separate commands for python
> version, pyspark version, auth check, pip list). Combine all pre-flight
> environment and package availability probes into a single composite python
> one-liner or shell check step. This bundling also applies to marker file
> detection; use a single `ls` or `find` command to check for all potential
> dependency manager files at once (e.g. `ls uv.lock poetry.lock Pipfile.lock
> requirements.txt pyproject.toml`).

## Dependency Manager Detection

Before installing ANY Python package, check the workspace for these files **in
priority order**:

1.  **Signal:** `uv.lock` or `pyproject.toml` with `[tool.uv]`
    *   **Tool:** **uv**
    *   **Install:** `uv add <package>`
    *   **Setup:** `uv sync`
2.  **Signal:** `pyproject.toml` with `[tool.poetry]`
    *   **Tool:** **Poetry**
    *   **Install:** `poetry add <package>`
    *   **Setup:** `poetry install`
3.  **Signal:** `Pipfile`
    *   **Tool:** **Pipenv**
    *   **Install:** `pipenv install <package>`
    *   **Setup:** `pipenv install`
4.  **Signal:** `environment.yml`
    *   **Tool:** **Conda**
    *   **Install:** `conda install <package>`
    *   **Setup:** `conda env create -f environment.yml`
5.  **Signal:** `requirements.txt` only
    *   **Tool:** **venv + pip**
    *   **Install:** `.venv/bin/pip install <package>`
    *   **Setup:** `.venv/bin/pip install -r requirements.txt`
6.  **Signal:** None of the above
    *   **Tool:** **venv + pip** (default)
    *   **Install:** `.venv/bin/pip install <package>`
    *   **Setup:** `.venv/bin/pip install -r requirements.txt`

## Default: venv + pip

If no dependency manager is detected, use **venv + pip + requirements.txt** as
the default:

```bash
# Initialize environment
python3 -m venv .venv

# Add dependencies
.venv/bin/pip install <package>

# Preserve state
.venv/bin/pip freeze > requirements.txt
```

**Rules for venv + pip workflow:**

-   Always use `.venv/bin/pip` or `.venv/bin/python` (explicit path).
-   After installing, run: `.venv/bin/pip freeze > requirements.txt`.
-   When setting up: `.venv/bin/pip install -r requirements.txt`.

## Prohibited

-   **NEVER** run `pip install` globally
-   **NEVER** override an existing dependency manager with a different one
