# EventBridge Scheduler rule for pipeline execution

# -----------------------------------------------------------------------------
# Schedule: Generate Brief (Sunday 9 PM Eastern, DST-aware)
#
# Pipeline takes ~1.5-2 hours to execute, so a 9 PM kickoff finishes around
# 10:30-11 PM Eastern, leaving the user time for manual review before sleep.
# Using America/New_York timezone (instead of fixed UTC offset) so the
# schedule stays at 9 PM Eastern across DST transitions.
# -----------------------------------------------------------------------------

resource "aws_scheduler_schedule" "generate_brief" {
  name       = "${local.name_prefix}-generate-brief"
  group_name = "default"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression          = "cron(0 21 ? * SUN *)"
  schedule_expression_timezone = "America/New_York"

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
