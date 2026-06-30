import json
import time
from pathlib import Path
from typing import Any

import httpx

from faultscene.models import ReplayResult


def read_jsonl(path: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    return records


def run_replay(
    url: str,
    traffic_path: str,
    output_path: str = "reports/generated/latest_replay.json",
) -> dict[str, Any]:
    traffic = read_jsonl(traffic_path)
    results: list[dict[str, Any]] = []

    with httpx.Client(timeout=10.0) as client:
        for index, request in enumerate(traffic, start=1):
            method = request.get("method", "POST").upper()
            expected_status = int(request.get("expected_status", 200))
            body = request.get("json")

            start = time.perf_counter()

            try:
                response = client.request(method, url, json=body)
                latency_ms = round((time.perf_counter() - start) * 1000, 2)

                try:
                    response_json = response.json()
                except ValueError:
                    response_json = {"raw_body": response.text}

                result = ReplayResult(
                    request_id=index,
                    method=method,
                    url=url,
                    expected_status=expected_status,
                    actual_status=response.status_code,
                    ok=response.status_code == expected_status,
                    latency_ms=latency_ms,
                    response_json=response_json,
                )

            except Exception as exc:
                latency_ms = round((time.perf_counter() - start) * 1000, 2)

                result = ReplayResult(
                    request_id=index,
                    method=method,
                    url=url,
                    expected_status=expected_status,
                    actual_status=None,
                    ok=False,
                    latency_ms=latency_ms,
                    response_json=None,
                    error=str(exc),
                )

            results.append(result.to_dict())

    failed = [item for item in results if not item["ok"]]

    payload = {
        "summary": {
            "total_requests": len(results),
            "failed_requests": len(failed),
            "success_rate": round((len(results) - len(failed)) / max(len(results), 1), 2),
        },
        "results": results,
    }

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    return payload


def load_replay(path: str = "reports/generated/latest_replay.json") -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))
