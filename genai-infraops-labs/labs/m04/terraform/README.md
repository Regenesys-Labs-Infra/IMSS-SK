# Lab 4.1 workspace
Copilot Agent mode will create main.tf, variables.tf and outputs.tf here.
The lab uses only the `local` and `random` providers, so no cloud account is needed.
If your trainer enables the AWS sandbox, a limited IAM user is provided separately - never paste its keys into chat.

Run `terraform init`, `terraform fmt`, `terraform validate`, and `terraform plan`
to review the model. `terraform apply` writes `infrastructure_model.json`; no
cloud resources are created. The modeled security group allows TCP port 443
from `10.0.0.0/8` only.
