# Validation — Week 18 Docker and Environment Configuration

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 5](../README.md) › [Week 18 — Docker & Environment Config](./README.md) › **validation.md**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

## 1. Pre-validation checklist

- [ ] `.[dev,api,storage]` is installed in an active virtual environment.
- [ ] The app reads configuration from environment variables (a settings module).
- [ ] Only `.env.example` is committed; real `.env` secrets are git-ignored.
- [ ] The app already runs correctly **locally** before you trust the container.

## 2. Exact commands

```bash
source .venv/bin/activate
python -m pip install -e ".[dev,api,storage]"
ruff check src tests
pytest tests/unit/test_settings.py -v
# Confirm the app works locally FIRST:
researchops --help
docker build -t researchops:local .
docker compose up --build      # Ctrl-C to stop
# Secret hygiene:
git check-ignore .env && echo ".env is ignored (good)"
git ls-files | grep -E "(^|/)\.env$" && echo "DANGER: .env tracked" || echo "no real .env tracked (good)"
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

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 5 — Production and Portfolio · **Week 18 — Docker & Environment Config** · *validation.md — the checkpoint* (step 5 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [break_it.md](./break_it.md)
- ▶ **Next:** [reflection.md](./reflection.md)

### Read this week in order
1. [Week overview (README)](./README.md)
2. [notes.md](./notes.md)
3. [exercises.md](./exercises.md)
4. [break_it.md](./break_it.md)
5. **➡ [validation.md](./validation.md) ← you are here**
6. [reflection.md](./reflection.md)
7. [Write your weekly report](../../../docs/weekly-reports/README.md)
8. [Next week → Week 19](../../../curriculum/month-05-production-portfolio/week-19-documentation-portfolio-polish/README.md)

### Optional paths — where to go if…
- 😕 **Confused by the concepts?** → [notes.md](./notes.md)
- ✍️ **Want hands-on practice?** → [exercises.md](./exercises.md)
- 💥 **Tests fail / want to understand failure?** → [break_it.md](./break_it.md)
- ✅ **Think you are done?** → [validation.md](./validation.md)
- 🪞 **Validation passed?** → [reflection.md](./reflection.md)
- 📓 **Reflection complete?** → [Write your weekly report](../../../docs/weekly-reports/README.md)
- 🚀 **Weekly report done?** → [Start Week 19 — Documentation & Portfolio Polish](../../../curriculum/month-05-production-portfolio/week-19-documentation-portfolio-polish/README.md)

### Stuck? Do this
1. Re-read this week's [notes.md](./notes.md) slowly.
2. Reproduce the failure modes in [break_it.md](./break_it.md).
3. Re-run the [validation checklist](./validation.md).
4. Zoom out to the [Month 5 overview](../README.md) or the [Roadmap](../../../ROADMAP.md).

### Global navigation
[🏠 Home](../../../README.md) · [🗺️ Roadmap](../../../ROADMAP.md) · [📚 Syllabus](../../../SYLLABUS.md) · [📦 Month 5 overview](../README.md) · [📄 Week 18 README](./README.md)

*Returning later? The [Roadmap](../../../ROADMAP.md) is always your map back to the main path through all 20 weeks.*
<!-- NAV:BOTTOM:END -->
