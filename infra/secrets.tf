# Secrets Manager for API keys and credentials.
#
# Each secret here is a CONTAINER. Terraform creates the empty container;
# you must populate the value manually after `terraform apply`:
#
#   aws secretsmanager put-secret-value \
#     --secret-id ideal-brief-prod-{name} \
#     --secret-string '...'
#
# The Fargate task definition (see ecs.tf) wires each container into the
# pipeline container as an environment variable via `valueFrom`.

# -----------------------------------------------------------------------------
# GitHub: write access to push briefs to main
# -----------------------------------------------------------------------------
resource "aws_secretsmanager_secret" "github_token" {
  name        = "${local.name_prefix}-github-token"
  description = "GitHub token for pushing briefs to main"

  tags = {
    Name = "${local.name_prefix}-github-token"
  }
}

# -----------------------------------------------------------------------------
# Anthropic: every LLM call in the pipeline
# -----------------------------------------------------------------------------
resource "aws_secretsmanager_secret" "anthropic_api_key" {
  name        = "${local.name_prefix}-anthropic-api-key"
  description = "Anthropic API key for all LLM calls"

  tags = {
    Name = "${local.name_prefix}-anthropic-api-key"
  }
}

# -----------------------------------------------------------------------------
# Brave: news search (essential — used by triage, expansion, story map)
# -----------------------------------------------------------------------------
resource "aws_secretsmanager_secret" "brave_api_key" {
  name        = "${local.name_prefix}-brave-api-key"
  description = "Brave Search API key for news discovery"

  tags = {
    Name = "${local.name_prefix}-brave-api-key"
  }
}

# -----------------------------------------------------------------------------
# SearchAPI: Google search for government source discovery
# -----------------------------------------------------------------------------
resource "aws_secretsmanager_secret" "searchapi_key" {
  name        = "${local.name_prefix}-searchapi-key"
  description = "SearchAPI (Google) key for government source discovery"

  tags = {
    Name = "${local.name_prefix}-searchapi-key"
  }
}

# -----------------------------------------------------------------------------
# Diffbot: article extraction (one of the fallback chain entries)
# -----------------------------------------------------------------------------
resource "aws_secretsmanager_secret" "diffbot_token" {
  name        = "${local.name_prefix}-diffbot-token"
  description = "Diffbot API token for article extraction"

  tags = {
    Name = "${local.name_prefix}-diffbot-token"
  }
}

# -----------------------------------------------------------------------------
# Browserbase: cloud browser for sites that need JS rendering / bot bypass
# -----------------------------------------------------------------------------
resource "aws_secretsmanager_secret" "browserbase_api_key" {
  name        = "${local.name_prefix}-browserbase-api-key"
  description = "Browserbase API key for cloud browser extraction"

  tags = {
    Name = "${local.name_prefix}-browserbase-api-key"
  }
}

resource "aws_secretsmanager_secret" "browserbase_project_id" {
  name        = "${local.name_prefix}-browserbase-project-id"
  description = "Browserbase project ID (paired with the API key)"

  tags = {
    Name = "${local.name_prefix}-browserbase-project-id"
  }
}

# -----------------------------------------------------------------------------
# Guardian: Guardian-specific extractor (used when extracting Guardian articles)
# -----------------------------------------------------------------------------
resource "aws_secretsmanager_secret" "guardian_api_key" {
  name        = "${local.name_prefix}-guardian-api-key"
  description = "The Guardian API key for the Guardian-specific extractor"

  tags = {
    Name = "${local.name_prefix}-guardian-api-key"
  }
}
