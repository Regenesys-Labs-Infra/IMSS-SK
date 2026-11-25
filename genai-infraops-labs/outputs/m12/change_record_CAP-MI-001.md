# Draft change record - CAP-MI-001

**Change ID:** TBD (assign in ITSM; do not reuse CHG0003051)
**Type:** Normal
**Status:** Draft - not scheduled, CAB-approved, or implemented
**Requested by:** APP-PORTAL-L2
**Short description:** Align the `portal-web` Service selector with its pod labels and add release validation.
**Affected CI:** `portal-web` in namespace `portal`; confirm the live CI and cluster before scheduling.
**Planned window:** TBD; select and approve a low-traffic window.
**Related evidence:** [CAP-MI-001 evidence pack](./CAP-MI-001_evidence.md)
**Approval history:** REM-0001 rejected; REM-0002 approved by Rajesh but pre-check failed because `kubectl` was unavailable. No infrastructure change was applied. A fresh proposal and approval are required.

## Description and scope

The supplied manifest has Service selector `app=portal-web-v2` while the `portal-web` pod template is labelled `app=portal-web`. The proposed change is limited to the Service selector. The `portal-api` image and Ingress hostname are separate unverified findings and are out of scope for this change.

## Implementation plan

1. Assign the ITSM change ID and confirm the exact isolated target context and production CI through the approved change process.
2. Using read-only checks, capture the current Service selector, deployment pod labels, ready pod state, and Service endpoints.
3. Stop if the live values differ from the evidence or if the target context cannot be verified; revise the plan and re-approve.
4. Through a fresh approved `tools/approve.py` plan, set the `portal-web` Service selector to `app=portal-web`. Do not modify the Deployment, image, Ingress, or other resources under this change.
5. Verify the selector, endpoint addresses, readiness, and customer-facing sign-in/report checks. Monitor HTTP 5xx and login success before declaring completion.

## Test plan

- Confirm pre-change selector and pod-template labels from the approved context.
- Confirm ready `portal-web` pods expose the expected label.
- After the approved patch, verify the Service selector is `app=portal-web` and endpoint addresses correspond to ready pods.
- Run the approved customer-facing smoke checks and confirm HTTP 5xx/login metrics recover.
- Record command output and reviewer sign-off in the change record. No live test has been performed yet.

## Backout plan

Restore the selector captured in the pre-change snapshot using a separately approved rollback if verification fails. The supplied manifest's `app=portal-web-v2` value is associated with a historical zero-endpoint symptom; restoring it may reintroduce the outage. Keep the incident open, notify the bridge, and obtain a new approval before rollback. Backout is documented but untested.

## Provisional change risk

| Factor | Score | Reason |
|---|---:|---|
| Impact if it fails | 3 | A selector error can leave a customer-facing portal without web endpoints. |
| Complexity | 2 | Several manual steps are required for pre-checks, the approved mutation, and verification. |
| Change history | 3* | No history was provided; use the highest score as a planning placeholder, not a claim that this is a first-time change. |
| Backout | 2 | Prior selector can be restored, but the rollback is untested and may restore the known mismatch. |
| Timing | 3* | No window is selected; use the highest score as a planning placeholder, not a claim that the window is peak/month-end. |
| **Total** | **13 / 15 - High** | CAB review required under the supplied rubric. |

*Change-history and timing scores are conservative placeholders because required facts are unavailable. Re-score both when the change history and window are confirmed.

## CAB one-page summary

- **What:** Align the `portal-web` Service selector with the actual pod-template label.
- **Why:** The supplied manifest and historical logs indicate a selector mismatch and zero endpoints; Nov 12 live state is unverified.
- **Risk:** High, provisional; customer-facing service, untested rollback, and unscheduled window.
- **Backout:** Restore the captured prior selector only after a new approval; keep the incident open if endpoints do not recover.
- **Communications:** Notify the bridge and Service Desk before the window; issue customer updates only after Incident Manager approval.

### Go / no-go checklist

- [ ] ITSM change ID assigned; this draft is linked to CAP-MI-001.
- [ ] Service owner, CAB, and required platform approvers have approved the plan.
- [ ] Exact target context is verified as the intended isolated environment.
- [ ] Change window, customer impact, and rollback owner are confirmed.
- [ ] Current selector, labels, endpoint list, and ready pod state are captured.
- [ ] Image and Ingress issues are tracked separately and not silently included.
- [ ] Approved execution plan and backout plan pass policy checks.
- [ ] Customer/service-desk communications are reviewed and scheduled.
- [ ] Post-change selector/endpoints and customer-facing checks have named reviewers.
- [ ] Stop/rollback criteria and monitoring period are agreed.

## Maintenance notice (draft; under 80 words)

We are planning maintenance to improve Customer Portal availability. The date, time, and expected impact are not yet confirmed. We will share a notice after the change window and approvals are finalized. No action is required from users at this time.

## Service Desk briefing

- **Expected contacts:** Portal sign-in errors, HTTP 503 reports, slow or unavailable reports.
- **Scripted answer:** “We are investigating the portal issue. A fix has not been verified yet; we will share the next confirmed update through the incident channel.”
- **Escalation:** P1/P2 or broad impact to APP-PORTAL-L2 and the Incident Manager; pod/image-pull findings to K8S-PLATFORM-L3; edge/Ingress findings to LINUX-L2.
- **Handling:** Do not promise resolution or share internal hostnames. If a customer included a credential, follow the approved credential-exposure process without repeating the value.
