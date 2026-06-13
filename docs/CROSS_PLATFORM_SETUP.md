# Cross-Platform Setup Guide — Windows First

ResearchOps is designed so a learner can work from a Windows PC, a Mac, or a Linux machine without changing the project code. The main difference between platforms is the shell command used to activate the Python virtual environment. After the environment is active, most commands are identical.

Use this guide whenever a weekly file says to run commands from the repository root.

---

## 1. Recommended Windows workflow

Use **Windows PowerShell** as the primary shell.

```powershell
# 1. Move into the cloned repository
cd researchops_python_mastery

# 2. Create a local virtual environment
python -m venv .venv

# 3. Activate the virtual environment
.\.venv\Scripts\Activate.ps1

# 4. Upgrade pip inside the virtual environment
python -m pip install --upgrade pip

# 5. Install ResearchOps with development tools
python -m pip install -e ".[dev]"

# 6. Confirm the CLI works
researchops --help

# 7. Run tests and linting
pytest -q
ruff check src tests
```

### What those Windows commands mean

- `python -m venv .venv` creates a private Python environment in the `.venv` folder.
- `.\.venv\Scripts\Activate.ps1` tells PowerShell to use the Python and packages from that private environment.
- `python -m pip install -e ".[dev]"` installs this repository in editable mode, so changes under `src/researchops` are immediately used by the `researchops` command.
- `pytest -q` runs the test suite.
- `ruff check src tests` checks code style and common Python mistakes.

### If PowerShell blocks activation

If you see a message about scripts being disabled, run this once for your Windows user account:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Then close and reopen PowerShell, return to the repository, and run:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 2. Windows Command Prompt alternative

If you prefer Command Prompt instead of PowerShell, only the activation command changes.

```cmd
cd researchops_python_mastery
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
researchops --help
pytest -q
ruff check src tests
```

---

## 3. Windows Git Bash alternative

If you installed Git for Windows and prefer Git Bash, activation looks more like macOS/Linux but uses the Windows `Scripts` folder.

```bash
cd researchops_python_mastery
python -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
researchops --help
pytest -q
ruff check src tests
```

---

## 4. macOS and Linux workflow

On macOS and Linux, use Terminal.

```bash
cd researchops_python_mastery
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
researchops --help
pytest -q
ruff check src tests
```

If your system command is `python3` instead of `python`, use `python3 -m venv .venv` and `python3 -m pip ...`.

---

## 5. Commands that are the same on all platforms

Run these after the virtual environment is active:

```text
python -m pip install -e ".[dev]"
researchops --help
researchops scan examples/sample_papers
pytest -q
pytest --cov=researchops --cov-report=term-missing -q
ruff check src tests
```

The command text is the same in PowerShell, Command Prompt, Git Bash, macOS Terminal, and Linux shells.

---

## 6. Path examples

Python code in this repository uses `pathlib.Path`, which understands Windows and Unix paths.

| Situation | Windows example | macOS/Linux example |
|----------|-----------------|---------------------|
| Virtual environment activation | `.\.venv\Scripts\Activate.ps1` | `source .venv/bin/activate` |
| Relative project path | `examples\sample_papers` | `examples/sample_papers` |
| CLI path accepted by ResearchOps | `researchops scan examples/sample_papers` | `researchops scan examples/sample_papers` |

Forward slashes usually work in Python CLI arguments on Windows, so the curriculum normally uses paths like `examples/sample_papers` for readability.

---

## 7. Docker on Windows, Mac, and Linux

Week 18 introduces Docker. On Windows, install and start **Docker Desktop** before running Docker commands.

Use the modern Compose command when available:

```powershell
docker compose up --build
```

Older systems may use:

```powershell
docker-compose up --build
```

Both commands mean: build the containers if needed, then start the ResearchOps services.

---

## 8. Beginner troubleshooting checklist

If a command fails, check these in order:

1. Are you in the repository root, where `pyproject.toml` exists?
2. Is the virtual environment active? PowerShell should show `(.venv)` near the prompt.
3. Did you install the project with `python -m pip install -e ".[dev]"`?
4. Are you using Python 3.11 or newer?
5. Did you copy the command for your shell, not a different shell?
6. If `researchops` is not found, reinstall with `python -m pip install -e ".[dev]"` while the environment is active.

The goal is not to memorize every shell command. The goal is to understand which commands are platform-specific and which commands are project-specific.
