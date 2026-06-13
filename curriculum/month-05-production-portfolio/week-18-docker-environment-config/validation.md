
<!-- QUICKREF -->
## ⚡ Quick Commands

| Command | Purpose |
|---------|--------|
| `python -m pip install -e ".[dev]"` | Install / update dependencies |
| `researchops --help` | CLI smoke test |
| `pytest -q` | Run full test suite |
| `ruff check src tests` | Lint check |

*Full commands for Week 18 are in the [Commands to run](#commands-to-run) section below.*

<!-- QUICKREF_END -->
<!-- NAV_START -->
---
[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)

**Week 18 — Docker and Environment Config:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

---
<!-- NAV_END -->

# Validation — Week 18 Docker and Environment Configuration

## 1. Pre-validation checklist

- [ ] `.[dev,api,storage]` is installed in an active virtual environment.
- [ ] The app reads configuration from environment variables (a settings module).
- [ ] Only `.env.example` is committed; real `.env` secrets are git-ignored.
- [ ] The app already runs correctly **locally** before you trust the container.

## 2. Exact commands

Use Windows PowerShell as the primary local workflow. Docker on Windows requires Docker Desktop to be installed and running.

### Windows PowerShell — primary

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev,api,storage]"
ruff check src tests
pytest tests/unit/test_settings.py -v
# Confirm the app works locally FIRST:
researchops --help
docker build -t researchops:local .
docker compose up --build      # Ctrl-C to stop
# Secret hygiene, written in Python so it is cross-platform:
python -c "import subprocess; ignored = subprocess.run(['git', 'check-ignore', '.env'], capture_output=True, text=True); print('.env is ignored (good)' if ignored.returncode == 0 else 'WARNING: .env is not ignored'); tracked = subprocess.run(['git', 'ls-files', '.env'], capture_output=True, text=True); print('DANGER: .env tracked' if tracked.stdout.strip() else 'no real .env tracked (good)')"
```

### macOS / Linux alternative

```bash
source .venv/bin/activate
python -m pip install -e ".[dev,api,storage]"
ruff check src tests
pytest tests/unit/test_settings.py -v
researchops --help
docker build -t researchops:local .
docker compose up --build      # Ctrl-C to stop
python -c "import subprocess; ignored = subprocess.run(['git', 'check-ignore', '.env'], capture_output=True, text=True); print('.env is ignored (good)' if ignored.returncode == 0 else 'WARNING: .env is not ignored'); tracked = subprocess.run(['git', 'ls-files', '.env'], capture_output=True, text=True); print('DANGER: .env tracked' if tracked.stdout.strip() else 'no real .env tracked (good)')"
```

## 3. Expected behavior

- Settings tests pass; configuration comes from the environment.
- The image builds and the container starts with documented env vars.
- The containerized app behaves the same as the local app.

## 4. Tests that must pass

- `tests/unit/test_settings.py`
- `pytest -q` (whole suite)

## 5. Manual checks

- Override a setting via an env var and confirm the app picks it up.
- Start the container and exercise a real command/endpoint.
- Grep the repo for committed secrets (keys, tokens) and confirm none exist.

## 6. Architecture checks

- A single settings module centralises configuration; secrets are not hard-coded.
- Build-time concerns (image contents) and runtime concerns (env vars) are
  clearly separated.

## 7. Documentation checks

- `.env.example` lists every required variable with safe placeholder values.
- `notes.md` explains image vs container and build-time vs runtime config.

## 8. Do-not-proceed warnings

**Do not proceed to Week 19 if:**

- **Docker hides a broken local setup** — the app must work locally first; the
  container is not a way to paper over breakage.
- **`.env` secrets are committed** — only `.env.example` belongs in Git.

## 9. Ruthless mentor checkpoint

- "Does the app run locally without Docker? Prove it before we discuss the
  container."
- "Show me `git ls-files` — is any real `.env` or secret tracked?"
- "Change one setting via an environment variable. Did the app honor it?"

## 10. Definition of done

- [ ] Settings module reads config from the environment; tests pass.
- [ ] `.env.example` exists and is safe; real `.env` is git-ignored.
- [ ] No secrets are committed.
- [ ] Dockerfile builds; `docker compose up` starts the app.
- [ ] The container matches local behavior (it does not mask local breakage).
- [ ] `pytest -q` passes; `ruff` clean.
- [ ] You can explain build-time vs runtime config.
<!-- NAV_BOTTOM_START -->
---
⬅️ [← Break It](break_it.md) · ➡️ [Reflection →](reflection.md)

**Week 18 — Docker and Environment Config:** [README](README.md) · [Notes](notes.md) · [Exercises](exercises.md) · [Break It](break_it.md) · **Validation** · [Reflection](reflection.md)

[🏠 Home](../../../README.md) · [🗺 Roadmap](../../../ROADMAP.md) · [📋 Syllabus](../../../SYLLABUS.md) · [🗂 Curriculum Map](../../NAVIGATION.md) · [📅 Month 5: Production and Portfolio](../README.md)
---
<!-- NAV_BOTTOM_END -->
