# Module 12: Capstone: AI-Powered Infrastructure Operations Assistant

| Day | Session | Theory | Hands-on | Format |
|---|---|---|---|---|
| Day 3 | Session 6 | 0.25 h | 2.75 h | Capstone Project |

Teams assemble everything built in the course into one Operations Assistant in a shared repository and demonstrate a full ticket-to-RCA flow with human approvals.

## What you will learn

- Integrate the prompt library, scripts, IaC, Kubernetes workflow, RCA templates and governance checklist.
- Demonstrate a supervised agent workflow with at least one rejected proposal.
- Present and defend design choices on autonomy and safety.

## Key terms explained

| Term | Plain-English meaning |
|---|---|
| Capstone | The final team project that combines everything built in the course. |
| Branch | Your own line of work in Git, so you can change files without affecting others until merged. |
| Rubric | The scoring guide used to assess the capstone. |

## Real-time Service Desk use case Capstone: End-to-end Service Desk to Infrastructure Operations Assistant

| | |
|---|---|
| Persona | Teams of 3-5 |
| Problem statement | Multiple tickets and alerts after a release need triage, investigation, a safe fix, communication and learning - fast and under control. |
| What AI does | Agents triage, investigate, propose and draft communications. |
| Human review checkpoint | Desk lead, approving engineer and publisher make every decision that changes a ticket, a system or a customer message. |
| Output asset | AI-powered Infrastructure Operations Assistant (Git repository) |
| KPI impact | Demonstrated MTTA, MTTR and audit completeness |

## Hands-on labs

### Capstone: Ticket-to-RCA Operations Assistant (165 min)

**Objective:** After a deployment, 9 tickets ("portal slow", "login errors") and an alert storm arrive. The assistant must handle them end to end.

**Files:** `labs/m12/CAPSTONE_BRIEF.md`, `data/capstone/`

**Steps**

1. Form teams of 3-5 and create a team branch: team/<team-name>. Assign roles: desk lead, investigator, approver, communicator, presenter.
2. Sanitise data/capstone/tickets.csv, then auto-triage and route it (Modules 10-11).
3. Correlate data/capstone/alerts.json into one parent incident (Module 6).
4. Investigate with sd-investigator and produce the evidence pack (Module 9).
5. Propose, review, approve and execute the fix with tools/approve.py; keep one rejected proposal (Module 9).
6. Draft the customer reply, bridge update, RCA, KB article and change record for the permanent fix (Modules 1, 2, 8, 10).
7. Open a pull request with everything; present for 8 minutes: the flow, one AI error you caught, the audit log.

**Expected result:** A working team repository: prompts, chat modes, scripts, evidence, audit log, RCA, KB and change record.

**Check before you finish**

- [ ] Audit log shows the full approval trail
- [ ] No secrets in any prompt or file
- [ ] Rubric criteria covered

**Deliverable:** Team repository with the assistant, audit log and presentation.


## Save your work

```bash
git add -A
git commit -m "Module 12 labs"
git push
```
