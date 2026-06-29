from incidentos.classifier import classify_replay


def test_classifier_detects_schema_drift():
    replay = {
        "summary": {"total_requests": 1, "failed_requests": 1, "success_rate": 0.0},
        "results": [
            {
                "ok": False,
                "actual_status": 502,
                "response_json": {
                    "detail": {
                        "service": "gateway",
                        "upstream_response": {
                            "detail": {
                                "service": "orders",
                                "failed_dependency": "inventory",
                                "error": "schema drift detected",
                                "missing_field": "reservation_id",
                            }
                        },
                    }
                },
            }
        ],
    }

    result = classify_replay(replay)

    assert result.scenario == "schema-drift"
    assert result.root_service == "inventory"
    assert result.severity == "HIGH"


def test_classifier_detects_payment_failure():
    replay = {
        "summary": {"total_requests": 1, "failed_requests": 1, "success_rate": 0.0},
        "results": [
            {
                "ok": False,
                "actual_status": 502,
                "response_json": {
                    "detail": {
                        "upstream_response": {
                            "detail": {
                                "failed_dependency": "payments",
                                "dependency_status": 500,
                                "dependency_response": {"detail": "payment processor error"},
                            }
                        }
                    }
                },
            }
        ],
    }

    result = classify_replay(replay)

    assert result.scenario == "payment-500"
    assert result.root_service == "payments"
    assert result.severity == "HIGH"


def test_classifier_detects_clean_replay():
    replay = {
        "summary": {"total_requests": 1, "failed_requests": 0, "success_rate": 1.0},
        "results": [{"ok": True, "actual_status": 200, "response_json": {"status": "created"}}],
    }

    result = classify_replay(replay)

    assert result.scenario == "no-incident"
    assert result.severity == "LOW"
