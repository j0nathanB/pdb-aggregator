# SES Configuration for email sending

resource "aws_ses_configuration_set" "main" {
  name = "${local.name_prefix}-config"

  reputation_metrics_enabled = true
  sending_enabled            = true

  delivery_options {
    tls_policy = "Require"
  }
}

# SNS topic for SES events (bounces, complaints, deliveries)
resource "aws_sns_topic" "ses_events" {
  name = "${local.name_prefix}-ses-events"

  tags = {
    Name = "${local.name_prefix}-ses-events"
  }
}

# SES event destination - send bounce/complaint to SNS
resource "aws_ses_event_destination" "sns" {
  name                   = "sns-events"
  configuration_set_name = aws_ses_configuration_set.main.name
  enabled                = true

  matching_types = [
    "bounce",
    "complaint",
    "delivery",
    "send",
  ]

  sns_destination {
    topic_arn = aws_sns_topic.ses_events.arn
  }
}

# Note: Email identity verification must be done manually or via CLI
# For production, you'll want to verify a domain instead of individual emails
#
# To verify an email address:
#   aws ses verify-email-identity --email-address brief@idealbrief.org
#
# To verify a domain (recommended for production):
#   aws ses verify-domain-identity --domain idealbrief.org
#   Then add the TXT record to your DNS
