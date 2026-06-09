# Validation - Week 18 Docker and Environment Configuration

## Exact shell commands to run
```bash
source .venv/bin/activate
python -m pip install -e ".[dev,api,storage]"
pytest tests/unit/test_settings.py -v
docker build -t researchops:local .
docker compose up --build
```

## Expected outputs
- Settings tests pass.
- Docker image builds successfully.
- Compose starts the configured service(s) with documented environment variables.

## Pytest commands and expected results
```bash
pytest -k settings -v
pytest -q
```

Expected result: the app reads configuration from environment variables, container startup is reproducible, and the repository includes enough configuration documentation to boot the system locally.

## Completion checklist
- [ ] Dockerfile exists.
- [ ] Compose file exists.
- [ ] Settings module exists.
- [ ] `.env.example` exists and is safe.
- [ ] Secrets are excluded from version control.
- [ ] Settings override tests pass.
- [ ] Docker image builds.
- [ ] Containerized app starts.
- [ ] `pytest -q` passes.
- [ ] You can explain build-time vs runtime config.
