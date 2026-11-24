# M01 Lab 1.1: Environment Check Result

**Checked:** 2026-11-24
**Working copy:** `genai-infraops-labs` is already present; no clone was attempted because the guide contains a placeholder repository URL.

## Environment check

`./setup/check_env.sh` reports **6 passed, 11 failed**. The checks are from the current host, not the synthetic incident VM.

| Check | Result | Detail |
|---|---|---|
| Git | PASS | 2.43.0 |
| Python 3.10+ | PASS | System Python 3.12.3 |
| Python packages | FAIL | System Python lacks `pandas`; the lab `.venv` has the requirements installed and imports `jsonschema`, `pandas`, `sklearn` and `mcp` successfully. |
| Docker | FAIL | The Docker socket is owned by group `docker`; the current user lacks socket access. The daemon responds when accessed with elevated privileges. |
| Docker Compose | FAIL | The Docker Compose plugin is unavailable. |
| kubectl | PASS | Client v1.37.2 |
| kind | PASS | v0.33.0 |
| Cluster reachable | PASS | Local `genai-labs-control-plane` node is Ready (Kubernetes v1.37.0). |
| Helm | FAIL | Not installed. |
| Terraform | FAIL | Not installed. |
| Ansible | FAIL | Not installed. |
| ansible-lint | FAIL | Not installed. |
| Checkov | FAIL | Not installed. |
| ShellCheck | FAIL | Not installed. |
| Pylint | FAIL | Not installed in system Python. |
| yamllint | FAIL | Not installed. |
| VS Code CLI | PASS | 1.147.0 |

The check script was updated to enable `pipefail`; without it, missing commands in pipelines could be incorrectly reported as PASS. The corrected results above should be shared with the lab administrator/trainer.

## Copilot workbench

The VS Code CLI is available, but this session cannot verify GitHub Copilot sign-in, workspace trust prompts, Copilot Chat mode, or the model picker. The `@workspace` prompt and model comparison therefore were not run in the VS Code UI.

## Repository overview

| Folder | Purpose | Module use |
|---|---|---|
| `.github/` | Copilot instructions, prompt files and chat modes | Across modules; agent modes in M09 |
| `.vscode/` | Workspace settings and MCP server registration | M09 and later agent labs |
| `setup/` | VM checks and local cluster setup | Environment setup and Kubernetes labs |
| `labs/m01`–`labs/m12` | Module guides, scenarios and exercises | Corresponding module |
| `data/` | Synthetic tickets, logs, alerts, CMDB and policies | Across operational labs |
| `k8s/`, `monitoring/`, `runbooks/` | Cluster scenarios, observability and procedures | Infrastructure and operations labs |
| `tools/`, `schemas/`, `mcp/`, `approvals/` | Automation, validation, mock tools and approval workflow | M03–M12, especially M09 |
