# Module 10: AI Agents for Operational Workflows

| Day | Session | Theory | Hands-on | Format |
|---|---|---|---|---|
| Day 3 | Session 5 | 0.25 h | 1.75 h | Agent Workflow Lab |

Participants build end-to-end workflows: ticket auto-triage with a human review queue, change enablement and a runbook chatbot grounded in team documents.

## What you will learn

- Build a ticket summarisation, classification and routing flow with schema-valid JSON output.
- Route low-confidence and high-priority results to a human review queue.
- Generate deployment checklists, change records and CAB summaries.
- Build an operational chatbot prompt flow grounded in team runbooks.

## Key terms explained

| Term | Plain-English meaning |
|---|---|
| JSON / JSON Schema | JSON is a structured data format machines read easily. A schema defines which fields and values are allowed, so AI output can be checked automatically. |
| Triage | Deciding a ticket's category, priority and the team it goes to. |
| Assignment group | The support team responsible for a ticket (e.g. NETWORK-L2). |
| Confidence score | A number from 0 to 1 the AI gives for how sure it is. Below our threshold (0.80) a human decides. |
| Review queue | The list of AI results that must be checked by a person before they are used. |
| CAB / Change Manager | Change Advisory Board: the group that approves significant changes. The Change Manager runs the change process. |
| Risk score / backout plan | A rating of how risky a change is using an agreed rubric / the plan to undo the change if it fails. |
| Grounding | Making the AI answer only from given sources (your runbooks) and cite them, instead of from general knowledge. |

## Real-time Service Desk use case UC-10 / UC-12: Auto-triage with review queue and change enablement

| | |
|---|---|
| Persona | Service Desk lead, Change Manager |
| Problem statement | In the 9-10 AM peak, triage takes 4-6 minutes per ticket, about 18% are mis-routed, and change records reach CAB with weak backout plans. |
| What AI does | Classifies category, priority, assignment group, duplicates and KB match with a confidence score; drafts change records and risk scores. |
| Human review checkpoint | Desk lead decides every P1/P2, VIP and low-confidence ticket; Change Manager owns the risk score; CAB approves. |
| Output asset | Triage flow, review queue, change-risk prompt pack |
| KPI impact | Reassignment rate, MTTA, change success rate |

## Hands-on labs

### Lab 10.1: Auto-triage and routing with review queue (50 min)

**Objective:** Triage 20 live tickets and route them safely (UC-10).

**Files:** `data/tickets/live_queue.json`, `schemas/triage.schema.json`, `tools/validate_json.py`, `tools/route_triage.py`

**Steps**

1. Agent mode with the itsm-mock server running:

   Copilot Chat prompt:

   ```text
   /triage-json
   ```

2. Validate the JSON. If it fails, improve the prompt and re-run - do not hand-edit:

   Terminal:

   ```bash
   python3 tools/validate_json.py schemas/triage.schema.json outputs/m10/triage.json
   ```

3. Route by confidence and priority:

   Terminal:

   ```bash
   python3 tools/route_triage.py outputs/m10/triage.json
   ```

4. Act as desk lead: open outputs/m10/review_queue.json and record your decisions in outputs/m10/lead_decisions.csv (ticket, ai_value, human_value, reason). Calculate the agreement rate.
5. Add two corrected examples to .github/prompts/triage-json.prompt.md and re-run. Did agreement improve? Check that INC0010247 (injection) went to SECOPS for review.

**Expected result:** Schema-valid triage for 20 tickets; P1/P2, VIP, security and low-confidence tickets in the review queue.

**Check before you finish**

- [ ] VALID from the validator
- [ ] Agreement rate recorded
- [ ] Injection ticket not treated as P1 Network

**Deliverable:** Triage flow, lead decisions and agreement rate.


### Lab 10.2: Change enablement and deployment checklist (30 min)

**Objective:** Complete a change record and CAB pack for the permanent fix (UC-12).

**Files:** `data/changes/CHG0003051.md`, `data/changes/change_risk_rubric.md`

**Steps**

1. Run the prompt with @workspace so Copilot finds the related RCA:

   Copilot Chat prompt:

   ```text
   /change-risk   (changeFile: CHG0003051.md)
   ```

2. Check the risk score against the rubric yourself; adjust and justify any difference.
3. Save the CAB one-pager, deployment checklist, maintenance notice and desk briefing to outputs/m10/.

**Expected result:** Completed change record with implementation, test and backout plans; risk score with reasons; CAB pack.

**Check before you finish**

- [ ] Backout marked tested or untested
- [ ] Risk reasons match the rubric
- [ ] Notice has date, time, impact and contact

**Deliverable:** Change record, risk score and CAB one-pager.


### Lab 10.3: Runbook Q&A assistant (25 min)

**Objective:** Answer operational questions only from team runbooks.

**Files:** `runbooks/`

**Steps**

1. Create .github/prompts/runbook-qa.prompt.md:

   Copilot Chat prompt:

   ```text
   Create a prompt file runbook-qa (mode: ask) that answers ${input:question} using ONLY files in runbooks/ via @workspace,
   quotes the runbook file name and step numbers, and replies 'No runbook covers this - escalate to L2' when nothing matches.
   ```

2. Test five questions, including one with no runbook (for example 'How do I reset the SAN switch?'). It must not invent an answer.

**Expected result:** A grounded runbook assistant that cites its source and admits gaps.

**Check before you finish**

- [ ] Every answer cites a runbook
- [ ] No invented procedure for the unknown question

**Deliverable:** Runbook assistant prompt file.


## Save your work

```bash
git add -A
git commit -m "Module 10 labs"
git push
```
