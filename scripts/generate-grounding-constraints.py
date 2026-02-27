#!/usr/bin/env python3
"""
Generate .well-known/grounding-constraints.json from the protocol.
This file is URL-addressable so providers (e.g. Gemini on your phone) can
fetch it and apply the same logic route as the local system.
"""
import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

from logic_route import logic_route
from protocol_loader import load_protocol

OUTPUT_PATH = root / ".well-known" / "grounding-constraints.json"
CANONICAL_QUERY = "Apply these grounding constraints to every query. Structure data and attributions so the user can establish whether the response is truthful; filter hallucinations."


def main():
    protocol = load_protocol()
    result = logic_route(CANONICAL_QUERY, protocol)
    # Add a stable URL hint for clients (e.g. mobile) that fetch this file
    result["_meta"] = {
        "description": "Grounding constraints (logic route) for Agent Lookup Source Repo. Structure data and attributions; the user establishes truthfulness. Includes data_sources (where the model must grab data from).",
        "usage": "Point your agent or provider (e.g. Gemini) at this URL so answers follow the same protocol as the repo.",
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
