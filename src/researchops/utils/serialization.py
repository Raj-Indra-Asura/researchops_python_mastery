"""Serialization helpers for ResearchOps."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


def to_json(obj: Any, indent: int = 2) -> str:
    """Serialize an object to a JSON string, handling common types."""
    return json.dumps(obj, default=_default_encoder, indent=indent)


def from_json(text: str) -> Any:
    """Deserialize a JSON string."""
    return json.loads(text)


def _default_encoder(obj: Any) -> Any:
    """Extend json.JSONEncoder to handle datetime and Path objects."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, Path):
        return str(obj)
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")
