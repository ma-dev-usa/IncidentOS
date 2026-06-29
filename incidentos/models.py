from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class ReplayResult:
    request_id: int
    method: str
    url: str
    expected_status: int
    actual_status: int | None
    ok: bool
    latency_ms: float
    response_json: Any | None
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class IncidentClassification:
    scenario: str
    root_service: str
    root_cause: str
    severity: str
    confidence: float
    affected_services: list[str]
    evidence: list[str]
    remediation: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
