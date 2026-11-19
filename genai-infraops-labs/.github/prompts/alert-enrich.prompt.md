---
mode: ask
description: UC-05 Turn a group of correlated alerts into one enriched parent incident
---
Input: alert group ${input:groupId} from #file:outputs/m06/alert_groups.json
Reference: #file:data/cmdb/ci_inventory.csv and #file:data/policy/assignment_groups.json
Produce a parent incident with: Short description (<= 80 chars) · Business service · Impact (who/what is affected)
· Probable cause (hypothesis, label it) · First 3 read-only checks · Owner group (ID from assignment_groups.json only)
· Linked child alerts (IDs) · Suggested priority with impact/urgency reasoning.
Do not invent runbook URLs; write "runbook: TBD" if none is known.
