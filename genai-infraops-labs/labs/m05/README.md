# Module 5: AI-Assisted Kubernetes Operations

| Day | Session | Theory | Hands-on | Format |
|---|---|---|---|---|
| Day 2 | Session 3 | 0.25 h | 2.75 h | Kubernetes Lab |

Participants generate production-grade manifests, diagnose broken workloads with Copilot reading real kubectl output, and build the L2-to-L3 escalation evidence pack.

## What you will learn

- Generate Deployment, Service, ConfigMap and Ingress YAML with probes, limits and labels.
- Diagnose CrashLoopBackOff, ImagePullBackOff, OOMKilled, Pending and Service selector faults.
- Use @terminal and #terminalLastCommand so Copilot reasons over actual cluster output.
- Review RBAC and pod security for least privilege.

## Key terms explained

| Term | Plain-English meaning |
|---|---|
| Container | A packaged application with everything it needs to run, started from an image (for example nginx:1.27-alpine). |
| Kubernetes (K8s) | A platform that runs and manages containers across machines. kind and minikube run a small Kubernetes cluster on your VM. |
| Pod / Deployment | A pod is one running instance of a container. A Deployment keeps the requested number of pods running and replaces failed ones. |
| Service / selector / endpoints | A Service gives pods a stable address. It finds pods using a label selector; the matching pods are its endpoints. Wrong selector = 0 endpoints = app unreachable. |
| Ingress | The entry point that routes web traffic from outside the cluster (a hostname) to a Service. |
| Namespace | A folder-like boundary inside a cluster that groups related resources (our app lives in namespace 'portal'). |
| kubectl | The command-line tool for Kubernetes: get (list), describe (details and events), logs (container output). |
| CrashLoopBackOff / ImagePullBackOff | Pod states: the container keeps crashing and restarting / Kubernetes cannot download the container image (often a wrong tag). |
| OOMKilled / Pending | The container used more memory than its limit and was killed / the pod cannot be scheduled because no node has enough resources. |
| RBAC | Role-Based Access Control: rules defining who can do which actions on which Kubernetes resources. |
| L1 / L2 / L3 | Support levels. L1 = Service Desk first contact; L2 = technical specialists; L3 = engineering / platform experts. |

## Real-time Service Desk use case UC-07K: "Portal unreachable" Kubernetes decision tree

| | |
|---|---|
| Persona | L2 / L3 engineer |
| Problem statement | An L2 engineer spends about 40 minutes collecting evidence for an application-unreachable ticket. Escalations reach L3 without evidence, so L3 repeats the work and the ticket is reassigned twice. |
| What AI does | Copilot interprets kubectl output, ranks likely causes and drafts the customer update and escalation pack. |
| Human review checkpoint | L2 verifies every evidence line with their own command before escalating. |
| Output asset | Troubleshooting playbook and L2-to-L3 escalation template |
| KPI impact | Time to diagnose, reassignment count |

## Hands-on labs

### Lab 5.1: Generate and deploy manifests (40 min)

**Objective:** Deploy a sample web app and API to kind or minikube.

**Files:** `labs/m05/app/`

**Steps**

1. Make sure the cluster is running:

   Terminal:

   ```bash
   kubectl get nodes
   kubectl create namespace demo
   ```

2. Ask Copilot (Edit mode):

   Copilot Chat prompt:

   ```text
   Create labs/m05/app/deployment.yaml, service.yaml and configmap.yaml for an nginx web app in namespace demo:
   3 replicas, readiness and liveness probes, CPU/memory requests and limits, labels app=web.
   ```

3. Validate, apply and watch:

   Terminal:

   ```bash
   kubectl apply --dry-run=server -f labs/m05/app/
   kubectl apply -f labs/m05/app/
   kubectl rollout status deployment/web -n demo
   ```

4. Select the rollout output, Ctrl+I, /explain.

**Expected result:** 3 web pods Running and Ready in namespace demo.

**Check before you finish**

- [ ] Probes and limits set
- [ ] Service has 3 endpoints (kubectl get endpoints -n demo)

**If something goes wrong**

- kind cluster missing: run ./setup/create_cluster.sh.

**Deliverable:** Running workload and manifests in the repository.


### Lab 5.2: Diagnose 4 broken workloads (70 min)

**Objective:** Find root cause and fix for planted faults.

**Files:** `k8s/broken/`

**Steps**

1. Deploy the broken workloads:

   Terminal:

   ```bash
   kubectl apply -f k8s/broken/
   kubectl get pods,svc,endpoints -n portal
   ```

2. For each problem, collect evidence and ask Copilot to reason over the real output:

   Terminal:

   ```bash
   kubectl describe pod <pod-name> -n portal
   kubectl get events -n portal --sort-by=.lastTimestamp | tail -20
   ```

3. Then in Chat:

   Copilot Chat prompt:

   ```text
   @terminal Using the last kubectl output, what is the most likely root cause? Quote the evidence line. Suggest a read-only command to confirm.
   ```

4. Record each fault in labs/m05/diagnosis.md: Symptom | Evidence | Root cause | Fix.
5. Open k8s/rbac/overpermissive-role.yaml and ask Copilot to reduce it to read-only access to pods and logs in namespace portal.

**Expected result:** Four faults diagnosed: ImagePullBackOff, Service with 0 endpoints, OOMKilled, Pending.

**Check before you finish**

- [ ] Every diagnosis cites an evidence line
- [ ] RBAC role has no '*' verbs

**If something goes wrong**

- The OOM pod may take a minute to fail; use kubectl get pods -w.

**Deliverable:** Diagnosis log and corrected RBAC role.


### Lab 5.3: "Portal unreachable" decision tree and escalation pack (55 min)

**Objective:** Build the L2 workflow for an application-unreachable ticket (Service Desk use case).

**Files:** `data/tickets/live_queue.json (INC0010260)`, `k8s/broken/portal.yaml`

**Steps**

1. Ask Copilot to draft the L2 decision tree:

   Copilot Chat prompt:

   ```text
   Create a decision tree for the ticket 'Customer portal unreachable' on Kubernetes:
   DNS > Ingress > Service endpoints > Pod status > Events > Recent change.
   For each node: the read-only kubectl command, what good looks like, what bad looks like, next node.
   ```

2. Walk the tree against namespace portal and INC0010260. Record the evidence at each node.
3. Generate the customer update (max 80 words, no hostnames) and the L2-to-L3 escalation pack: summary, evidence, ruled out, suspected cause, requested action.
4. Ask for a daily cluster health checklist; save all outputs under outputs/m05/.

**Expected result:** Playbook, customer update and escalation pack under outputs/m05/.

**Check before you finish**

- [ ] Escalation pack contains evidence lines, not opinions
- [ ] Customer update has no internal details

**Deliverable:** Kubernetes troubleshooting playbook and escalation template.


## Save your work

```bash
git add -A
git commit -m "Module 5 labs"
git push
```
