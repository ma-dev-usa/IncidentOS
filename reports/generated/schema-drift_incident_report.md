# FaultScene Incident Report

## Summary

- **Scenario:** `schema-drift`
- **Root service:** `inventory`
- **Root cause:** Inventory response schema changed and omitted reservation_id
- **Severity:** `HIGH`
- **Confidence:** `92%`
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

- Orders service detected missing reservation_id from inventory response.
- Gateway returned an upstream dependency failure.
- Failed statuses observed: [502, 502, 502, 502, 502]

## Recommended Remediation

- Restore reservation_id field or update the orders service contract.
- Add OpenAPI contract checks for the inventory reserve endpoint.
- Block release until dependent service schema is compatible.

## Release Gate Reasons

- Root cause: Inventory response schema changed and omitted reservation_id
- Root service: inventory
- Scenario: schema-drift
