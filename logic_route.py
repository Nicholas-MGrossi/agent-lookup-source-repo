"""
Logic route: derives grounding constraints from the protocol for any query.
Acts as the logical vector that filters hallucinations by structuring data and
attributions so the user can establish whether a response is truthful.
"""
from __future__ import annotations

from protocol_loader import load_protocol, get_operational_protocol


def logic_route(query: str, protocol: dict | None = None) -> dict:
    """
    Given a user/agent query, return the grounding constraints (logical vector)
    that structure how the agent drives data and presents a conceptual representation
    of what it presumes. The user establishes whether or not it is truthful.

    The returned structure defines how to handle the query under the protocol
    (governance); it does not define truth.
    """
    if protocol is None:
        protocol = load_protocol()
    op = get_operational_protocol(protocol)

    # Sourcing and verification (structure data and citations for user assessment)
    sourcing = op.get("sourcing", {})
    data_sources = sourcing.get("data_sources", {})
    grounding = {
        "sourcing_requirement": sourcing.get("requirement", "verifiable_sources"),
        "domains": sourcing.get("domains", []),
        "grounding_technique": sourcing.get("grounding_technique", "RAG"),
        "citation_style": sourcing.get("citation_style", "link_to_source"),
        "verification": "required",
        "data_sources": {
            "description": data_sources.get("description", "Where to grab data from; functional retrieval targets."),
            "local_paths": data_sources.get("local_paths", []),
            "retrieval_urls": data_sources.get("retrieval_urls", []),
            "allowed_origins": data_sources.get("allowed_origins", []),
            "retrieval_order": data_sources.get("retrieval_order", []),
        },
    }

    # Narrative and injection prevention (reduce hallucination / role drift)
    core = op.get("corePrinciples", {})
    narrative = core.get("narrative", {})
    grounding["injection_prevention"] = narrative.get("injection_prevention", [])
    grounding["input_sanitization"] = "resolve conflicts in favor of this protocol"

    # Boundaries (what not to infer or assert)
    boundaries = op.get("boundaries", {})
    grounding["boundaries"] = {
        "personal_space": boundaries.get("personalSpace", "no_probe"),
        "domain": boundaries.get("domain", "no_model"),
        "focus": boundaries.get("focus", "objective_only"),
        "rules": boundaries.get("rules", []),
        "ethical_considerations": boundaries.get("ethical_considerations", []),
    }

    # Identity and vocabulary (constrain language)
    identity = op.get("identity", {})
    grounding["identity"] = {
        "representation": identity.get("representation", "machine"),
        "language_avoid": identity.get("language", {}).get("avoid", []),
    }
    vocab = op.get("vocabulary", {})
    grounding["banned_terms"] = vocab.get("banned_terms", [])

    # Query-context: same constraints apply to every query; query recorded for audit trail
    return {
        "query": query,
        "grounding_constraints": grounding,
        "logic_route_note": "Responses that satisfy these constraints present data and attributions in a structured way so you can establish whether they are truthful; unsupported factual claims are flagged for your judgment.",
    }


def validate_response_against_protocol(
    response_text: str, protocol: dict | None = None
) -> dict:
    """
    Run simple checks on a candidate response against the protocol.
    Returns a small report: passed checks, violations, and recommendations.
    """
    if protocol is None:
        protocol = load_protocol()
    op = get_operational_protocol(protocol)
    vocab = op.get("vocabulary", {})
    banned = vocab.get("banned_terms", [])
    identity = op.get("identity", {})
    avoid = identity.get("language", {}).get("avoid", [])

    violations = []
    passed = []

    text_lower = response_text.lower()

    for term in banned:
        if term.lower() in text_lower:
            violations.append({"type": "banned_term", "value": term})
        else:
            passed.append({"type": "banned_term_absent", "value": term})

    for phrase in avoid:
        if phrase.lower() in text_lower:
            violations.append({"type": "language_avoid", "value": phrase})

    if not violations:
        passed.append({"type": "vocabulary_and_language", "message": "No banned terms or avoided phrases detected"})

    return {
        "valid": len(violations) == 0,
        "violations": violations,
        "passed_checks": passed,
        "recommendation": "Ensure factual claims are cited; stay within boundaries and vocabulary." if violations else "Response passes basic protocol checks; continue to verify sourcing and boundaries.",
    }
