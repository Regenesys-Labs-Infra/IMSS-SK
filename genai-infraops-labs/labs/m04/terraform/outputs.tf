output "network_config" {
  description = "Network configuration"
  value       = local.network
}

output "vm_config" {
  description = "VM configuration"
  value       = local.vm
}

output "security_group_config" {
  description = "Security group configuration"
  value       = local.security_group
}

output "infrastructure_model_file" {
  description = "Path to the generated infrastructure model JSON file"
  value       = local_file.infrastructure_model.filename
}

output "infrastructure_model" {
  description = "Complete infrastructure model"
  value       = local.infrastructure_model
}
