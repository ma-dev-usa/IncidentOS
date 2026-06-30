# FaultScene Incident Report

## Summary

- **Scenario:** `schema-drift`
- **Root service:** `inventory`
- **Root cause:** Inventory response schema changed unexpectedly
- **Severity:** `HIGH`
- **Confidence:** `94%`
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

- 5/5 replayed requests failed.
- Observed HTTP statuses: [502].
- Orders service detected missing inventory reservation_id.
- Checkout failed because downstream response shape no longer matched the expected contract.

## Recommended Remediation

- Block release until inventory response contract is restored or orders service is updated.
- Add contract tests for required inventory response fields.

## Release Gate Reasons

- Root cause: Inventory response schema changed unexpectedly
- Root service: inventory
- Scenario: schema-drift
