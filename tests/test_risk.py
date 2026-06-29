from incidentos.models import IncidentClassification
from incidentos.risk import score_release_risk, should_fail


def test_high_severity_blocks_release():
    classification = IncidentClassification(
        scenario="payment-500",
        root_service="payments",
        root_cause="Payments dependency returned HTTP 500",
        severity="HIGH",
        confidence=0.9,
        affected_services=["gateway", "orders", "payments"],
        evidence=["payment failed"],
        remediation=["rollback payment service"],
    )

    risk = score_release_risk(classification)

    assert risk["risk"] == "HIGH"
    assert risk["should_block_release"] is True
    assert should_fail("HIGH", "HIGH") is True


def test_low_severity_does_not_block_release():
    classification = IncidentClassification(
        scenario="normal",
        root_service="none",
        root_cause="No incident detected",
        severity="LOW",
        confidence=0.95,
        affected_services=[],
        evidence=["all requests passed"],
        remediation=["none"],
    )

    risk = score_release_risk(classification)

    assert risk["risk"] == "LOW"
    assert risk["should_block_release"] is False
    assert should_fail("LOW", "HIGH") is False
