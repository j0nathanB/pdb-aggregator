"""
Email sender Lambda - sends digest emails to subscribers.
Triggered by API Gateway webhook from GitHub Actions.
"""

import boto3
import json
import logging
import os
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.client("dynamodb")
ses = boto3.client("ses")
s3 = boto3.client("s3")

SUBSCRIBERS_TABLE = os.environ["SUBSCRIBERS_TABLE"]
EVENTS_TABLE = os.environ["EVENTS_TABLE"]
ARTIFACTS_BUCKET = os.environ["ARTIFACTS_BUCKET"]
SES_FROM_EMAIL = os.environ["SES_FROM_EMAIL"]
SES_CONFIG_SET = os.environ["SES_CONFIG_SET"]
UNSUBSCRIBE_BASE_URL = os.environ["UNSUBSCRIBE_BASE_URL"]


def find_latest_brief():
    """Find the most recent brief_date in S3 by listing prefixes."""
    result = s3.list_objects_v2(
        Bucket=ARTIFACTS_BUCKET,
        Prefix="briefs/",
        Delimiter="/",
    )
    prefixes = [
        p["Prefix"].rstrip("/").split("/")[-1]
        for p in result.get("CommonPrefixes", [])
    ]
    if not prefixes:
        return None
    # Sort descending — dates are YYYY-MM-DD, lexicographic order works
    prefixes.sort(reverse=True)
    return prefixes[0]


def handler(event, context):
    """
    Webhook trigger for email distribution.

    Accepts optional {"brief_date": "2026-02-08"} in body.
    If brief_date is omitted, auto-discovers the latest brief in S3.
    """
    logger.info(f"Received event: {json.dumps(event)}")

    try:
        body = json.loads(event.get("body", "{}"))
    except json.JSONDecodeError:
        body = {}

    brief_id = body.get("brief_date")

    # Auto-discover latest brief if not specified
    if not brief_id:
        brief_id = find_latest_brief()
        if not brief_id:
            return response(404, {"error": "No briefs found in S3"})
        logger.info(f"Auto-discovered latest brief: {brief_id}")

    logger.info(f"Processing email distribution for brief: {brief_id}")

    # 1. Verify artifacts exist in S3
    try:
        s3.head_object(Bucket=ARTIFACTS_BUCKET, Key=f"briefs/{brief_id}/email.html")
    except s3.exceptions.ClientError:
        return response(404, {"error": f"email.html not found for {brief_id}"})

    # 2. Load email HTML from S3
    html_obj = s3.get_object(Bucket=ARTIFACTS_BUCKET, Key=f"briefs/{brief_id}/email.html")
    html_body = html_obj["Body"].read().decode("utf-8")

    # 3. Load subject from meta.json if exists
    subject = f"The Middle Powers Monitor: Week of {brief_id}"
    try:
        meta_obj = s3.get_object(Bucket=ARTIFACTS_BUCKET, Key=f"briefs/{brief_id}/meta.json")
        meta = json.loads(meta_obj["Body"].read().decode("utf-8"))
        if "subject" in meta:
            subject = meta["subject"]
    except Exception:
        pass  # Use default subject

    # 4. Fetch active subscribers
    subscribers = get_active_subscribers()
    logger.info(f"Found {len(subscribers)} active subscribers")

    # 5. Send with idempotency
    sent_count = 0
    skip_count = 0
    errors = []

    for subscriber in subscribers:
        email = subscriber["email"]
        token = subscriber.get("unsubscribe_token", "")

        # Personalize unsubscribe link
        unsubscribe_url = f"{UNSUBSCRIBE_BASE_URL.rstrip('/')}/unsubscribe?token={token}"
        personalized_html = html_body.replace("{{unsubscribe_url}}", unsubscribe_url)

        result = send_to_subscriber(email, brief_id, subject, personalized_html)
        if result == "sent":
            sent_count += 1
        elif result == "skipped":
            skip_count += 1
        else:
            errors.append({"email": email, "error": result})

    logger.info(f"Distribution complete: {sent_count} sent, {skip_count} skipped")
    if errors:
        logger.warning(f"Errors: {errors}")

    return response(200, {
        "brief_id": brief_id,
        "sent": sent_count,
        "skipped": skip_count,
        "errors": len(errors),
    })


def get_active_subscribers():
    """Query DynamoDB for active subscribers."""
    subscribers = []

    response = dynamodb.query(
        TableName=SUBSCRIBERS_TABLE,
        IndexName="status-index",
        KeyConditionExpression="#s = :active",
        ExpressionAttributeNames={"#s": "status"},
        ExpressionAttributeValues={":active": {"S": "active"}},
    )

    for item in response.get("Items", []):
        subscribers.append({
            "email": item["email"]["S"],
            "unsubscribe_token": item.get("unsubscribe_token", {}).get("S", ""),
        })

    # Handle pagination
    while "LastEvaluatedKey" in response:
        response = dynamodb.query(
            TableName=SUBSCRIBERS_TABLE,
            IndexName="status-index",
            KeyConditionExpression="#s = :active",
            ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={":active": {"S": "active"}},
            ExclusiveStartKey=response["LastEvaluatedKey"],
        )
        for item in response.get("Items", []):
            subscribers.append({
                "email": item["email"]["S"],
                "unsubscribe_token": item.get("unsubscribe_token", {}).get("S", ""),
            })

    return subscribers


def send_to_subscriber(email: str, brief_id: str, subject: str, html_body: str) -> str:
    """Send with idempotency check. Returns 'sent', 'skipped', or error message."""
    now = datetime.utcnow().isoformat()

    # Conditional update: only proceed if last_sent_brief_id != this brief
    try:
        dynamodb.update_item(
            TableName=SUBSCRIBERS_TABLE,
            Key={"email": {"S": email}},
            UpdateExpression="SET last_sent_brief_id = :brief_id, updated_at = :now",
            ConditionExpression="attribute_not_exists(last_sent_brief_id) OR last_sent_brief_id <> :brief_id",
            ExpressionAttributeValues={
                ":brief_id": {"S": brief_id},
                ":now": {"S": now},
            },
        )
    except dynamodb.exceptions.ConditionalCheckFailedException:
        logger.info(f"Skipping {email}: already sent {brief_id}")
        return "skipped"
    except Exception as e:
        logger.error(f"DynamoDB error for {email}: {e}")
        return str(e)

    # Send the email
    try:
        ses.send_email(
            Source=SES_FROM_EMAIL,
            Destination={"ToAddresses": [email]},
            Message={
                "Subject": {"Data": subject, "Charset": "UTF-8"},
                "Body": {"Html": {"Data": html_body, "Charset": "UTF-8"}},
            },
            ConfigurationSetName=SES_CONFIG_SET,
            Tags=[
                {"Name": "brief_id", "Value": brief_id},
            ],
        )

        # Record send event
        dynamodb.put_item(
            TableName=EVENTS_TABLE,
            Item={
                "email": {"S": email},
                "event_timestamp": {"S": now},
                "event_type": {"S": "send"},
                "brief_id": {"S": brief_id},
                "ttl": {"N": str(int(datetime.utcnow().timestamp()) + 90 * 24 * 3600)},
            },
        )

        return "sent"
    except Exception as e:
        logger.error(f"SES error for {email}: {e}")
        return str(e)


def response(status_code: int, body: dict) -> dict:
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }
