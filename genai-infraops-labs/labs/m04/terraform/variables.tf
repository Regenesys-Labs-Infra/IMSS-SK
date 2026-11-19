variable "network_cidr" {
  description = "CIDR block for the network (must be a valid CIDR)"
  type        = string
  default     = "10.0.0.0/16"

  validation {
    condition     = can(cidrhost(var.network_cidr, 0))
    error_message = "Network CIDR must be a valid CIDR block."
  }
}

variable "vm_size" {
  description = "Size/type of the VM (small, medium, or large)"
  type        = string
  default     = "medium"

  validation {
    condition     = contains(["small", "medium", "large"], var.vm_size)
    error_message = "VM size must be one of: small, medium, large."
  }
}

variable "vm_os" {
  description = "Operating system for the VM (ubuntu-20.04, ubuntu-22.04, or debian-11)"
  type        = string
  default     = "ubuntu-22.04"

  validation {
    condition     = contains(["ubuntu-20.04", "ubuntu-22.04", "debian-11"], var.vm_os)
    error_message = "OS must be one of: ubuntu-20.04, ubuntu-22.04, debian-11."
  }
}

variable "allowed_https_cidr" {
  description = "CIDR block allowed for HTTPS access - restricted for least privilege (default: 10.0.0.0/8)"
  type        = string
  default     = "10.0.0.0/8"

  validation {
    condition     = can(cidrhost(var.allowed_https_cidr, 0))
    error_message = "Allowed HTTPS CIDR must be a valid CIDR block."
  }
}

