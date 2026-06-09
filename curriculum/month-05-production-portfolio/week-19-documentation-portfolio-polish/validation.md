# Week 19 Validation

## Commands to Run

```bash
# Fresh clone test
cd /tmp
git clone https://github.com/YOUR_USERNAME/researchops_python_mastery.git fresh_test
cd fresh_test
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
researchops --help

# Full test suite still passes
pytest

# Ruff still clean
ruff check src tests
```

## Checklist

- [ ] README renders correctly on GitHub (images, code blocks, tables)
- [ ] All Mermaid diagrams render on GitHub
- [ ] `docs/demo.md` produces correct output when followed step by step
- [ ] Fresh clone + install + `researchops --help` works
- [ ] `pytest` still passes
- [ ] `ruff check` still clean
- [ ] `docs/retrospective.md` is written and honest
