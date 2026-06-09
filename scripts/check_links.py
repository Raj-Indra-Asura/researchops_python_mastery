#!/usr/bin/env python3
"""
check_links.py — verify that every relative Markdown link in the repository
points to a file or directory that actually exists.

Usage:
    python scripts/check_links.py            # check entire repo
    python scripts/check_links.py path/to/   # check a subtree
    python scripts/check_links.py file.md    # check a single file

Exit codes:
    0  — no broken links found
    1  — one or more broken links found
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Matches [text](url) and ![alt](url) — capture the URL part
LINK_RE = re.compile(r"!?\[(?:[^\]]*)\]\(([^)]+)\)")

# Anchors embedded in links: file.md#section — strip the fragment before checking
FRAGMENT_RE = re.compile(r"^([^#]*)#.*$")


def collect_md_files(root: Path) -> list[Path]:
    """Yield all .md files under *root*, skipping hidden directories."""
    results: list[Path] = []
    for path in sorted(root.rglob("*.md")):
        # Skip .git and other hidden dirs
        if any(part.startswith(".") for part in path.parts):
            continue
        results.append(path)
    return results


def check_file(md_file: Path) -> list[str]:
    """Return a list of error strings for broken relative links in *md_file*."""
    errors: list[str] = []
    try:
        text = md_file.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"  cannot read {md_file}: {exc}"]

    for lineno, line in enumerate(text.splitlines(), start=1):
        for match in LINK_RE.finditer(line):
            url = match.group(1).strip()

            # Skip absolute URLs and mailto
            if url.startswith(("http://", "https://", "ftp://", "mailto:")):
                continue
            # Skip pure fragment links (#section)
            if url.startswith("#"):
                continue

            # Strip trailing fragment from the path portion
            frag_match = FRAGMENT_RE.match(url)
            path_part = frag_match.group(1) if frag_match else url

            if not path_part:
                continue  # pure fragment after stripping

            target = (md_file.parent / path_part).resolve()

            if not target.exists():
                rel_md = md_file.relative_to(REPO_ROOT)
                errors.append(f"  {rel_md}:{lineno}: broken link → {url}")

    return errors


def main(argv: list[str]) -> int:
    if argv:
        roots = [Path(a).resolve() for a in argv]
    else:
        roots = [REPO_ROOT]

    md_files: list[Path] = []
    for root in roots:
        if root.is_file() and root.suffix == ".md":
            md_files.append(root)
        elif root.is_dir():
            md_files.extend(collect_md_files(root))
        else:
            print(f"warning: skipping {root} (not a .md file or directory)", file=sys.stderr)

    if not md_files:
        print("No Markdown files found.")
        return 0

    all_errors: list[str] = []
    for md_file in md_files:
        errors = check_file(md_file)
        all_errors.extend(errors)

    if all_errors:
        print(f"Found {len(all_errors)} broken link(s):\n")
        print("\n".join(all_errors))
        return 1

    print(f"✅  Checked {len(md_files)} Markdown files — no broken links found.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
