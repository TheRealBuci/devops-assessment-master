output "namespace" {
  description = "The Kubernetes namespace created for the homework app."
  value       = kubernetes_namespace_v1.homework.metadata[0].name
}

output "release_name" {
  description = "The Helm release name deployed by Terraform."
  value       = helm_release.homework.name
}

output "release_namespace" {
  description = "The namespace where the Helm release is deployed."
  value       = helm_release.homework.namespace
}

output "image_tag" {
  description = "The image tag currently configured for the Helm release."
  value       = var.image_tag
}

output "environment" {
  description = "The runtime environment passed to the application."
  value       = var.environment
}
