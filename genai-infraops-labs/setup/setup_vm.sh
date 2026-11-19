#!/usr/bin/env bash
# One-time VM preparation for Ubuntu 22.04 (run by the lab administrator with sudo rights, 2-3 days before Session 1).
# Usage: sudo ./setup/setup_vm.sh <participant-username>
set -euo pipefail
USER_NAME="${1:?usage: sudo ./setup/setup_vm.sh <participant-username>}"
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y git curl wget vim nano tree unzip jq build-essential python3 python3-pip python3-venv \
  shellcheck yamllint net-tools dnsutils traceroute ca-certificates gnupg lsb-release software-properties-common
# Docker
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list
# HashiCorp (Terraform)
curl -fsSL https://apt.releases.hashicorp.com/gpg | gpg --dearmor -o /etc/apt/keyrings/hashicorp.gpg
echo "deb [signed-by=/etc/apt/keyrings/hashicorp.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" > /etc/apt/sources.list.d/hashicorp.list
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin terraform
usermod -aG docker "$USER_NAME"
# kubectl, kind, helm
curl -fsSLo /usr/local/bin/kubectl "https://dl.k8s.io/release/$(curl -fsSL https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && chmod +x /usr/local/bin/kubectl
curl -fsSLo /usr/local/bin/kind https://kind.sigs.k8s.io/dl/v0.24.0/kind-linux-amd64 && chmod +x /usr/local/bin/kind
curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
# Python tools (system-wide for simplicity on a training VM)
pip3 install --upgrade ansible ansible-lint checkov pylint pytest jsonschema pandas scikit-learn "mcp>=1.2,<2"
# VS Code
curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /etc/apt/keyrings/microsoft.gpg
echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list
apt-get update && apt-get install -y code
sudo -u "$USER_NAME" code --install-extension GitHub.copilot --install-extension GitHub.copilot-chat \
  --install-extension ms-python.python --install-extension redhat.vscode-yaml \
  --install-extension ms-kubernetes-tools.vscode-kubernetes-tools --install-extension hashicorp.terraform \
  --install-extension timonwong.shellcheck || true
# Lab folder
mkdir -p /opt/genai-infra-labs && chown -R "$USER_NAME":"$USER_NAME" /opt/genai-infra-labs
# Allow the participant to restart only the lab services without a password (used in Lab 3.3)
echo "$USER_NAME ALL=(root) NOPASSWD: /usr/bin/systemctl restart nginx, /usr/bin/systemctl restart cron, /usr/bin/systemctl restart docker" > /etc/sudoers.d/genai-labs
chmod 440 /etc/sudoers.d/genai-labs
apt-get install -y nginx && systemctl enable --now nginx
echo "Done. Ask the participant to log out and in again (docker group), then run ./setup/create_cluster.sh and ./setup/check_env.sh"
