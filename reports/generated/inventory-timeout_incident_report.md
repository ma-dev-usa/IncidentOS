# FaultScene Incident Report

## Summary

- **Scenario:** `inventory-timeout`
- **Root service:** `inventory`
- **Root cause:** Inventory dependency exceeded timeout budget
- **Severity:** `HIGH`
- **Confidence:** `88%`
- **Release risk:** `HIGH`
- **Block release:** `True`

## Replay Results

- **Total requests:** 5
- **Failed requests:** 5
- **Success rate:** 0.0

## Affected Services

- `gateway`
- `orders`
- `inventory`

## Evidence

- Maximum failed-request latency was 2088.79 ms.
- Checkout path returned a timeout or upstream timeout failure.
- Failed statuses observed: [504, 504, 504, 504, 504]

## Recommended Remediation

- Inspect inventory latency, database queries, and saturation metrics.
- Add timeout budget alerts for the checkout dependency chain.
- Consider circuit breaking or fallback behavior for inventory failures.

## Release Gate Reasons

- Root cause: Inventory dependency exceeded timeout budget
- Root service: inventory
- Scenario: inventory-timeout
