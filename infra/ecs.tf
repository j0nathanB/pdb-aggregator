# ECS Cluster and Task Definition for the brief generation pipeline

# -----------------------------------------------------------------------------
# ECS Cluster
# -----------------------------------------------------------------------------

resource "aws_ecs_cluster" "main" {
  name = "${local.name_prefix}-cluster"

  setting {
    name  = "containerInsights"
    value = "disabled" # Keep costs low; enable if debugging needed
  }

  tags = {
    Name = "${local.name_prefix}-cluster"
  }
}

# -----------------------------------------------------------------------------
# CloudWatch Log Group for ECS tasks
# -----------------------------------------------------------------------------

resource "aws_cloudwatch_log_group" "ecs_pipeline" {
  name              = "/ecs/${local.name_prefix}-pipeline"
  retention_in_days = 30

  tags = {
    Name = "${local.name_prefix}-pipeline-logs"
  }
}

# -----------------------------------------------------------------------------
# ECS Task Definition
# -----------------------------------------------------------------------------

resource "aws_ecs_task_definition" "pipeline" {
  family                   = "${local.name_prefix}-pipeline"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.pipeline_cpu
  memory                   = var.pipeline_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "ARM64"
  }

  container_definitions = jsonencode([
    {
      name      = "pipeline"
      image     = "${aws_ecr_repository.pipeline.repository_url}:${var.pipeline_image_tag}"
      essential = true

      environment = [
        { name = "ARTIFACTS_BUCKET", value = aws_s3_bucket.artifacts.id },
        { name = "SES_FROM_EMAIL", value = var.ses_from_email },
        { name = "ALERT_EMAIL", value = var.alert_email },
        { name = "ENVIRONMENT", value = var.environment },
        { name = "CONTENT_REPO", value = var.content_repo },
      ]

      secrets = [
        {
          name      = "ANTHROPIC_API_KEY"
          valueFrom = aws_secretsmanager_secret.anthropic_api_key.arn
        },
        {
          name      = "GITHUB_TOKEN"
          valueFrom = aws_secretsmanager_secret.github_token.arn
        },
        {
          name      = "SEARCHAPI_KEY"
          valueFrom = aws_secretsmanager_secret.searchapi_key.arn
        },
        {
          name      = "DIFFBOT_TOKEN"
          valueFrom = aws_secretsmanager_secret.diffbot_token.arn
        },
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.ecs_pipeline.name
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "pipeline"
        }
      }
    }
  ])

  tags = {
    Name = "${local.name_prefix}-pipeline"
  }
}
