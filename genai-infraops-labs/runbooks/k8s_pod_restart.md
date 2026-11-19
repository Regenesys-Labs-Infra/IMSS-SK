# Runbook: Restart a Kubernetes deployment (L2, approval required)
1. Pre-check: `kubectl get deploy <name> -n <ns>` and `kubectl rollout history deploy/<name> -n <ns>`.
2. Submit a remediation plan with command `kubectl rollout restart deployment/<name> -n <ns>` and rollback `kubectl rollout undo`.
3. After approval: `python3 tools/approve.py execute <id>`.
4. Verify: `kubectl rollout status deployment/<name> -n <ns>`.
