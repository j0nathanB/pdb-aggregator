# Secrets Manager for API keys and credentials

resource "aws_secretsmanager_secret" "github_token" {
  name        = "${local.name_prefix}-github-token"
  description = "GitHub token for PR creation"

  tags = {
    Name = "${local.name_prefix}-github-token"
  }
}

# Note: GitHub token value should be set manually in AWS Console
# or via: aws secretsmanager put-secret-value --secret-id ideal-brief-prod-github-token --secret-string '{"token":"ghp_xxx"}'

resource "aws_secretsmanager_secret" "anthropic_api_key" {
  name        = "${local.name_prefix}-anthropic-api-key"
  description = "Anthropic API key for the pipeline"

  tags = {
    Name = "${local.name_prefix}-anthropic-api-key"
  }
}

# Note: Set the value manually:
# aws secretsmanager put-secret-value --secret-id ideal-brief-prod-anthropic-api-key --secret-string 'sk-ant-xxx'

resource "aws_secretsmanager_secret" "searchapi_key" {
  name        = "${local.name_prefix}-searchapi-key"
  description = "SearchAPI key for news fetching"

  tags = {
    Name = "${local.name_prefix}-searchapi-key"
  }
}

# Note: Set the value manually:
# aws secretsmanager put-secret-value --secret-id ideal-brief-prod-searchapi-key --secret-string 'xxx'

resource "aws_secretsmanager_secret" "diffbot_token" {
  name        = "${local.name_prefix}-diffbot-token"
  description = "Diffbot API token for full article extraction"

  tags = {
    Name = "${local.name_prefix}-diffbot-token"
  }
}
