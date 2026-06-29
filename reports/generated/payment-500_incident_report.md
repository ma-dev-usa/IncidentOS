# IncidentOS Incident Report

## Summary

- **Scenario:** `payment-500`
- **Root service:** `payments`
- **Root cause:** Payments dependency returned HTTP 500 during checkout
- **Severity:** `HIGH`
- **Confidence:** `90%`
- **Release risk:** `HIGH`
- **Block release:** `True`

## Replay Results

- **Total requests:** 5
- **Failed requests:** 5
- **Success rate:** 0.0

## Affected Services

- `gateway`
- `orders`
- `payments`

## Evidence

- Orders service reported failed_dependency=payments.
- Payments service returned a server-side failure.
- Failed statuses observed: [502, 502, 502, 502, 502]

## Recommended Remediation

- Inspect payments service logs for processor errors.
- Verify payment provider credentials and recent deploys.
- Block release until payment dependency is stable.

## Release Gate Reasons

- Root cause: Payments dependency returned HTTP 500 during checkout
- Root service: payments
- Scenario: payment-500
