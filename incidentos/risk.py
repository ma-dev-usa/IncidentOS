from typing import Any

from incidentos.models import IncidentClassification

RISK_ORDER = {
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 3,
}


def score_release_risk(classification: IncidentClassification) -> dict[str, Any]:
    if classification.severity == "HIGH":
        return {
            "risk": "HIGH",
            "should_block_release": True,
            "reasons": [
                f"Root cause: {classification.root_cause}",
                f"Root service: {classification.root_service}",
                f"Scenario: {classification.scenario}",
            ],
        }

    if classification.severity == "MEDIUM":
        return {
            "risk": "MEDIUM",
            "should_block_release": False,
            "reasons": [
                "Incident detected but severity is below automatic release-block threshold.",
                f"Scenario: {classification.scenario}",
            ],
        }

    return {
        "risk": "LOW",
        "should_block_release": False,
        "reasons": [
            "Replay did not detect a release-blocking incident.",
        ],
    }


def should_fail(risk: str, fail_on: str) -> bool:
    return RISK_ORDER[risk.upper()] >= RISK_ORDER[fail_on.upper()]
