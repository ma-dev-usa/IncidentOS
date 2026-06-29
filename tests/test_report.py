from pathlib import Path

from incidentos.models import IncidentClassification
from incidentos.report import generate_markdown_report


def test_report_generator_writes_markdown(tmp_path):
    classification = IncidentClassification(
        scenario="inventory-down",
        root_service="inventory",
        root_cause="Inventory unavailable",
        severity="HIGH",
        confidence=0.93,
        affected_services=["gateway", "orders", "inventory"],
        evidence=["inventory returned 503"],
        remediation=["check inventory service"],
    )

    replay = {
        "summary": {
            "total_requests": 5,
            "failed_requests": 5,
            "success_rate": 0.0,
        }
    }

    output = tmp_path / "report.md"
    path = generate_markdown_report(classification, replay, str(output))

    content = Path(path).read_text(encoding="utf-8")

    assert "# IncidentOS Incident Report" in content
    assert "inventory-down" in content
    assert "Block release" in content
