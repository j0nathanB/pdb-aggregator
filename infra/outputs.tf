# Outputs for reference

# =============================================================================
# Networking
# =============================================================================

output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "public_subnet_id" {
  description = "Public subnet ID for Fargate tasks"
  value       = aws_subnet.public.id
}

output "fargate_security_group_id" {
  description = "Security group ID for Fargate tasks"
  value       = aws_security_group.fargate_task.id
}

# =============================================================================
# IAM
# =============================================================================

output "ecs_task_execution_role_arn" {
  description = "ECS task execution role ARN"
  value       = aws_iam_role.ecs_task_execution.arn
}

output "ecs_task_role_arn" {
  description = "ECS task role ARN"
  value       = aws_iam_role.ecs_task.arn
}

output "scheduler_role_arn" {
  description = "EventBridge scheduler role ARN"
  value       = aws_iam_role.scheduler.arn
}

# =============================================================================
# ECS + EventBridge
# =============================================================================

output "ecr_repository_url" {
  description = "ECR repository URL for pipeline image"
  value       = aws_ecr_repository.pipeline.repository_url
}

output "ecs_cluster_name" {
  description = "ECS cluster name"
  value       = aws_ecs_cluster.main.name
}

output "ecs_cluster_arn" {
  description = "ECS cluster ARN"
  value       = aws_ecs_cluster.main.arn
}

output "pipeline_task_definition_arn" {
  description = "Pipeline ECS task definition ARN"
  value       = aws_ecs_task_definition.pipeline.arn
}

output "pipeline_log_group" {
  description = "CloudWatch log group for pipeline tasks"
  value       = aws_cloudwatch_log_group.ecs_pipeline.name
}
