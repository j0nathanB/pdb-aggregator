"""
Unsubscribe handler Lambda - two-step unsubscribe to prevent forwarding attacks.
"""

import boto3
import json
import logging
import os
import urllib.parse
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.client("dynamodb")
SUBSCRIBERS_TABLE = os.environ["SUBSCRIBERS_TABLE"]


def handler(event, context):
    """Handle GET /unsubscribe and POST /unsubscribe/confirm"""
    logger.info(f"Received event: {json.dumps(event)}")

    method = event.get("requestContext", {}).get("http", {}).get("method", "GET")
    path = event.get("rawPath", "")

    if method == "GET" and "/unsubscribe" in path:
        return show_confirmation_page(event)
    elif method == "POST" and "/confirm" in path:
        return confirm_unsubscribe(event)
    else:
        return html_response(404, "<h1>Not Found</h1>")


def show_confirmation_page(event):
    """Show confirmation page with subscriber email."""
    params = event.get("queryStringParameters", {}) or {}
    token = params.get("token", "")

    if not token:
        return html_response(400, "<h1>Missing token</h1>")

    subscriber = get_subscriber_by_token(token)
    if not subscriber:
        return html_response(404, """
            <h1>Invalid or expired link</h1>
            <p>This unsubscribe link is no longer valid.</p>
        """)

    email = subscriber["email"]
    # Mask email for privacy: j***@example.com
    masked = email[0] + "***@" + email.split("@")[1] if "@" in email else email

    return html_response(200, f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Unsubscribe - IDEAL Brief</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 500px; margin: 50px auto; padding: 20px; }}
                h1 {{ color: #333; }}
                .email {{ font-weight: bold; color: #0066cc; }}
                button {{ background: #dc3545; color: white; border: none; padding: 12px 24px; font-size: 16px; cursor: pointer; border-radius: 4px; }}
                button:hover {{ background: #c82333; }}
                .note {{ color: #666; font-size: 14px; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <h1>Unsubscribe from IDEAL Brief</h1>
            <p>You are unsubscribing: <span class="email">{masked}</span></p>
            <form method="POST" action="/prod/unsubscribe/confirm">
                <input type="hidden" name="token" value="{token}">
                <button type="submit">Confirm Unsubscribe</button>
            </form>
            <p class="note">Not your email? Someone may have forwarded our newsletter to you. Just close this page.</p>
        </body>
        </html>
    """)


def confirm_unsubscribe(event):
    """Process the unsubscribe confirmation."""
    body = event.get("body", "")

    # Handle base64 encoded body
    if event.get("isBase64Encoded"):
        import base64
        body = base64.b64decode(body).decode("utf-8")

    # Parse form data
    params = urllib.parse.parse_qs(body)
    token = params.get("token", [""])[0]

    if not token:
        return html_response(400, "<h1>Missing token</h1>")

    subscriber = get_subscriber_by_token(token)
    if not subscriber:
        return html_response(404, "<h1>Invalid or expired link</h1>")

    # Update status to unsubscribed
    try:
        dynamodb.update_item(
            TableName=SUBSCRIBERS_TABLE,
            Key={"email": {"S": subscriber["email"]}},
            UpdateExpression="SET #s = :status, updated_at = :now, unsubscribed_at = :now",
            ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={
                ":status": {"S": "unsubscribed"},
                ":now": {"S": datetime.utcnow().isoformat()},
            },
        )
        logger.info(f"Unsubscribed: {subscriber['email']}")
    except Exception as e:
        logger.error(f"Error unsubscribing: {e}")
        return html_response(500, "<h1>Error processing request</h1>")

    return html_response(200, """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Unsubscribed - IDEAL Brief</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 500px; margin: 50px auto; padding: 20px; }
                h1 { color: #28a745; }
            </style>
        </head>
        <body>
            <h1>You've been unsubscribed</h1>
            <p>You will no longer receive IDEAL Brief emails.</p>
            <p>Changed your mind? Contact us to resubscribe.</p>
        </body>
        </html>
    """)


def get_subscriber_by_token(token: str) -> dict | None:
    """Look up subscriber by unsubscribe token."""
    # Scan for token (not ideal but token lookups are rare)
    response = dynamodb.scan(
        TableName=SUBSCRIBERS_TABLE,
        FilterExpression="unsubscribe_token = :token",
        ExpressionAttributeValues={":token": {"S": token}},
        Limit=1,
    )

    items = response.get("Items", [])
    if not items:
        return None

    return {
        "email": items[0]["email"]["S"],
        "status": items[0].get("status", {}).get("S", "unknown"),
    }


def html_response(status_code: int, body: str) -> dict:
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "text/html; charset=utf-8"},
        "body": body,
    }
