from incidentos.classifier import classify_replay


def test_classifies_normal_replay_as_low_risk():
    payload = {
        "summary": {"total_requests": 1, "failed_requests": 0, "success_rate": 1.0},
        "results": [
            {
                "ok": True,
                "actual_status": 200,
                "latency_ms": 100,
                "response_json": {"service": "gateway", "status": "created"},
            }
        ],
    }

    classification = classify_replay(payload)

    assert classification.severity == "LOW"
    assert classification.root_service == "none"


def test_classifies_schema_drift_as_high_risk():
    payload = {
        "summary": {"total_requests": 1, "failed_requests": 1, "success_rate": 0.0},
        "results": [
            {
                "ok": False,
                "actual_status": 502,
                "latency_ms": 350,
                "response_json": {
                    "detail": {
                        "service": "orders",
                        "failed_dependency": "inventory",
                        "error": "schema drift detected",
                        "missing_field": "reservation_id",
                    }
                },
            }
        ],
    }

    classification = classify_replay(payload)

    assert classification.scenario == "schema-drift"
    assert classification.root_service == "inventory"
    assert classification.severity == "HIGH"


def test_classifies_payment_failure_as_high_risk():
    payload = {
        "summary": {"total_requests": 1, "failed_requests": 1, "success_rate": 0.0},
        "results": [
            {
                "ok": False,
                "actual_status": 502,
                "latency_ms": 275,
                "response_json": {
                    "detail": {
                        "service": "orders",
                        "failed_dependency": "payments",
                        "dependency_status": 500,
                        "dependency_response": {
                            "detail": {
                                "service": "payments",
                                "error": "payment processor error",
                            }
                        },
                    }
                },
            }
        ],
    }

    classification = classify_replay(payload)

    assert classification.scenario == "payment-500"
    assert classification.root_service == "payments"
    assert classification.severity == "HIGH"
