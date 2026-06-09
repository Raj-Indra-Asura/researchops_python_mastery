# Notes - Week 18 Docker and Environment Configuration

Docker helps you package an application with its runtime environment so it behaves more consistently across machines. A Docker image is a built artifact. A container is a running instance of that image.

A simple Python Dockerfile often:
1. starts from a Python base image
2. sets a working directory
3. copies dependency metadata
4. installs dependencies
5. copies application code
6. defines a command

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .
CMD ["researchops", "--help"]
```

Layer order matters because it affects build caching. If dependencies change rarely, copy dependency files before application code so Docker can reuse cached install layers.

Environment variables are a standard way to configure behavior without editing code. For example, the database path or API host should not be hard-coded. Libraries like `pydantic-settings` make this comfortable.

```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///researchops.db"
    log_level: str = "INFO"
```

At runtime, environment variables can override defaults. This keeps the same code usable in development, tests, and containers.

A `.env.example` file documents required settings without containing real secrets. Real secrets should come from the actual environment or a secure secret manager, not from committed files.

`docker-compose.yml` is useful for local orchestration. Even if ResearchOps starts as one container, compose can define environment variables, mounted volumes, and extra services. It also gives teammates a repeatable startup command.

Be clear about build-time versus run-time configuration. A build-time value becomes part of the image. A run-time value is provided when the container starts. Database paths, API keys, and ports are usually runtime concerns.

Testing settings is worth doing. A small test can confirm that defaults are sensible and that environment overrides work correctly. This is especially important because configuration bugs often appear only after deployment, when they are more frustrating to debug.

Containerization is not only about shipping. It also forces you to think clearly about application boundaries: what files must exist, which settings are required, and what command starts the app. That clarity improves the project even before any real deployment happens.
