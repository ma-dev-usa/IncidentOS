import json
from pathlib import Path
from typing import Any

from incidentos.models import IncidentClassification


def _flatten_text(value: Any) -> str:
    if value is None:
        return ""

    if isinstance(value, dict):
        return " ".join(f"{k} {_flatten_text(v)}" for k, v in value.items())

    if isinstance(value, list):
        return " ".join(_flatten_text(item) for item in value)

    return str(value)


def classify_replay(replay_payload: dict[str, Any]) -> IncidentClassification:
    results = replay_payload.get("results", [])
    failed = [item for item in results if not item.get("ok", False)]
    summary = replay_payload.get("summary", {})

    if not failed:
        return IncidentClassification(
            scenario="normal",
            root_service="none",
            root_cause="No incident detected",
            severity="LOW",
            confidence=0.95,
            affected_services=[],
            evidence=[
                f"{summary.get('total_requests', 0)} requests replayed successfully",
                f"Success rate was {summary.get('success_rate', 0)}",
            ],
            remediation=[
                "No remediation required.",
                "Continue monitoring checkout path health.",
            ],
        )

    text_parts: list[str] = []

    for item in failed:
        text_parts.extend(
            [
                _flatten_text(item.get("response_json")),
                _flatten_text(item.get("error")),
                str(item.get("actual_status")),
                str(item.get("latency_ms")),
            ]
        )

    text = " ".join(text_parts).lower()

    failed_statuses = [item.get("actual_status") for item in failed]
    max_latency = max(float(item.get("latency_ms", 0)) for item in failed)

    if "schema drift" in text or "missing_field" in text or "reservation_id" in text:
        return IncidentClassification(
            scenario="schema-drift",
            root_service="inventory",
            root_cause="Inventory response schema changed and omitted reservation_id",
            severity="HIGH",
            confidence=0.92,
            affected_services=["gateway", "orders", "inventory"],
            evidence=[
                "Orders service detected missing reservation_id from inventory response.",
                "Gateway returned an upstream dependency failure.",
                f"Failed statuses observed: {failed_statuses}",
            ],
            remediation=[
                "Restore reservation_id field or update the orders service contract.",
                "Add OpenAPI contract checks for the inventory reserve endpoint.",
                "Block release until dependent service schema is compatible.",
            ],
        )

    if "payment" in text and ("processor error" in text or "500" in text):
        return IncidentClassification(
            scenario="payment-500",
            root_service="payments",
            root_cause="Payments dependency returned HTTP 500 during checkout",
            severity="HIGH",
            confidence=0.9,
            affected_services=["gateway", "orders", "payments"],
            evidence=[
                "Orders service reported failed_dependency=payments.",
                "Payments service returned a server-side failure.",
                f"Failed statuses observed: {failed_statuses}",
            ],
            remediation=[
                "Inspect payments service logs for processor errors.",
                "Verify payment provider credentials and recent deploys.",
                "Block release until payment dependency is stable.",
            ],
        )

    if "inventory" in text and ("unavailable" in text or "503" in text):
        return IncidentClassification(
            scenario="inventory-down",
            root_service="inventory",
            root_cause="Inventory dependency unavailable during checkout",
            severity="HIGH",
            confidence=0.91,
            affected_services=["gateway", "orders", "inventory"],
            evidence=[
                "Orders service reported failed_dependency=inventory.",
                "Inventory service returned unavailable status.",
                f"Failed statuses observed: {failed_statuses}",
            ],
            remediation=[
                "Verify inventory service health and recent deployments.",
                "Check network connectivity between orders and inventory.",
                "Block release until inventory dependency recovers.",
            ],
        )

    if "timed out" in text or "timeout" in text or 504 in failed_statuses or max_latency > 2000:
        return IncidentClassification(
            scenario="inventory-timeout",
            root_service="inventory",
            root_cause="Inventory dependency exceeded timeout budget",
            severity="HIGH",
            confidence=0.88,
            affected_services=["gateway", "orders", "inventory"],
            evidence=[
                f"Maximum failed-request latency was {max_latency} ms.",
                "Checkout path returned a timeout or upstream timeout failure.",
                f"Failed statuses observed: {failed_statuses}",
            ],
            remediation=[
                "Inspect inventory latency, database queries, and saturation metrics.",
                "Add timeout budget alerts for the checkout dependency chain.",
                "Consider circuit breaking or fallback behavior for inventory failures.",
            ],
        )

    if "missing required configuration" in text or "missing_config" in text:
        return IncidentClassification(
            scenario="bad-config",
            root_service="orders",
            root_cause="Orders service missing required runtime configuration",
            severity="HIGH",
            confidence=0.87,
            affected_services=["gateway", "orders"],
            evidence=[
                "Orders service emitted missing configuration error.",
                "Checkout failed before dependency calls completed.",
                f"Failed statuses observed: {failed_statuses}",
            ],
            remediation=[
                "Validate required environment variables during service startup.",
                "Add configuration smoke tests to CI/CD.",
                "Block release until configuration checks pass.",
            ],
        )

    return IncidentClassification(
        scenario="unknown",
        root_service="unknown",
        root_cause="Unclassified checkout failure",
        severity="MEDIUM",
        confidence=0.55,
        affected_services=["gateway", "orders"],
        evidence=[
            "Replay detected failed checkout requests.",
            f"Failed statuses observed: {failed_statuses}",
            f"Failed request count: {len(failed)}",
        ],
        remediation=[
            "Inspect generated replay payload.",
            "Review gateway and orders service logs.",
            "Add a new classifier rule for this failure signature.",
        ],
    )


def save_classification(
    classification: IncidentClassification,
    output_path: str = "reports/generated/latest_classification.json",
) -> str:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(classification.to_dict(), indent=2), encoding="utf-8")
    return str(output)


def load_classification(path: str = "reports/generated/latest_classification.json") -> IncidentClassification:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return IncidentClassification(**data)
