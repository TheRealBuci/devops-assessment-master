variable "namespace" {
  description = "Namespace for the homework application."
  type        = string
  default     = "homework"
}

variable "environment" {
  description = "Runtime environment value passed to the application."
  type        = string
  default     = "dev"
}

variable "image_tag" {
  description = "Docker image tag to deploy through the Helm release."
  type        = string
  default     = "latest"
}