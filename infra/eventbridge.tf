# EventBridge Scheduler rules for pipeline execution and monitoring

# -----------------------------------------------------------------------------
# Schedule: Generate Brief (Sunday 11 PM ET = Monday 04:00 UTC)
# -----------------------------------------------------------------------------

resource "aws_scheduler_schedule" "generate_brief" {
  name       = "${local.name_prefix}-generate-brief"
  group_name = "default"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression          = "cron(0 4 ? * MON *)"
  schedule_expression_timezone = "UTC"

  target {
    arn      = aws_ecs_cluster.main.arn
    role_arn = aws_iam_role.scheduler.arn

    ecs_parameters {
      task_definition_arn = aws_ecs_task_definition.pipeline.arn
      launch_type         = "FARGATE"
      task_count          = 1

      network_configuration {
        subnets          = [aws_subnet.public.id]
        assign_public_ip = true
        security_groups  = [aws_security_group.fargate_task.id]
      }
    }

    retry_policy {
      maximum_retry_attempts       = 2
      maximum_event_age_in_seconds = 3600 # 1 hour
    }
  }

  state = var.enable_schedules ? "ENABLED" : "DISABLED"
}

# -----------------------------------------------------------------------------
# Schedule: Dead Man's Switch (Monday 8 AM ET = Monday 13:00 UTC)
# -----------------------------------------------------------------------------

resource "aws_scheduler_schedule" "dead_mans_switch" {
  name       = "${local.name_prefix}-dead-mans-switch"
  group_name = "default"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression          = "cron(0 13 ? * MON *)"
  schedule_expression_timezone = "UTC"

  target {
    arn      = aws_lambda_function.dead_mans_switch.arn
    role_arn = aws_iam_role.scheduler.arn

    retry_policy {
      maximum_retry_attempts       = 2
      maximum_event_age_in_seconds = 3600
    }
  }

  state = var.enable_schedules ? "ENABLED" : "DISABLED"
}
