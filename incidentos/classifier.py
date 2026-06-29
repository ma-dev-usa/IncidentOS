from typing import Any

from incidentos.models import IncidentClassification


def _flatten_text(value: Any) -> str:
    if value is None:
        return ""

    if isinstance(value, dict):
        return " ".join(_flatten_text(item) for item in value.values())

    if isinstance(value, list):
        return " ".join(_flatten_text(item) for item in value)

    return str(value)


def _collect_failed_results(replay_payload: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        result
        for result in replay_payload.get("results", [])
        if not result.get("ok", False)
    ]


def classify_replay(replay_payload: dict[str, Any]) -> IncidentClassification:
    failed = _collect_failed_results(replay_payload)

    if not failed:
        return IncidentClassification(
            scenario="no-incident",
            root_service="none",
            root_cause="No incident detected",
            severity="LOW",
            confidence=0.99,
            affected_services=[],
            evidence=["All replayed requests matched expected status codes."],
            remediation=["No release block recommended."],
        )

    combined_text = " ".join(
        _flatten_text(result.get("response_json")) + " " + _flatten_text(result.get("error"))
        for result in failed
    ).lower()

    statuses = {
        result.get("actual_status")
        for result in failed
        if result.get("actual_status") is not None
    }

    failed_count = len(failed)
    total_count = replay_payload.get("summary", {}).get("total_requests", failed_count)

    base_evidence = [
        f"{failed_count}/{total_count} replayed requests failed.",
        f"Observed HTTP statuses: {sorted(statuses)}.",
    ]

    if "schema drift" in combined_text or "missing_field" in combined_text or "reservation_id" in combined_text:
        return IncidentClassification(
            scenario="schema-drift",
            root_service="inventory",
            root_cause="Inventory response schema changed unexpectedly",
            severity="HIGH",
            confidence=0.94,
            affected_services=["gateway", "orders", "inventory"],
            evidence=base_evidence + [
                "Orders service detected missing inventory reservation_id.",
                "Checkout failed because downstream response shape no longer matched the expected contract.",
            ],
            remediation=[
                "Block release until inventory response contract is restored or orders service is updated.",
                "Add contract tests for required inventory response fields.",
            ],
        )

    if "retry storm" in combined_text or 429 in statuses:
        return IncidentClassification(
            scenario="retry-storm",
            root_service="orders",
            root_cause="Orders service generated repeated dependency calls",
            severity="HIGH",
            confidence=0.9,
            affected_services=["gateway", "orders", "inventory"],
            evidence=base_evidence + [
                "Orders service reported retry storm behavior.",
                "Repeated inventory calls increase dependency pressure and checkout latency.",
            ],
            remediation=[
                "Apply retry budgets and exponential backoff.",
                "Add circuit breaking around inventory dependency calls.",
            ],
        )

    if "bad configuration" in combined_text or "missing_config" in combined_text:
        return IncidentClassification(
            scenario="bad-config",
            root_service="orders",
            root_cause="Orders service is missing required runtime configuration",
            severity="HIGH",
            confidence=0.91,
            affected_services=["gateway", "orders"],
            evidence=base_evidence + [
                "Orders service reported missing required configuration.",
                "Checkout cannot complete because service discovery/configuration is invalid.",
            ],
            remediation=[
                "Verify required environment variables before startup.",
                "Add configuration validation to fail fast during deployment.",
            ],
        )

    if "payment" in combined_text and ("500" in combined_text or "processor error" in combined_text):
        return IncidentClassification(
            scenario="payment-500",
            root_service="payments",
            root_cause="Payment dependency returned internal server error",
            severity="HIGH",
            confidence=0.93,
            affected_services=["gateway", "orders", "payments"],
            evidence=base_evidence + [
                "Orders service identified payments as the failed dependency.",
                "Payment dependency returned an internal server error.",
            ],
            remediation=[
                "Inspect payment service logs and error rate.",
                "Add fallback handling or release block for payment dependency failures.",
            ],
        )

    if "inventory" in combined_text and ("unavailable" in combined_text or "503" in combined_text):
        return IncidentClassification(
            scenario="inventory-down",
            root_service="inventory",
            root_cause="Inventory dependency is unavailable",
            severity="HIGH",
            confidence=0.93,
            affected_services=["gateway", "orders", "inventory"],
            evidence=base_evidence + [
                "Orders service identified inventory as the failed dependency.",
                "Inventory dependency returned unavailable.",
            ],
            remediation=[
                "Check inventory service health and deployment status.",
                "Block release if inventory dependency is required for checkout.",
            ],
        )

    if "timeout" in combined_text or 504 in statuses:
        return IncidentClassification(
            scenario="inventory-timeout",
            root_service="inventory",
            root_cause="Inventory dependency exceeded timeout threshold",
            severity="HIGH",
            confidence=0.88,
            affected_services=["gateway", "orders", "inventory"],
            evidence=base_evidence + [
                "Checkout returned a gateway timeout.",
                "Orders service failed while waiting on a downstream dependency.",
            ],
            remediation=[
                "Inspect inventory latency and timeout settings.",
                "Add timeout budgets, monitoring, and circuit breaking.",
            ],
        )

    return IncidentClassification(
        scenario="unknown-dependency-failure",
        root_service="unknown",
        root_cause="Unhandled dependency failure detected during replay",
        severity="MEDIUM",
        confidence=0.65,
        affected_services=["gateway", "orders"],
        evidence=base_evidence + [
            "Replay detected failed checkout responses but did not match a known incident signature.",
        ],
        remediation=[
            "Inspect raw replay output and service logs.",
            "Add a new classifier rule for this failure pattern.",
        ],
    )
