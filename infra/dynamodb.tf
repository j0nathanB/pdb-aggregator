# Subscribers table
# Partition key: email
# GSI on status for querying active subscribers
resource "aws_dynamodb_table" "subscribers" {
  name         = "${local.name_prefix}-subscribers"
  billing_mode = "PAY_PER_REQUEST" # On-demand pricing, ~$0.25/mo at low scale

  hash_key = "email"

  attribute {
    name = "email"
    type = "S"
  }

  attribute {
    name = "status"
    type = "S"
  }

  # GSI for querying by status (active, unsubscribed, bounced, complained)
  global_secondary_index {
    name            = "status-index"
    hash_key        = "status"
    projection_type = "ALL"
  }

  point_in_time_recovery {
    enabled = true
  }

  tags = {
    Name = "${local.name_prefix}-subscribers"
  }
}

# Email events table for tracking opens, clicks, bounces
# Partition key: email, Sort key: event_timestamp
# TTL: 90 days auto-expire
resource "aws_dynamodb_table" "email_events" {
  name         = "${local.name_prefix}-email-events"
  billing_mode = "PAY_PER_REQUEST"

  hash_key  = "email"
  range_key = "event_timestamp"

  attribute {
    name = "email"
    type = "S"
  }

  attribute {
    name = "event_timestamp"
    type = "S"
  }

  attribute {
    name = "brief_id"
    type = "S"
  }

  # GSI for querying events by brief
  global_secondary_index {
    name            = "brief-index"
    hash_key        = "brief_id"
    range_key       = "event_timestamp"
    projection_type = "ALL"
  }

  ttl {
    attribute_name = "ttl"
    enabled        = true
  }

  tags = {
    Name = "${local.name_prefix}-email-events"
  }
}
