# Lambda functions for email distribution

locals {
  lambda_runtime = "python3.12"
  lambda_handler = "handler.handler"
}

# -----------------------------------------------------------------------------
# Email Sender Lambda
# -----------------------------------------------------------------------------

resource "aws_lambda_function" "email_sender" {
  function_name = "${local.name_prefix}-email-sender"
  role          = aws_iam_role.lambda_execution.arn
  handler       = local.lambda_handler
  runtime       = local.lambda_runtime
  timeout       = 300 # 5 minutes for batch sending
  memory_size   = 256

  filename         = data.archive_file.email_sender.output_path
  source_code_hash = data.archive_file.email_sender.output_base64sha256

  environment {
    variables = {
      SUBSCRIBERS_TABLE    = aws_dynamodb_table.subscribers.name
      EVENTS_TABLE         = aws_dynamodb_table.email_events.name
      ARTIFACTS_BUCKET     = aws_s3_bucket.artifacts.id
      SES_FROM_EMAIL       = var.ses_from_email
      SES_CONFIG_SET       = aws_ses_configuration_set.main.name
      UNSUBSCRIBE_BASE_URL = aws_apigatewayv2_stage.prod.invoke_url
    }
  }

  tags = {
    Name = "${local.name_prefix}-email-sender"
  }
}

data "archive_file" "email_sender" {
  type        = "zip"
  source_dir  = "${path.module}/lambda/email_sender"
  output_path = "${path.module}/.build/email_sender.zip"
}

# -----------------------------------------------------------------------------
# Unsubscribe Handler Lambda
# -----------------------------------------------------------------------------

resource "aws_lambda_function" "unsubscribe" {
  function_name = "${local.name_prefix}-unsubscribe"
  role          = aws_iam_role.lambda_execution.arn
  handler       = local.lambda_handler
  runtime       = local.lambda_runtime
  timeout       = 10
  memory_size   = 128

  filename         = data.archive_file.unsubscribe.output_path
  source_code_hash = data.archive_file.unsubscribe.output_base64sha256

  environment {
    variables = {
      SUBSCRIBERS_TABLE = aws_dynamodb_table.subscribers.name
    }
  }

  tags = {
    Name = "${local.name_prefix}-unsubscribe"
  }
}

data "archive_file" "unsubscribe" {
  type        = "zip"
  source_dir  = "${path.module}/lambda/unsubscribe"
  output_path = "${path.module}/.build/unsubscribe.zip"
}

# -----------------------------------------------------------------------------
# SES Event Handler Lambda (bounces, complaints)
# -----------------------------------------------------------------------------

resource "aws_lambda_function" "ses_events" {
  function_name = "${local.name_prefix}-ses-events"
  role          = aws_iam_role.lambda_execution.arn
  handler       = local.lambda_handler
  runtime       = local.lambda_runtime
  timeout       = 30
  memory_size   = 128

  filename         = data.archive_file.ses_events.output_path
  source_code_hash = data.archive_file.ses_events.output_base64sha256

  environment {
    variables = {
      SUBSCRIBERS_TABLE = aws_dynamodb_table.subscribers.name
      EVENTS_TABLE      = aws_dynamodb_table.email_events.name
    }
  }

  tags = {
    Name = "${local.name_prefix}-ses-events"
  }
}

data "archive_file" "ses_events" {
  type        = "zip"
  source_dir  = "${path.module}/lambda/ses_events"
  output_path = "${path.module}/.build/ses_events.zip"
}

# SNS trigger for SES events
resource "aws_lambda_permission" "ses_events_sns" {
  statement_id  = "AllowSNS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ses_events.function_name
  principal     = "sns.amazonaws.com"
  source_arn    = aws_sns_topic.ses_events.arn
}

resource "aws_sns_topic_subscription" "ses_events_lambda" {
  topic_arn = aws_sns_topic.ses_events.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.ses_events.arn
}

# -----------------------------------------------------------------------------
# API Key Authorizer Lambda
# -----------------------------------------------------------------------------

resource "aws_lambda_function" "authorizer" {
  function_name = "${local.name_prefix}-authorizer"
  role          = aws_iam_role.lambda_authorizer.arn
  handler       = local.lambda_handler
  runtime       = local.lambda_runtime
  timeout       = 5
  memory_size   = 128

  filename         = data.archive_file.authorizer.output_path
  source_code_hash = data.archive_file.authorizer.output_base64sha256

  environment {
    variables = {
      API_KEY_SECRET_ARN = aws_secretsmanager_secret.api_key.arn
    }
  }

  tags = {
    Name = "${local.name_prefix}-authorizer"
  }
}

data "archive_file" "authorizer" {
  type        = "zip"
  source_dir  = "${path.module}/lambda/authorizer"
  output_path = "${path.module}/.build/authorizer.zip"
}

# Authorizer needs its own role with Secrets Manager access
resource "aws_iam_role" "lambda_authorizer" {
  name = "${local.name_prefix}-lambda-authorizer"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "authorizer_basic" {
  role       = aws_iam_role.lambda_authorizer.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "authorizer_secrets" {
  name = "secrets-access"
  role = aws_iam_role.lambda_authorizer.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "secretsmanager:GetSecretValue"
      ]
      Resource = aws_secretsmanager_secret.api_key.arn
    }]
  })
}

# -----------------------------------------------------------------------------
# Dead Man's Switch Lambda
# -----------------------------------------------------------------------------

resource "aws_lambda_function" "dead_mans_switch" {
  function_name = "${local.name_prefix}-dead-mans-switch"
  role          = aws_iam_role.lambda_execution.arn
  handler       = local.lambda_handler
  runtime       = local.lambda_runtime
  timeout       = 30
  memory_size   = 128

  filename         = data.archive_file.dead_mans_switch.output_path
  source_code_hash = data.archive_file.dead_mans_switch.output_base64sha256

  environment {
    variables = {
      ARTIFACTS_BUCKET = aws_s3_bucket.artifacts.id
      EVENTS_TABLE     = aws_dynamodb_table.email_events.name
      ALERT_EMAIL      = var.alert_email
      SES_FROM_EMAIL   = var.ses_from_email
    }
  }

  tags = {
    Name = "${local.name_prefix}-dead-mans-switch"
  }
}

data "archive_file" "dead_mans_switch" {
  type        = "zip"
  source_dir  = "${path.module}/lambda/dead_mans_switch"
  output_path = "${path.module}/.build/dead_mans_switch.zip"
}
