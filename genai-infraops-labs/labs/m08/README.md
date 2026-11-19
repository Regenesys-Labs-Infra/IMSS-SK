# Module 8: AI-Driven Incident Management & RCA

| Day | Session | Theory | Hands-on | Format |
|---|---|---|---|---|
| Day 2 | Session 4 | 0.25 h | 0.75 h | RCA Lab |

Participants use Copilot as a Major Incident co-pilot: timeline, stakeholder updates, SLA impact and a blameless RCA.

## What you will learn

- Reconstruct an incident timeline from alerts, work notes and bridge chat.
- Draft stakeholder, executive and status-page updates without speculation.
- Compute SLA impact with a script rather than the model.
- Produce a blameless RCA / post-incident review with corrective and preventive actions.

## Key terms explained

| Term | Plain-English meaning |
|---|---|
| Incident / Major Incident | An incident is an unplanned interruption or degradation of a service. A Major Incident has high business impact and is run by a Major Incident Manager on a bridge call. |
| P1 / P2 / P3 / P4 | Priority levels from Impact x Urgency. P1 is the most critical. |
| Bridge | The live call/chat where teams work a major incident together. |
| Stakeholder update / status page | Regular internal update to managers and the customer-safe public message about service status. |
| SLA / breach | Service Level Agreement: agreed response and resolution times. A breach means a target was missed. |
| RCA / PIR | Root Cause Analysis / Post-Incident Review: the structured review after an incident to find causes and prevent recurrence. |
| 5 Whys | Asking 'why?' repeatedly (about five times) to move from symptom to root cause. |
| Blameless | Reviews focus on systems and processes, never on blaming individuals. |
| CAPA | Corrective And Preventive Actions: fixes for this incident and changes to stop it happening again. |

## Real-time Service Desk use case UC-08: Major Incident co-pilot

| | |
|---|---|
| Persona | Major Incident Manager |
| Problem statement | During a P1 the Incident Manager must coordinate the bridge, send updates every 30 minutes, compute SLA impact and deliver an RCA within 5 days. Updates go out late and inconsistent. |
| What AI does | Drafts the timeline, bridge updates, status-page text and RCA; the SLA figure comes from a script. |
| Human review checkpoint | Incident Manager approves every update; Problem Manager and service owner approve the RCA. |
| Output asset | Major-incident communication and RCA pack |
| KPI impact | Update cadence adherence, PIR lead time |

## Hands-on labs

### Lab 8.1: Major Incident co-pilot for INC-MAJ-0042 (45 min)

**Objective:** Run the communication and RCA workflow for a 2-hour portal outage after a release.

**Files:** `data/incidents/INC-MAJ-0042/`, `data/policy/sla_policy.json`, `tools/sla_calc.py`

**Steps**

1. Timeline:

   Copilot Chat prompt:

   ```text
   Build a minute-level timeline from #file:data/incidents/INC-MAJ-0042/bridge_chat.txt and #file:data/incidents/INC-MAJ-0042/worknotes.json.
   Columns: Time (IST) | Source | Event | Fact or Assumption.
   ```

2. Run /mi-bridge-update three times with as-at times 18:51, 19:21 and 19:51.
3. Calculate SLA with code, not with the AI:

   Terminal:

   ```bash
   python3 tools/sla_calc.py --incident data/incidents/INC-MAJ-0042/worknotes.json --policy data/policy/sla_policy.json --out outputs/m08/sla_result.txt
   ```

4. Run /rca-pir and review: is it blameless? Are actions owned and dated (TBD allowed)?

**Expected result:** Timeline, 3 bridge updates, status-page text, SLA result and RCA draft in outputs/m08/.

**Check before you finish**

- [ ] Times match the sources
- [ ] No speculation stated as fact
- [ ] No individual blamed

**Deliverable:** RCA template pack and bridge updates.


## Save your work

```bash
git add -A
git commit -m "Module 8 labs"
git push
```
