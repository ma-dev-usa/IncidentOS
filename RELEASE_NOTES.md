# FaultScene v1.0.0

FaultScene is a Dockerized microservice incident replay and root-cause analysis platform for simulating production-style checkout failures, replaying synthetic traffic, classifying likely root cause, and generating release-risk reports.

## Highlights

- Built a Docker Compose microservice environment with gateway, orders, inventory, payments, and traffic replay services
- Simulated a schema drift incident where inventory omits an expected response field
- Added synthetic traffic replay for reproducing failure scenarios
- Implemented root-cause classification for dependency and API contract failures
- Generated release-risk reports for validating production readiness
- Added Pytest validation and GitHub Actions CI coverage
- Documented architecture, screenshots, and local setup flow

## Stack

Python, FastAPI, Docker, Docker Compose, Pytest, GitHub Actions, Makefile automation, Markdown reporting
