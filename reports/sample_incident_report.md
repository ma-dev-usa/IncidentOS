# Sample Incident Report

## Summary

Checkout requests failed because the inventory service exceeded the configured latency threshold and caused downstream timeout behavior.

## Severity

High

## Likely Root Cause

inventory-service latency breach

## Confidence

91%

## Affected Path

```text
gateway-service -> orders-service -> inventory-service
