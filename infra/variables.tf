variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name (prod, staging)"
  type        = string
  default     = "prod"
}

variable "artifacts_bucket_name" {
  description = "S3 bucket name for brief artifacts"
  type        = string
  default     = "ideal-brief-artifacts"
}

# VPC CIDR - small range sufficient for this workload
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/24"
}

variable "public_subnet_cidr" {
  description = "CIDR block for public subnet"
  type        = string
  default     = "10.0.0.0/26"
}

variable "availability_zone" {
  description = "Availability zone for subnet"
  type        = string
  default     = "us-east-1a"
}

# Email settings
variable "ses_from_email" {
  description = "Email address to send from (must be verified in SES)"
  type        = string
  default     = "brief@idealbrief.org"
}

variable "alert_email" {
  description = "Email address for dead man's switch alerts"
  type        = string
}

# ECS Pipeline settings
variable "pipeline_cpu" {
  description = "CPU units for pipeline Fargate task (1024 = 1 vCPU)"
  type        = number
  default     = 2048 # 2 vCPU - needed for sentence-transformers models
}

variable "pipeline_memory" {
  description = "Memory (MB) for pipeline Fargate task"
  type        = number
  default     = 4096 # 4 GB
}

variable "pipeline_image_tag" {
  description = "Docker image tag for the pipeline container"
  type        = string
  default     = "latest"
}

variable "content_repo" {
  description = "GitHub repo for brief content (owner/repo format)"
  type        = string
  default     = ""
}

variable "enable_schedules" {
  description = "Whether to enable EventBridge schedules (set false for initial deploy)"
  type        = bool
  default     = false
}

# Security
variable "webhook_api_key" {
  description = "API key for webhook authentication (generate with: openssl rand -hex 32)"
  type        = string
  sensitive   = true
}
