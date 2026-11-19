# GenAI & Agentic AI for Infrastructure Operations - Lab Repository
Regenesys Corporate Education | Happiest Minds - Track: GenAI for AI Infra & Ops (24 h, 6 sessions x 4 h)
AI tool: GitHub Copilot in VS Code. All data in this repository is synthetic.

## Start here
1. Lab administrators: see [setup/README.md](setup/README.md).
2. Participants: open [sessions/session-1.md](sessions/session-1.md) and follow Lab 1.1.

## Sessions
| Session | Theme |
|---|---|
| [Session 1](sessions/session-1.md) | Copilot foundations, safe AI usage, runbooks, prompt library, ticket intake and KB |
| [Session 2](sessions/session-2.md) | Script automation kit and Infrastructure-as-Code with security review |
| [Session 3](sessions/session-3.md) | Kubernetes operations and troubleshooting; alert rules and dashboards |
| [Session 4](sessions/session-4.md) | Alert noise reduction, log intelligence, problem management, major incident and RCA |
| [Session 5](sessions/session-5.md) | Agentic AI: Investigator and Resolver agents with approval gates; triage and change workflows |
| [Session 6](sessions/session-6.md) | Governance and AI usage policy; capstone build, demo and review |

## Modules
| Module | Title | Guide |
|---|---|---|
| 1 | Gen AI for Infrastructure Operations | [labs/m01](labs/m01/README.md) |
| 2 | GitHub Copilot for Infrastructure Engineers | [labs/m02](labs/m02/README.md) |
| 3 | AI-Assisted Shell, Python & YAML Automation | [labs/m03](labs/m03/README.md) |
| 4 | Infrastructure-as-Code using AI | [labs/m04](labs/m04/README.md) |
| 5 | AI-Assisted Kubernetes Operations | [labs/m05](labs/m05/README.md) |
| 6 | AI-Powered Observability & Monitoring | [labs/m06](labs/m06/README.md) |
| 7 | Intelligent Log Monitoring & Analysis | [labs/m07](labs/m07/README.md) |
| 8 | AI-Driven Incident Management & RCA | [labs/m08](labs/m08/README.md) |
| 9 | Agentic AI for Infrastructure Operations | [labs/m09](labs/m09/README.md) |
| 10 | AI Agents for Operational Workflows | [labs/m10](labs/m10/README.md) |
| 11 | Guardrails, Governance & Secure AI Operations | [labs/m11](labs/m11/README.md) |
| 12 | Capstone: AI-Powered Infrastructure Operations Assistant | [labs/m12](labs/m12/README.md) |

## Repository map
| Folder | Purpose |
|---|---|
| .github/copilot-instructions.md | Team rules Copilot follows in this repository |
| .github/prompts/ | Reusable prompt files (run with /name in Copilot Chat) |
| .github/chatmodes/ | sd-investigator (read-only) and sd-resolver (propose-only) agents |
| .vscode/ | MCP server registration and safe settings (auto-approve off) |
| setup/ | VM preparation, cluster creation and environment check |
| sessions/ | One instruction guide per session |
| labs/m01 ... m12 | One instruction guide and starter files per module |
| data/ | Synthetic tickets, alerts, logs, incidents, KB, CMDB, policies, changes, capstone |
| k8s/, monitoring/, runbooks/ | Kubernetes faults and RBAC, Prometheus/Grafana stack, team runbooks |
| tools/, schemas/, mcp/ | Sanitiser, validators, routers, SLA calculator, approval gate, JSON schemas, mock ITSM MCP server |
| approvals/ | Agent proposals (pending/approved/rejected/executed) and audit.log |
| outputs/ | Your lab outputs |

## Human-in-the-loop rules
Agents only read, draft or propose. A named person approves every change (tools/approve.py), with a second confirmation at execution; every decision is written to approvals/audit.log.
