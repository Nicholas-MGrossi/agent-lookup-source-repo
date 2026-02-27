"""
Functional data sources: where the model grabs data from.
Resolves local paths and loads file contents for non-conceptual retrieval.
"""
from __future__ import annotations

import json
from pathlib import Path

from protocol_loader import get_data_sources, load_protocol

_REPO_ROOT = Path(__file__).resolve().parent


def get_local_source_paths(repo_root: Path | None = None, protocol: dict | None = None) -> list[tuple[str, Path, str]]:
    """
    Return list of (source_id, absolute_path, description) for each local_paths entry.
    Use this to know exactly which files to read for retrieval.
    """
    repo_root = repo_root or _REPO_ROOT
    if protocol is None:
        protocol = load_protocol()
    ds = get_data_sources(protocol)
    local_paths = ds.get("local_paths", [])
    out = []
    for entry in local_paths:
        sid = entry.get("id", "")
        rel = entry.get("path", "")
        desc = entry.get("description", "")
        abs_path = (repo_root / rel).resolve()
        out.append((sid, abs_path, desc))
    return out


def load_local_sources(repo_root: Path | None = None, protocol: dict | None = None) -> dict[str, str | dict]:
    """
    Load content from each local data source. Returns dict: source_id -> content (string or parsed JSON).
    Functional: call this before or during generation so the model has actual data to cite.
    """
    repo_root = repo_root or _REPO_ROOT
    if protocol is None:
        protocol = load_protocol()
    paths = get_local_source_paths(repo_root, protocol)
    out = {}
    for sid, abs_path, _desc in paths:
        if not abs_path.exists():
            out[sid] = f"[missing: {abs_path}]"
            continue
        try:
            text = abs_path.read_text(encoding="utf-8")
            if abs_path.suffix.lower() == ".json":
                out[sid] = json.loads(text)
            else:
                out[sid] = text
        except Exception as e:
            out[sid] = f"[error reading {abs_path}: {e}]"
    return out


def get_retrieval_urls(protocol: dict | None = None) -> list[str]:
    """Return the list of retrieval URLs from data_sources (for remote fetch)."""
    if protocol is None:
        protocol = load_protocol()
    return get_data_sources(protocol).get("retrieval_urls", [])
