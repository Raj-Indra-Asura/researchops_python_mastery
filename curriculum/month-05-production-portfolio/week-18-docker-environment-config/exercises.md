# Exercises - Week 18 Docker and Environment Configuration

## Warm-up exercises
1. Write a minimal Dockerfile for a Python command.
2. Define one settings class with defaults.
3. Override one setting with an environment variable.
4. Create a `.env.example` documenting expected keys.

## Project exercises
1. Build a Docker image for ResearchOps.
2. Add a compose file for local API or worker startup.
3. Refactor config loading into a settings module.
4. Write tests for default settings and env-var overrides.

## Stretch exercises
1. Add separate compose services for API and worker.
2. Mount a local data volume into the container.
3. Add a production-oriented non-root container user.

## Writing questions
1. What belongs in env vars versus source code?
2. Which setting would be most dangerous to hard-code?
3. How did Docker reveal missing assumptions in your app?
4. Why should `.env.example` exist even if you use defaults?
