#!/usr/bin/env python3
"""Development environment setup script.

Run once after cloning:
    python scripts/setup_dev.py
"""

import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> None:
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}")
        sys.exit(result.returncode)


def main() -> None:
    root = Path(__file__).parent.parent

    print("=== ResearchOps Dev Setup ===\n")

    # Create data directory
    data_dir = root / "data"
    data_dir.mkdir(exist_ok=True)
    print(f"✓ Created {data_dir}\n")

    # Create .env if it doesn't exist
    env_file = root / ".env"
    if not env_file.exists():
        example = root / ".env.example"
        if example.exists():
            env_file.write_text(example.read_text())
            print("✓ Copied .env.example → .env\n")

    # Install dev dependencies
    run([sys.executable, "-m", "pip", "install", "-e", ".[dev]"])
    print()

    print("=== Setup complete ===")
    print("\nNext steps:")
    print("  researchops --help")
    print("  pytest")


if __name__ == "__main__":
    main()
