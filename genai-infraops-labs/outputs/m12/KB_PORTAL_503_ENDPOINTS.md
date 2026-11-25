# Draft KB - Customer Portal sign-in errors and missing web endpoints

**Status:** Draft only. Validate against live evidence and obtain Knowledge Manager approval before publishing.
**Applies to:** Customer Portal (`portal-web`, `portal-api`, `nginx-edge-01`) - verify CI/service mapping before use.

## Symptoms

- Users report sign-in errors or HTTP 503.
- Monitoring reports elevated edge HTTP 5xx, portal pod readiness failures, image-pull failures, or low login success.

## Read-only checks

Use the approved, verified Kubernetes context and the `portal` namespace for all checks.

1. Confirm the affected scope and check the current incident/status page.
2. Inspect the `portal-web` Service selector and deployment pod-template labels:

   ```text
   kubectl get service portal-web -n portal --context <verified-context> -o yaml
   kubectl get deployment portal-web -n portal --context <verified-context> -o yaml
   ```

3. Inspect the Service endpoints and ready pods:

   ```text
   kubectl get endpoints portal-web -n portal --context <verified-context>
   kubectl get pods -n portal --context <verified-context> -l app=portal-web
   ```

4. If the Service selector does not match the pod labels or endpoints are empty, capture the outputs and escalate to APP-PORTAL-L2. Do not patch the Service from this article.
5. For `portal-api` image-pull alerts, collect the pod events and escalate to K8S-PLATFORM-L3. Do not guess or substitute an image tag.
6. For an Ingress hostname concern, verify the approved hostname with the service owner before escalation to LINUX-L2.

## Resolution status

The selector correction is proposed but was not applied: the approval gate stopped because `kubectl` was unavailable. Do not tell users the issue is resolved or publish a fix until the approved change is executed and endpoints and customer-facing checks pass.

## Escalation

- APP-PORTAL-L2: portal Service, application symptoms, and customer impact.
- K8S-PLATFORM-L3: pod readiness, image-pull events, or cluster/platform findings.
- LINUX-L2: edge and Ingress routing.

## Source

[CAP-MI-001 evidence pack](./CAP-MI-001_evidence.md). Historical log lines cited there are dated Nov 9 and must not be used as proof of current state.
