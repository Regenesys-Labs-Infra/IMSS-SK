# Module 6: AI-Powered Observability & Monitoring

| Day | Session | Theory | Hands-on | Format |
|---|---|---|---|---|
| Day 2 | Sessions 3-4 | 0.25 h | 1.75 h | Monitoring Lab |

Participants generate alert rules and dashboards, then fix the alert-to-ticket pipeline so monitoring creates fewer, better tickets.

## What you will learn

- Generate Prometheus alert rules and PromQL and validate them with promtool.
- Define SLIs and SLOs and reduce alert fatigue.
- Generate Grafana dashboard JSON and SRE health reports from metrics exports.
- Write alert playbooks that L1 can follow.

## Key terms explained

| Term | Plain-English meaning |
|---|---|
| Metric | A number measured over time, such as CPU %, memory used or HTTP errors per second. |
| Prometheus / PromQL | Prometheus collects metrics; PromQL is its query language for calculating and alerting on them. |
| Alert rule | A condition (PromQL) that fires an alert when true for a set time, with labels (severity) and annotations (description, runbook). |
| promtool | Prometheus's checker: 'promtool check rules file.yml' validates alert rules before they are loaded. |
| Grafana | A dashboard tool that charts Prometheus metrics. Dashboards are stored as JSON. |
| SLI / SLO / Error budget | SLI = what we measure (e.g. % successful logins). SLO = the target (99.5%). Error budget = how much failure the SLO allows. |
| Alert fatigue | So many noisy alerts that people stop reacting to them - including the important ones. |
| Correlation / de-duplication | Grouping many alerts caused by the same event into one incident, instead of one ticket per alert. |
| NOC | Network Operations Centre: the team watching monitoring and alerts. |

## Real-time Service Desk use case UC-05: Alert-to-incident enrichment and noise reduction

| | |
|---|---|
| Persona | NOC / SRE / monitoring desk |
| Problem statement | Monitoring creates tickets like "ALERT: HighCPU srv-fin-app-02" with no impact, owner or first step. During an alert storm, 47 alerts create 47 tickets for one root event and MTTA for the real incident suffers. |
| What AI does | Correlates alerts by CI and time window, enriches the parent incident from the CMDB and rewrites alert annotations. |
| Human review checkpoint | NOC lead approves the correlation rule and ticket template before it is used. |
| Output asset | Enriched alert rules and parent/child incident template |
| KPI impact | Duplicate tickets, MTTA |

## Hands-on labs

### Lab 6.1: Alert rules and dashboard (45 min)

**Objective:** Create node, pod and application alerts and a Grafana dashboard.

**Files:** `monitoring/docker-compose.yml`, `monitoring/rules/node_alerts.yml`

**Steps**

1. Start the monitoring stack and open Grafana (http://localhost:3000, admin / admin, change password on first login):

   Terminal:

   ```bash
   cd monitoring && docker compose up -d && cd -
   ```

2. Improve the rules with Copilot:

   Copilot Chat prompt:

   ```text
   In #file:monitoring/rules/node_alerts.yml add alerts for memory > 90% for 5m and node exporter down.
   For every alert add annotations: summary, impact, first_checks, owner_group, runbook_url (use TBD if unknown).
   ```

3. Validate:

   Terminal:

   ```bash
   docker run --rm -v $PWD/monitoring/rules:/r --entrypoint promtool prom/prometheus check rules /r/node_alerts.yml
   ```

4. Ask Copilot for a Grafana dashboard JSON (CPU, memory, disk, HTTP 5xx) and import it in Grafana (Dashboards > New > Import).
5. Use /troubleshooting-checklist to write playbooks for the top 3 alerts into runbooks/alerts/.

**Expected result:** Rules pass promtool; dashboard imported; 3 alert playbooks.

**Check before you finish**

- [ ] promtool SUCCESS
- [ ] Every alert has owner_group and first_checks

**If something goes wrong**

- Port 3000 in use: docker compose down then up again, or ask the trainer.

**Deliverable:** Validated rules, dashboard JSON and 3 alert playbooks.


### Lab 6.2: Alert-to-incident enrichment and noise reduction (60 min)

**Objective:** Turn an alert storm into a few enriched parent incidents (Service Desk use case UC-05).

**Files:** `data/alerts/alerts_stream.json`, `data/cmdb/ci_inventory.csv`, `data/metrics/metrics_export.csv`

**Steps**

1. Ask Copilot (Agent mode):

   Copilot Chat prompt:

   ```text
   Create tools/correlate_alerts.py: read data/alerts/alerts_stream.json and data/cmdb/ci_inventory.csv,
   group alerts by business_service within a 5-minute window, and write outputs/m06/alert_groups.json
   with group_id, business_service, root_candidate, child_alert_ids, count. Print a summary table.
   ```

2. Run it and compare with a chat-only grouping of the same file. Discuss: which is repeatable?

   Terminal:

   ```bash
   python3 tools/correlate_alerts.py
   ```

3. Run /alert-enrich for the largest group to produce the parent incident text.
4. Generate the weekly SRE health report from data/metrics/metrics_export.csv (top risks, trends, recommended actions).

**Expected result:** 47 alerts reduced to a few parent incidents; enriched incident text; SRE report.

**Check before you finish**

- [ ] Group count far below 47
- [ ] Owner group exists in data/policy/assignment_groups.json

**Deliverable:** Correlation script, enriched rules and SRE report.


## Save your work

```bash
git add -A
git commit -m "Module 6 labs"
git push
```
