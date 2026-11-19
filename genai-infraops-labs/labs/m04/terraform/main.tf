terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "local" {}
provider "random" {}

# Generate a random suffix for unique naming
resource "random_string" "suffix" {
  length  = 4
  special = false
  lower   = true
}

# Network Definition
resource "random_string" "network_name" {
  length  = 8
  special = false
  lower   = true
}

locals {
  network = {
    name = "network-${random_string.network_name.result}"
    cidr = var.network_cidr
  }
}

# VM Definition
locals {
  vm = {
    name = "vm-${random_string.suffix.result}"
    size = var.vm_size
    os   = var.vm_os
  }
}

# Security Group Definition
locals {
  security_group = {
    name = "sg-${random_string.suffix.result}"
    ingress_rules = [
      {
        protocol   = "tcp"
        port       = 443
        cidr_block = var.allowed_https_cidr
      }
    ]
  }
}

# Infrastructure Model as JSON
locals {
  infrastructure_model = {
    network        = local.network
    vm             = local.vm
    security_group = local.security_group
  }
}

# Output the infrastructure model as JSON file
resource "local_file" "infrastructure_model" {
  filename = "${path.module}/infrastructure_model.json"
  content  = jsonencode(local.infrastructure_model)
}
