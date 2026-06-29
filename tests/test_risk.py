from incidentos.models import IncidentClassification
from incidentos.risk import score_release_risk, should_fail


def test_high_severity_blocks_release():
    classification = IncidentClassification(
        scenario="schema-drift",
        root_service="inventory",
        root_cause="Inventory schema changed",
        severity="HIGH",
        confidence=0.94,
        affected_services=["gateway", "orders", "inventory"],
        evidence=["missing reservation_id"],
        remediation=["block release"],
    )

    risk = score_release_risk(classification)

    assert risk["risk"] == "HIGH"
    assert risk["should_block_release"] is True


def test_should_fail_release_gate():
    assert should_fail("HIGH", "HIGH") is True
    assert should_fail("HIGH", "MEDIUM") is True
    assert should_fail("LOW", "HIGH") is False
