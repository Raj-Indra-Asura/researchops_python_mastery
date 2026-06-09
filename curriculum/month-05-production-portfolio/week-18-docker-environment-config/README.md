# Week 18 - Docker and Environment Configuration

<!-- NAV:TOP:START -->
> **You are here:** [🏠 Home](../../../README.md) › [🗺️ Roadmap](../../../ROADMAP.md) › [Month 5](../README.md) › **Week 18 — Docker & Environment Config**
>
> 📘 *ResearchOps reads like a book.* New here? Begin at the [root README](../../../README.md). Feeling lost? Open the [Roadmap](../../../ROADMAP.md).
<!-- NAV:TOP:END -->

## Learning objectives
- Build a Docker image for the ResearchOps application.
- Use environment variables for configuration instead of hard-coded values.
- Understand the difference between build-time and run-time config.
- Add a `docker-compose` setup for local development services.
- Keep secrets out of source control.
- Test configuration loading across CLI and API paths.
- Prepare the app for reproducible local deployment.

## Project milestone
Containerize ResearchOps and standardize environment-driven configuration for local development and deployment.

## Files to modify/create
- `Dockerfile`
- `docker-compose.yml`
- `.env.example`
- `src/researchops/settings.py`
- `tests/unit/test_settings.py`

## Concepts covered
Containers, images, environment variables, configuration management, `.env` conventions, and reproducible environments.

## Expected deliverables
- A working Dockerfile.
- Compose configuration for local services or app startup.
- A settings layer driven by env vars.
- Tests proving defaults and overrides work.

## Definition of done
- [ ] Docker image builds.
- [ ] App can run in a container.
- [ ] Settings read from environment variables.
- [ ] `.env.example` documents required config.
- [ ] Secrets are not committed.
- [ ] Settings tests pass.
- [ ] You can explain your runtime configuration strategy.

<!-- NAV:BOTTOM:START -->
---

## 🧭 Navigation

**Where am I?** Month 5 — Production and Portfolio · **Week 18 — Docker & Environment Config** · *Week overview (README)* (step 1 of 6 this week).

### ◀ Previous / Next ▶
- ◀ **Previous:** [Week 17 weekly report](../../../docs/weekly-reports/README.md)
- ▶ **Next:** [notes.md](./notes.md)

### Read this week in order
1. **➡ [Week overview (README)](./README.md) ← you are here**
2. [notes.md](./notes.md)
3. [exercises.md](./exercises.md)
4. [break_it.md](./break_it.md)
5. [validation.md](./validation.md)
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
