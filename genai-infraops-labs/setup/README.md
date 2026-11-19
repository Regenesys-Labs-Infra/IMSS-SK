# Lab environment set-up

| Who | When | What |
|---|---|---|
| Lab administrator (Regenesys / Happiest Minds IT) | 2-3 days before Session 1 | Provision one Ubuntu 22.04 VM per participant (2-4 vCPU, 8-16 GB RAM, 80-100 GB disk), run `sudo ./setup/setup_vm.sh <user>` |
| Lab administrator | Same day | Confirm GitHub Copilot Business/Enterprise licences, Agent mode and MCP enabled for the organisation |
| Participant | Before Session 1 | Log in to the VM, accept the GitHub repository invitation, sign in to GitHub in VS Code |
| Participant | Session 1, Lab 1.1 | Clone the repository, `./setup/create_cluster.sh`, `./setup/check_env.sh` |

## Network access required from the VM
github.com, api.github.com, *.githubcopilot.com, copilot-proxy.githubusercontent.com, marketplace.visualstudio.com,
registry-1.docker.io, pypi.org, files.pythonhosted.org, releases.hashicorp.com, dl.k8s.io, kind.sigs.k8s.io.

## Option without a VM: Docker on a laptop
If VMs are not available, a laptop with Docker Desktop, VS Code and GitHub Copilot can run every lab:
install the tools listed in `setup_vm.sh` and run `./setup/create_cluster.sh`.

## Data policy
All data in this repository is synthetic. Do not add real tickets, user names, IP addresses or credentials.
