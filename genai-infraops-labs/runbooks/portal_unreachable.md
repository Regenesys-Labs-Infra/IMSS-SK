# Runbook: Customer portal unreachable (L2)
1. Confirm scope: one user, one site or all users? Check the status page and open P1/P2 incidents.
2. `kubectl get ingress -n portal` - host name correct?
3. `kubectl get endpoints portal-web -n portal` - at least 1 address? If none, compare Service selector with pod labels.
4. `kubectl get pods -n portal` - all Running and Ready? If not, `kubectl describe pod` and read Events.
5. `kubectl get events -n portal --sort-by=.lastTimestamp | tail -20`
6. Any change in the last 24 h? Check the change calendar.
Any fix that changes the cluster: write a remediation plan and get L2/L3 approval (tools/approve.py).
Escalate to K8S-PLATFORM-L3 when: node or cluster-wide issue, or cause not found in 30 minutes.
