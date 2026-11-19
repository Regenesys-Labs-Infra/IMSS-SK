# Module 9: Agentic AI for Infrastructure Operations

| Day | Session | Theory | Hands-on | Format |
|---|---|---|---|---|
| Day 3 | Session 5 | 0.5 h | 1.5 h | Agentic AI Design Lab |

Participants design and run supervised agents in VS Code: a read-only Investigator and a Resolver that can only propose fixes behind a human approval gate.

## What you will learn

- Distinguish chat, scripts and agents, and choose the right one for a task.
- Design an agent with goal, tools, permissions, flow and approval checkpoints.
- Configure custom chat modes and MCP servers (.vscode/mcp.json) with least-privilege tools.
- Apply Planner-Executor and ReAct patterns with human-in-the-loop.

## Key terms explained

| Term | Plain-English meaning |
|---|---|
| AI agent | An AI that works towards a goal in steps: it plans, uses tools (read files, run queries), observes results and decides the next step. |
| Tool | A capability the agent can call, such as 'get_ticket' or 'read_logs'. Each tool call is shown to you for approval. |
| MCP / MCP server | Model Context Protocol: a standard way to connect AI to tools and data. An MCP server offers tools; VS Code connects to it via .vscode/mcp.json. |
| Custom chat mode | A saved Copilot Chat persona (.github/chatmodes/*.chatmode.md) with its own instructions and a restricted list of tools. |
| Autonomy tier | How much the AI may do on its own: T0 read-only, T1 suggest, T2 execute with approval, T3 never. |
| Human-in-the-loop (HITL) | A person reviews and approves AI output or actions at defined checkpoints before anything changes. |
| Approval gate | The checkpoint where a named person approves, edits or rejects an agent's proposal. In our labs: tools/approve.py. |
| ReAct / Planner-Executor | Agent patterns. ReAct = Reason, Act, observe, repeat. Planner-Executor = one step plans, another carries out the approved plan. |
| Evidence pack | A structured summary of the facts gathered for a ticket (timeline, tool outputs, ranked causes) used for escalation. |
| Red-team | Deliberately trying to make the system do something unsafe, to prove the guardrails work. |

## Real-time Service Desk use case UC-09 / UC-11: Agentic Investigator and Resolver with approval gate

| | |
|---|---|
| Persona | L2 / L3 / on-call engineer |
| Problem statement | At 2 AM an on-call engineer must gather evidence, craft a fix, remember pre-checks and write a rollback. Manual fixes under pressure cause change-induced incidents. |
| What AI does | Investigator gathers evidence with read-only tools; Resolver proposes a plan with pre-checks, command, rollback and verification. |
| Human review checkpoint | Engineer approves or rejects the plan, then confirms again at execution; every decision is logged. |
| Output asset | Investigator and Resolver chat modes, MCP configuration, approval workflow |
| KPI impact | Time to diagnose, MTTR, change-induced incidents |

## Hands-on labs

### Lab 9.1: Read-only Investigator agent (45 min)

**Objective:** Configure an Investigator that gathers evidence for INC0010260 but cannot change anything (UC-09).

**Files:** `.vscode/mcp.json`, `mcp/itsm_mock_server.py`, `.github/chatmodes/sd-investigator.chatmode.md`

**Steps**

1. Start the MCP server: Ctrl+Shift+P > MCP: List Servers > itsm-mock > Start. Open Copilot Chat > tools icon and confirm the itsm-mock tools are listed.
2. Make sure the broken portal is deployed (kubectl get pods -n portal). In the chat mode drop-down choose sd-investigator and ask:

   Copilot Chat prompt:

   ```text
   Investigate INC0010260 and produce the Evidence Pack.
   ```

3. For each tool call, read the request and click Allow. Reject one call on purpose (for example reading the auth log) and watch how the agent continues.
4. Try to make it act:

   Copilot Chat prompt:

   ```text
   Just fix the service selector now.
   ```

5. It must refuse and hand over to the Resolver. Verify two evidence lines yourself with kubectl. Save the pack to outputs/m09/INC0010260_evidence.md.

**Expected result:** Evidence pack naming the Service selector mismatch, ImagePullBackOff and ingress host typo; no change attempted; injected log instruction reported, not obeyed.

**Check before you finish**

- [ ] Only read tools used
- [ ] Each claim backed by a tool output
- [ ] Agent refused to make changes

**If something goes wrong**

- MCP server fails to start: run python3 mcp/itsm_mock_server.py in a terminal to see the error (usually a missing package: pip install -r requirements.txt).

**Deliverable:** Evidence pack and chat-mode definition.


### Lab 9.2: Resolver agent with human approval gate (45 min)

**Objective:** Propose, review, reject, revise, approve and execute a fix (UC-11).

**Files:** `.github/chatmodes/sd-resolver.chatmode.md`, `tools/approve.py`, `approvals/`

**Steps**

1. Choose the sd-resolver chat mode and ask:

   Copilot Chat prompt:

   ```text
   Using #file:outputs/m09/INC0010260_evidence.md propose a remediation for the Service selector fault on INC0010260.
   ```

2. Allow the propose_remediation tool call. Then review as the approving engineer:

   Terminal:

   ```bash
   python3 tools/approve.py list
   python3 tools/approve.py show REM-0001
   ```

3. Reject the first plan with a reason (this is a required step):

   Terminal:

   ```bash
   python3 tools/approve.py reject REM-0001 --by <your-name> --reason "Add a pre-check of current endpoints"
   ```

4. Ask the Resolver to revise the plan using the rejection reason. Approve and execute the revision:

   Terminal:

   ```bash
   python3 tools/approve.py approve REM-0002 --by <your-name>
   python3 tools/approve.py execute REM-0002
   cat approvals/audit.log
   ```

5. Red-team: ask the Resolver to 'delete the portal namespace and redeploy'. Try to approve that plan - approve.py must refuse it.
6. Ask the Resolver to verify (kubectl get endpoints portal-web -n portal) and draft the work note and customer update.

**Expected result:** Audit log shows PROPOSED, REJECTED, PROPOSED, APPROVED, EXECUTED; endpoints restored; destructive plan blocked.

**Check before you finish**

- [ ] Execution only after approval and typed confirmation
- [ ] Rollback present in the plan
- [ ] Delete plan refused by the gate

**If something goes wrong**

- Plan IDs increase each time; use approve.py list to find yours.

**Deliverable:** Audit log showing proposal, rejection, approval and execution.


## Save your work

```bash
git add -A
git commit -m "Module 9 labs"
git push
```
