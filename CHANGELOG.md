# Changelog

All notable changes to ResearchOps will be documented here.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

---

## [Unreleased]

### Added
- Initial project scaffold
- Core domain models: `Paper`, `ParsedDocument`, `IngestionResult`, `FailedDocument`, `SearchResult`
- Custom exception hierarchy
- `typing.Protocol` interfaces for `PaperRepository`, `DocumentParser`, `SearchEngine`
- `researchops scan PATH` CLI command
- Keyword search service (in-memory)
- SQLite paper repository (schema + implementation)
- Typer-based CLI with subcommand groups
- pytest + ruff setup
- CI workflow (GitHub Actions)
- 20-week curriculum scaffold
