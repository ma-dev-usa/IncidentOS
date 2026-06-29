# IncidentOS

![Tests](https://github.com/ma-dev-usa/IncidentOS/actions/workflows/tests.yml/badge.svg)

IncidentOS is a Dockerized microservice incident replay and root-cause analysis platform. It simulates production-style checkout failures across gateway, orders, inventory, and payments services, replays synthetic traffic, classifies likely root cause, and generates release-risk reports.

## Why This Exists

Production incidents often require engineers to inspect service logs, failed requests, dependency behavior, and recent changes before identifying root cause. IncidentOS recreates that workflow in a local, repeatable environment.

The project demonstrates backend engineering, microservice debugging, API reliability, test automation, and production-support thinking.

## Architecture

```text
traffic-replayer
       |
       v
gateway-service
       |
       v
orders-service
   |          |
   v          v
inventory   payments
```

## Features

- Dockerized microservice environment
- Synthetic checkout traffic replay
- Failure scenario injection
- Root-cause classification
- Release-risk scoring
- Markdown incident reports
- Pytest validation
- Makefile workflow automation
- GitHub Actions CI

## Failure Scenarios

| Scenario | Description |
|---|---|
| inventory_timeout | Inventory service latency breach causes checkout failures |
| payment_failure | Payment dependency returns failed responses |
| service_500 | Controlled internal service error |
| bad_config | Missing or invalid service configuration |
| schema_drift | API response shape changes unexpectedly |

## Quick Start

```bash
git clone https://github.com/ma-dev-usa/IncidentOS.git
cd IncidentOS
make up
```

Run a scenario:

```bash
make scenario SCENARIO=inventory_timeout
make replay
make report
make risk
```

Run tests:

```bash
make test
```

If `make test` is unavailable:

```bash
pytest
```

## Example Root-Cause Output

```text
Likely Root Cause: inventory-service latency breach
Confidence: 91%
Affected Path: gateway-service -> orders-service -> inventory-service
Severity: High

Evidence:
- inventory-service exceeded latency threshold
- orders-service returned dependency timeout
- gateway-service returned checkout failure after retry attempts

Recommended Actions:
1. Inspect inventory-service logs.
2. Verify recent inventory deployment changes.
3. Check database or downstream dependency latency.
4. Roll back if failures began after the latest release.
```

## Sample Reports

- [Sample Incident Report](reports/sample_incident_report.md)
- [Sample Release Risk Report](reports/sample_release_risk.md)

## Tech Stack

| Area | Tools |
|---|---|
| Backend services | Python, FastAPI |
| Local orchestration | Docker Compose |
| Testing | Pytest |
| Automation | Makefile, GitHub Actions |
| Reporting | Markdown |
| Reliability concepts | failure injection, traffic replay, root-cause analysis, release-risk scoring |

## Project Structure

```text
IncidentOS/
├── services/
│   ├── gateway-service/
│   ├── orders-service/
│   ├── inventory/
│   └── payments/
├── scenarios/
├── reports/
├── tests/
├── docs/
├── docker-compose.yml
├── Makefile
└── README.md
```

## Design Notes

IncidentOS treats incident response as a repeatable engineering workflow. The system creates controlled failures, replays realistic API traffic, observes downstream behavior, ranks likely causes, and produces reports that mirror first-pass production triage.

The goal is not to replace monitoring platforms. The goal is to show how service dependencies, failure scenarios, test automation, and release-risk checks can be modeled in a local developer environment.

## Resume Summary

```text
IncidentOS: Microservice Incident Replay & Root-Cause Analysis Platform
Python, Docker Compose, FastAPI, Pytest, Makefile, GitHub Actions

Built a Dockerized microservice incident replay platform that simulated checkout failures across gateway, orders, inventory, and payments services, replayed synthetic traffic, classified likely root cause, and generated release-risk reports.
```
