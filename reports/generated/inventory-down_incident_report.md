# IncidentOS Incident Report

## Summary

- **Scenario:** `inventory-down`
- **Root service:** `inventory`
- **Root cause:** Inventory dependency unavailable during checkout
- **Severity:** `HIGH`
- **Confidence:** `91%`
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

- Orders service reported failed_dependency=inventory.
- Inventory service returned unavailable status.
- Failed statuses observed: [502, 502, 502, 502, 502]

## Recommended Remediation

- Verify inventory service health and recent deployments.
- Check network connectivity between orders and inventory.
- Block release until inventory dependency recovers.

## Release Gate Reasons

- Root cause: Inventory dependency unavailable during checkout
- Root service: inventory
- Scenario: inventory-down
