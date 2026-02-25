# API Gateway for webhook endpoints
# Requires API key for security

resource "aws_apigatewayv2_api" "main" {
  name          = "${local.name_prefix}-api"
  protocol_type = "HTTP"

  cors_configuration {
    allow_origins = ["*"]
    allow_methods = ["POST", "GET"]
    allow_headers = ["Content-Type", "x-api-key"]
  }

  tags = {
    Name = "${local.name_prefix}-api"
  }
}

resource "aws_apigatewayv2_stage" "prod" {
  api_id      = aws_apigatewayv2_api.main.id
  name        = "prod"
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gateway.arn
    format = jsonencode({
      requestId      = "$context.requestId"
      ip             = "$context.identity.sourceIp"
      requestTime    = "$context.requestTime"
      httpMethod     = "$context.httpMethod"
      routeKey       = "$context.routeKey"
      status         = "$context.status"
      responseLength = "$context.responseLength"
      errorMessage   = "$context.error.message"
    })
  }

  tags = {
    Name = "${local.name_prefix}-api-prod"
  }
}

resource "aws_cloudwatch_log_group" "api_gateway" {
  name              = "/aws/apigateway/${local.name_prefix}"
  retention_in_days = 14

  tags = {
    Name = "${local.name_prefix}-api-logs"
  }
}

# Lambda authorizer for API key validation
resource "aws_apigatewayv2_authorizer" "api_key" {
  api_id                            = aws_apigatewayv2_api.main.id
  authorizer_type                   = "REQUEST"
  authorizer_uri                    = aws_lambda_function.authorizer.invoke_arn
  identity_sources                  = ["$request.header.x-api-key"]
  name                              = "api-key-authorizer"
  authorizer_payload_format_version = "2.0"
  enable_simple_responses           = true
}

# Routes
resource "aws_apigatewayv2_route" "send_email" {
  api_id             = aws_apigatewayv2_api.main.id
  route_key          = "POST /send"
  target             = "integrations/${aws_apigatewayv2_integration.email_sender.id}"
  authorization_type = "CUSTOM"
  authorizer_id      = aws_apigatewayv2_authorizer.api_key.id
}

resource "aws_apigatewayv2_route" "unsubscribe" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "GET /unsubscribe"
  target    = "integrations/${aws_apigatewayv2_integration.unsubscribe.id}"
  # No auth - public endpoint with token in query param
}

resource "aws_apigatewayv2_route" "unsubscribe_confirm" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "POST /unsubscribe/confirm"
  target    = "integrations/${aws_apigatewayv2_integration.unsubscribe.id}"
}

# Integrations
resource "aws_apigatewayv2_integration" "email_sender" {
  api_id                 = aws_apigatewayv2_api.main.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.email_sender.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_integration" "unsubscribe" {
  api_id                 = aws_apigatewayv2_api.main.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.unsubscribe.invoke_arn
  payload_format_version = "2.0"
}

# Lambda permissions for API Gateway
resource "aws_lambda_permission" "api_email_sender" {
  statement_id  = "AllowAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.email_sender.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

resource "aws_lambda_permission" "api_unsubscribe" {
  statement_id  = "AllowAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.unsubscribe.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

resource "aws_lambda_permission" "api_authorizer" {
  statement_id  = "AllowAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.authorizer.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}
