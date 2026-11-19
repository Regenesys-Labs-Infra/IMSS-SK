---
mode: ask
description: UC-12 Complete a change record, score risk and build the CAB pack
---
Change: #file:data/changes/${input:changeFile}  Rubric: #file:data/changes/change_risk_rubric.md
Use @workspace to find the related RCA, runbooks and IaC.
1. List missing or weak fields in the change record and propose text for each (implementation, test, backout).
2. Score each rubric factor 1-3 with one-line reasons; total and category (Low/Medium/High) and who approves.
3. CAB one-pager: what, why, risk, backout, window, comms, go/no-go checklist (8-10 checks).
4. User maintenance notice (<= 80 words) and Service Desk briefing (expected calls, scripted answer, escalation path).
