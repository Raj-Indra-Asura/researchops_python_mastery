# Break It - Week 18 Docker and Environment Configuration

## Intentional failure experiments
1. Build the image without copying one required source directory.
2. Set an invalid database URL or missing required env var.
3. Commit a fake secret into `.env.example` and then remove it after reflecting on the risk.
4. Change the container command to a nonexistent module path.
5. Run compose without mounting the expected data directory.

## Debugging tasks
- Inspect container logs after startup failure.
- Print loaded settings at startup in a safe, non-secret way.
- Run `pytest -k settings -v` after config changes.

## Edge cases to explore
- Missing optional env vars.
- Relative versus absolute volume paths.
- Different port mappings.
- Read-only container file systems.

## What did you learn?
- Which config mistake was hardest to spot?
- What should never be committed?
- How will you document runtime requirements clearly?
