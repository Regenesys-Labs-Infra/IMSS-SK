variable "network_cidr" {
  description = "CIDR block for the network"
  type        = string
  default     = "10.0.0.0/16"
}

variable "vm_size" {
  description = "Size/type of the VM"
  type        = string
  default     = "t2.micro"
}

variable "vm_os" {
  description = "Operating system for the VM"
  type        = string
  default     = "ubuntu-22.04"
}

