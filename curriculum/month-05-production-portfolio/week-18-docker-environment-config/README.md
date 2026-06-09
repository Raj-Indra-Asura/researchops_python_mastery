# Week 18 - Docker and Environment Configuration

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
