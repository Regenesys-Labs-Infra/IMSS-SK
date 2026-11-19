# Capstone brief - AI-Powered Infrastructure Operations Assistant
## Scenario
Release 2026.11.12 of the Customer Portal went live at 14:00. Within 15 minutes the desk received 9 tickets
(data/capstone/tickets.csv) and monitoring raised an alert storm (data/capstone/alerts.json).
The broken workloads are in k8s/broken/ (namespace portal).
## Your assistant must
1. Sanitise the tickets. 2. Triage, de-duplicate and route them (review queue for P1/P2, VIP, low confidence).
3. Correlate alerts into one parent incident. 4. Investigate with the read-only Investigator (evidence pack).
5. Propose a fix, get it reviewed, reject once, approve, execute and verify via tools/approve.py.
6. Draft the customer reply, bridge update, RCA, KB article and the change record for the permanent fix.
## Rules
No production action without approval. No secrets in prompts. Everything committed to your team branch.
## Timing
Build 1 h 45 min - demo 8 min per team - peer review 20 min.
## Rubric
Technical correctness 25% - Verification of AI output 20% - Security & governance 20% - Workflow design 20% - Reusability & presentation 15%.
