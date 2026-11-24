#!/usr/bin/env bash
# Environment check for the GenAI InfraOps labs. Read-only. Run from the repository root: ./setup/check_env.sh
set -u
set -o pipefail
pass=0; fail=0
check() { # name, command
  if eval "$2" >/dev/null 2>&1; then printf "  PASS  %-22s %s\n" "$1" "$(eval "$2" 2>/dev/null | head -1)"; pass=$((pass+1));
  else printf "  FAIL  %-22s (not found or not working)\n" "$1"; fail=$((fail+1)); fi
}
echo "GenAI InfraOps lab environment check - $(date '+%Y-%m-%d %H:%M')"
check "git"            "git --version"
check "python3 (3.10+)" "python3 -c 'import sys; assert sys.version_info>=(3,10); print(sys.version.split()[0])'"
check "python packages" "python3 -c 'import jsonschema, pandas, sklearn, mcp; print(\"jsonschema pandas sklearn mcp\")'"
check "docker"         "docker version --format '{{.Server.Version}}'"
check "docker compose" "docker compose version --short"
check "kubectl"        "kubectl version --client -o yaml | grep gitVersion"
check "kind"           "kind version"
check "cluster reachable" "kubectl get nodes --no-headers"
check "helm"           "helm version --short"
check "terraform"      "terraform version | head -1"
check "ansible"        "ansible --version | head -1"
check "ansible-lint"   "ansible-lint --version | head -1"
check "checkov"        "checkov --version"
check "shellcheck"     "shellcheck --version | sed -n 2p"
check "pylint"         "pylint --version | head -1"
check "yamllint"       "yamllint --version"
check "VS Code CLI"    "code --version | head -1"
echo "Result: $pass passed, $fail failed"
[ "$fail" -eq 0 ] && echo "Environment READY" || echo "Report failures to your trainer (screenshot this output)."
