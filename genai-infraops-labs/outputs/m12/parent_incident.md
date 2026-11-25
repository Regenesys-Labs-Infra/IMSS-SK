# Proposed parent incident: CAP-MI-001

| Field | Value |
|---|---|
| Business service | Customer Portal |
| Priority / severity | P1 / Critical |
| Status | Proposed; awaiting NOC lead approval |
| Alert window | 2026-11-12 14:03:00-14:08:41 IST |
| Correlated alerts | 18 |
| Primary owner | APP-PORTAL-L2 |
| Supporting groups | K8S-PLATFORM-L3, LINUX-L2 |

## Summary

Eighteen critical alerts indicate a Customer Portal incident following the 14:00 release: HTTP 5xx at `nginx-edge-01`, readiness failures on `portal-web`, image-pull failures and low login success on `portal-api`. The alerts arrive in a continuous burst; the largest gap between same-service alerts is 39 seconds, so they are grouped under a five-minute rolling inactivity window.

## Root-cause candidate

An issue in the `portal-api` rollout or image pull may have caused pod readiness and login failures, with HTTP 5xx at the edge as a downstream symptom. This is an unverified hypothesis, not a confirmed root cause.

## Child alert breakdown

| Alert | CI | Count | Child IDs |
|---|---|---:|---|
| HTTP5xxRate | `nginx-edge-01` | 6 | CAPALR-000 through CAPALR-005 |
| PodNotReady | `portal-web` | 5 | CAPALR-006 through CAPALR-010 |
| KubePodImagePullBackOff | `portal-api` | 4 | CAPALR-011 through CAPALR-014 |
| LoginSuccessRateLow | `portal-api` | 3 | CAPALR-015 through CAPALR-017 |

## Excluded from this parent

CAPALR-018 and CAPALR-019 are `HighCPU` alerts on `srv-fin-app-02`, which the CMDB maps to Finance Reporting. They are intentionally not correlated with Customer Portal; route them separately for review.

## Human review and next checks

NOC lead approval is required before creating or updating an external incident. Confirm the affected release and CI relationships, investigate the `portal-api` image-pull/readiness events, and verify recovery using pod readiness, login success rate, and edge 5xx metrics. No remediation or production action has been executed.
