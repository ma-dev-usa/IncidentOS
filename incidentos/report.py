from pathlib import Path
from typing import Any

from incidentos.models import IncidentClassification
from incidentos.risk import score_release_risk


def generate_markdown_report(
    classification: IncidentClassification,
    replay_payload: dict[str, Any],
    output_path: str = "reports/generated/incident_report.md",
) -> str:
    risk = score_release_risk(classification)
    summary = replay_payload.get("summary", {})

    lines = [
        "# IncidentOS Incident Report",
        "",
        "## Summary",
        "",
        f"- **Scenario:** `{classification.scenario}`",
        f"- **Root service:** `{classification.root_service}`",
        f"- **Root cause:** {classification.root_cause}",
        f"- **Severity:** `{classification.severity}`",
        f"- **Confidence:** `{classification.confidence:.0%}`",
        f"- **Release risk:** `{risk['risk']}`",
        f"- **Block release:** `{risk['should_block_release']}`",
        "",
        "## Replay Results",
        "",
        f"- **Total requests:** {summary.get('total_requests', 0)}",
        f"- **Failed requests:** {summary.get('failed_requests', 0)}",
        f"- **Success rate:** {summary.get('success_rate', 0)}",
        "",
        "## Affected Services",
        "",
    ]

    for service in classification.affected_services:
        lines.append(f"- `{service}`")

    if not classification.affected_services:
        lines.append("- None")

    lines.extend(
        [
            "",
            "## Evidence",
            "",
        ]
    )

    for item in classification.evidence:
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## Recommended Remediation",
            "",
        ]
    )

    for item in classification.remediation:
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## Release Gate Reasons",
            "",
        ]
    )

    for item in risk["reasons"]:
        lines.append(f"- {item}")

    lines.append("")

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")

    return str(output)
