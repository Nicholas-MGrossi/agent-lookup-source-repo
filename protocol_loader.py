"""
Load the operational and integrity protocol from this repository.
This protocol is the authoritative governance for the logic route and for structuring
agent output. The agent cannot derive truth; the user establishes whether content is truthful.
"""
import json
from pathlib import Path

_PROTOCOL_PATH = Path(__file__).resolve().parent / "protocol" / "protocol.json"


def load_protocol() -> dict:
    """Load and return protocol/protocol.json. Raises if missing or invalid JSON."""
    with open(_PROTOCOL_PATH, encoding="utf-8") as f:
        return json.load(f)


def get_operational_protocol(protocol: dict | None = None) -> dict:
    """Return the operational_protocol section. Loads protocol if not provided."""
    if protocol is None:
        protocol = load_protocol()
    return protocol.get("operational_protocol", {})


def get_integrity_protocol(protocol: dict | None = None) -> dict:
    """Return the integrity_protocol section. Loads protocol if not provided."""
    if protocol is None:
        protocol = load_protocol()
    return protocol.get("integrity_protocol", {})


def get_output_schema(protocol: dict | None = None) -> dict:
    """Return the output_schema section. Loads protocol if not provided."""
    if protocol is None:
        protocol = load_protocol()
    return protocol.get("output_schema", {})


def get_data_sources(protocol: dict | None = None) -> dict:
    """Return the data_sources section from operational_protocol.sourcing. Where the model must grab data from (functional retrieval targets)."""
    if protocol is None:
        protocol = load_protocol()
    op = protocol.get("operational_protocol", {})
    return op.get("sourcing", {}).get("data_sources", {})
