# Module 4: Infrastructure-as-Code using AI

| Day | Session | Theory | Hands-on | Format |
|---|---|---|---|---|
| Day 1 | Session 2 | 0.25 h | 2.75 h | Hands-On IaC Lab |

Participants generate Terraform and Ansible with Copilot Agent mode, then catch the security and cost flaws AI commonly introduces.

## What you will learn

- Generate Terraform for network, compute and security groups, and Ansible playbooks for OS hardening.
- Validate IaC with terraform fmt/validate/plan and ansible-lint before any apply.
- Review AI-generated IaC for open security groups, public storage, hard-coded secrets and oversized instances.
- Document and refactor modules with Copilot.

## Key terms explained

| Term | Plain-English meaning |
|---|---|
| Infrastructure-as-Code (IaC) | Describing servers, networks and settings in code files, so they can be reviewed, versioned in Git and built the same way every time. |
| Terraform | An IaC tool. 'terraform plan' shows what would change; 'terraform apply' makes the change. We always review the plan first. |
| Ansible playbook | A YAML file listing configuration tasks Ansible runs on servers (install, harden, configure). '--check' runs it as a dry-run. |
| Security group / firewall rule | Network rules deciding which traffic may reach a server. 0.0.0.0/0 means 'the whole internet'. |
| Checkov / tfsec | Scanners that find security and compliance problems in IaC files before they are deployed. |
| Least privilege | Give only the minimum access needed for the task - nothing more. |
| Service request | A user asking for something standard (new VM, access, software), as opposed to reporting something broken (an incident). |
| Change request | A formal record proposing a change to production, assessed for risk and approved before it is made. |

## Real-time Service Desk use case UC-04B: Self-service VM request and firewall change risk triage

| | |
|---|---|
| Persona | L2 / Cloud Ops / InfraSec |
| Problem statement | "New VM" requests wait days for manual build, and firewall requests such as "open port 22 to the world" reach implementers without any risk check. |
| What AI does | Copilot generates a parameterised module and a fulfilment checklist; a prompt file flags risky rules with the failed Checkov checks. |
| Human review checkpoint | Cloud Ops approves the plan output; InfraSec decides on any internet-exposed rule. |
| Output asset | Request fulfilment templates and firewall risk-triage prompt |
| KPI impact | Request fulfilment time, insecure changes blocked |

## Hands-on labs

### Lab 4.1: Generate Terraform and Ansible (60 min)

**Objective:** Create a VPC/network, VM and security group in Terraform plus an nginx hardening playbook.

**Files:** `labs/m04/terraform/`, `labs/m04/ansible/`

**Steps**

1. Switch to Agent mode and ask:

   Copilot Chat prompt:

   ```text
   In labs/m04/terraform create main.tf, variables.tf and outputs.tf using the local and random providers to model:
   a network (name, CIDR), a VM definition (name, size, OS) and a security group allowing HTTPS from 10.0.0.0/8 only.
   Write the model as a local_file JSON output. Then run terraform init, fmt and validate.
   ```

2. Agent mode will ask before each terminal command. Read each one, then click Continue. Afterwards run the plan yourself:

   Terminal:

   ```bash
   cd labs/m04/terraform && terraform plan && cd -
   ```

3. Generate labs/m04/ansible/harden_nginx.yml (disable server_tokens, add security headers, ensure nginx enabled) and check it:

   Terminal:

   ```bash
   ansible-lint labs/m04/ansible/harden_nginx.yml
   ansible-playbook -i localhost, -c local --check labs/m04/ansible/harden_nginx.yml
   ```


**Expected result:** terraform plan succeeds; the playbook passes ansible-lint and runs in --check mode.

**Check before you finish**

- [ ] No 0.0.0.0/0 rules
- [ ] Variables have descriptions
- [ ] --check run without errors

**If something goes wrong**

- If the participant VM has no internet for providers, the trainer can enable the provider mirror in setup/terraformrc.

**Deliverable:** Validated Terraform plan and lint-clean playbook.


### Lab 4.2: Security and cost review of AI-generated IaC (50 min)

**Objective:** Find and fix 3 planted flaws.

**Files:** `labs/m04/review/insecure.tf`

**Steps**

1. Open labs/m04/review/insecure.tf. Before scanning, write down what looks risky.
2. Scan and explain:

   Terminal:

   ```bash
   checkov -d labs/m04/review --compact
   ```

3. Ask Copilot:

   Copilot Chat prompt:

   ```text
   Explain each failed Checkov check in #file:labs/m04/review/insecure.tf in plain English, rate the risk and propose the least-privilege fix.
   ```

4. Fix the file in Edit mode, re-run Checkov until clean, then generate labs/m04/review/README.md with /doc.

**Expected result:** Checkov passes for the 3 planted issues (open SSH, public bucket, hard-coded secret).

**Check before you finish**

- [ ] Secret moved to a variable marked sensitive
- [ ] SSH limited to a bastion CIDR
- [ ] Bucket not public

**If something goes wrong**

- Checkov may report extra checks; fix the three planted ones and discuss the rest.

**Deliverable:** Clean Checkov report and README.


### Lab 4.3: Self-service request fulfilment and change risk triage (55 min)

**Objective:** Turn a "New developer VM" ticket into a parameterised module, and triage a firewall change request.

**Files:** `labs/m04/request_vm/`, `data/changes/fw_request.tf`, `.github/prompts/change-risk.prompt.md`

**Steps**

1. Ask Copilot (Agent mode) to create a module in labs/m04/request_vm/ with variables size (small/medium/large), os and owner, and a REQUEST_CHECKLIST.md for the Service Desk.
2. Triage the firewall request:

   Copilot Chat prompt:

   ```text
   Act as InfraSec reviewer. Review #file:data/changes/fw_request.tf. List risks, failed controls, a safer alternative rule
   and a recommendation (approve / reject / approve with changes). Output a short risk note.
   ```

3. Save the note to outputs/m04/fw_risk_note.md, commit and open a pull request.

**Expected result:** A request module with a desk checklist and a firewall risk note recommending a restricted CIDR.

**Check before you finish**

- [ ] Module validates
- [ ] Risk note rejects 0.0.0.0/0 for SSH

**Deliverable:** Request module, desk checklist and firewall risk note.


## Save your work

```bash
git add -A
git commit -m "Module 4 labs"
git push
```
