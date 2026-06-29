from pathlib import Path

from incidentos.models import IncidentClassification
from incidentos.report import generate_markdown_report


def test_generates_markdown_report(tmp_path):
    classification = IncidentClassification(
        scenario="inventory-down",
        root_service="inventory",
        root_cause="Inventory dependency unavailable",
        severity="HIGH",
        confidence=0.91,
        affected_services=["gateway", "orders", "inventory"],
        evidence=["inventory returned 503"],
        remediation=["restore inventory service"],
    )

    replay_payload = {
        "summary": {
            "total_requests": 5,
            "failed_requests": 5,
            "success_rate": 0.0,
        }
    }

    output_path = tmp_path / "incident_report.md"
    result = generate_markdown_report(classification, replay_payload, str(output_path))

    contents = Path(result).read_text(encoding="utf-8")

    assert "# IncidentOS Incident Report" in contents
    assert "inventory-down" in contents
    assert "Release risk" in contents
