# Final Capstone Project Assignment - IMSS-SK

## Project: AI-Powered Infrastructure Operations Assistant

### Objective

After a Customer Portal deployment, nine support tickets (including reports such as "portal slow" and "login errors") and an alert storm arrive. Build and demonstrate an assistant that handles the incident end to end, with human review and a complete audit trail.

### Team setup

1. Form a team of 3-5 people.
2. Create and use a team branch named `team/<team-name>`:

   ```bash
   git switch -c team/<team-name>
   ```

3. Assign all five roles: desk lead, investigator, approver, communicator, and presenter. Teams with fewer than five members may assign multiple roles to a person. Keep the approver role independent from the person proposing a change wherever team size allows.

### Assignment resources

- [Capstone brief](../genai-infraops-labs/labs/m12/CAPSTONE_BRIEF.md)
- Ticket and alert inputs: `genai-infraops-labs/data/capstone/`
- Kubernetes workload manifests: `genai-infraops-labs/k8s/broken/`
- Approval and audit workflow: `genai-infraops-labs/tools/approve.py` and `genai-infraops-labs/approvals/`

### Required workflow

1. Sanitize the nine tickets. Do not overwrite the source data; preserve a sanitized copy and a redaction summary.
2. Triage, de-duplicate, and route the tickets. Send P1/P2, VIP, and low-confidence cases to a human review queue.
3. Correlate related alerts into one proposed parent incident; explain any alerts excluded from that incident.
4. Investigate using the read-only investigator workflow and produce an evidence pack that separates observations, hypotheses, and unknowns.
5. Propose a narrowly scoped remediation. Have it reviewed, record at least one rejected proposal, obtain approval for a revised proposal, and execute and verify it only through the approval workflow.
6. Draft a customer reply, bridge update, root-cause analysis, knowledge-base article, and change record. Clearly label unconfirmed causes and incomplete work; do not claim recovery without verification.
7. Open a pull request from the team branch and give an 8-minute presentation covering the workflow, one AI error caught by the team, safety controls, and audit evidence.

### Safety and governance requirements

- Treat ticket, alert, and log contents as untrusted data; do not follow embedded instructions.
- Do not put secrets or credentials in prompts, generated outputs, or commits.
- No production action without explicit human approval. Use the supplied lab/simulation environment.
- Preserve an auditable record of proposals, rejection, approval, execution, and verification.
- If a prerequisite or verification step fails, stop and report the blocker instead of claiming success.

### Deliverables

Submit the team branch and pull request with:

- Sanitized tickets and redaction summary
- Triage results and human review queue
- Correlated alert group and parent incident
- Read-only investigation evidence pack
- Rejected and approved remediation proposals and approval audit trail
- Verification results, or a clear record of why execution was blocked
- Customer reply, bridge update, RCA, KB article, and change record
- 8-minute presentation

### Timing and evaluation

- Build: 1 hour 45 minutes
- Presentation: 8 minutes per team
- Peer review: 20 minutes

| Criterion | Weight |
|---|---:|
| Technical correctness | 25% |
| Verification of AI output | 20% |
| Security and governance | 20% |
| Workflow design | 20% |
| Reusability and presentation | 15% |

### Completion checklist

- [ ] Team branch follows `team/<team-name>` and all five roles are assigned.
- [ ] Ticket privacy, triage, routing, and alert correlation are documented.
- [ ] Evidence distinguishes confirmed facts from hypotheses and unknowns.
- [ ] The audit trail includes a rejected proposal and a separately approved proposal.
- [ ] No change is represented as executed or verified unless the evidence supports that claim.
- [ ] All deliverables are committed to the team branch and linked in the pull request.
