# IncidentOS

IncidentOS is a Dockerized microservice incident replay and root-cause analysis platform.

## Goal

Simulate production-style checkout failures across multiple services, replay synthetic traffic, classify likely root cause, and generate release-risk reports.

## Architecture

```text
traffic-replayer
      |
      v
gateway-service
      |
      v
orders-service
   /        \
  v          v
inventory   payments
