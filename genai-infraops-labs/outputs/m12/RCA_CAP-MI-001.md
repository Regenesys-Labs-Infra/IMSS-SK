# Draft RCA / Post-Incident Review - CAP-MI-001

**Status:** Investigation incomplete; do not publish as a confirmed root cause.
**Incident window:** 2026-11-12 capstone simulation.

## 1. Summary

The Customer Portal produced critical HTTP 5xx, pod-readiness, image-pull, and login-success alerts after the 14:00 release.
Ticket reports also described sign-in errors and degraded report access.
The supplied manifest contains a Service selector mismatch and two additional configuration concerns; live state and recovery remain unverified.

## 2. Impact and SLA

- **Reported impact:** Multiple tickets report portal login failures, slow reports, and unavailable reports. The affected-user count and duration are unknown.
- **Alerts:** 18 critical Customer Portal alerts were grouped under CAP-MI-001. Two Finance Reporting alerts were kept separate.
- **SLA policy:** The policy target for P1 is a 15-minute response and 240-minute resolution. Actual acknowledgement, restoration, and closure times are unavailable, so no SLA breach conclusion is made.

## 3. Timeline (IST)

| Time | Event | Evidence / qualification |
|---|---|---|
| 14:00 | Release `2026.11.12` went live. | Capstone brief. |
| 14:03:00 | First `HTTP5xxRate` alert on `nginx-edge-01`. | CAPALR-000, critical. |
| 14:05:18 | First `PodNotReady` alert on `portal-web`. | CAPALR-006, critical. |
| 14:06:23 | First `KubePodImagePullBackOff` alert on `portal-api`. | CAPALR-011, critical. |
| 14:08:15 | First `LoginSuccessRateLow` alert on `portal-api`. | CAPALR-015, critical. |
| 14:08:41 | Last Customer Portal alert in the correlated burst. | CAPALR-017. |

**Subsequent remediation attempt (2026-11-25; not part of the incident event timeline):** REM-0001 was rejected; revised REM-0002 was approved, then stopped at pre-check because `kubectl` was unavailable. No patch command ran, and this attempt did not verify or restore the Nov 12 service.

## 4. Detection

The first supplied alert fired at 14:03 IST, approximately three minutes after the stated release time. The capstone brief says nine tickets arrived within 15 minutes. Acknowledgement and incident declaration timestamps were not supplied, so MTTA is not calculable.

## 5. Five Whys (blameless; hypotheses marked)

1. **Why did users report portal errors?** Tickets reported HTTP 503 sign-in failures and report degradation; alerts show edge 5xx and portal component health signals.
2. **Why might the web Service return 503?** The supplied manifest selects `app=portal-web-v2`, while the web pod template is labelled `app=portal-web`. Historical Nov 9 logs report zero endpoints for that selector. Whether this was the live Nov 12 state is unverified.
3. **Why did the selector mismatch reach the supplied manifest?** Unknown. No release validation or deployment history was provided.
4. **Why did `portal-api` report image-pull failures?** The capstone alerts show `KubePodImagePullBackOff`; the manifest's image reference is suspicious. Whether the tag is absent, inaccessible, or affected by registry configuration is unknown.
5. **Why was the ingress host potentially incorrect?** The supplied host string appears transposed, but the canonical hostname and DNS state are unavailable. This remains a hypothesis.

## 6. Contributing factors

- The selector mismatch is directly visible in the supplied manifest; historical logs from Nov 9 show the corresponding zero-endpoint/503 symptom, but do not establish current runtime state.
- The image-pull alerts and ingress host need separate live verification; they should not be treated as confirmed causes.
- No live cluster inspection was possible in the workspace because `kubectl` is unavailable.
- A read-only execution pre-check stopped the approved selector plan before mutation. The service state after that attempt is unknown.

## 7. Corrective and preventive actions

| Action | Type | Owner team | Due date / status |
|---|---|---|---|
| Verify live selector, pod labels, and endpoints; submit a fresh approved plan to align the selector if the mismatch remains. | CA | APP-PORTAL-L2 | TBD; prior plan REM-0002 failed pre-check |
| Inspect `portal-api` image-pull events, image availability, and registry access before proposing an image change. | CA | K8S-PLATFORM-L3 | TBD |
| Confirm the canonical portal hostname and DNS before proposing an Ingress change. | CA | LINUX-L2 / APP-PORTAL-L2 | TBD |
| Add CI validation that Service selectors match pod labels and that required endpoints are available in a deployment smoke test. | PA | APP-PORTAL-L2 / K8S-PLATFORM-L3 | TBD |
| Add release checks for image reference availability and approved Ingress hostnames. | PA | K8S-PLATFORM-L3 / LINUX-L2 | TBD |

## 8. What went well

- The alert burst was correlated into one Customer Portal parent while the Finance Reporting alerts remained separate.
- Ticket data was sanitized before triage, and instruction-like content was treated as untrusted data.
- The approval gate stopped before the patch when its pre-check could not run; no unverified infrastructure change was made.

**Closure requirement:** Revisit this RCA with live read-only evidence, confirmed recovery timestamps, and action owners/dates before marking the incident resolved.
