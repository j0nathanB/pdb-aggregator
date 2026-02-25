"""
Dead man's switch Lambda - alerts if no brief was published this week.
Triggered Monday 8 AM ET by EventBridge.
"""

import boto3
import json
import logging
import os
from datetime import datetime, timedelta

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")
dynamodb = boto3.client("dynamodb")
ses = boto3.client("ses")

ARTIFACTS_BUCKET = os.environ["ARTIFACTS_BUCKET"]
EVENTS_TABLE = os.environ["EVENTS_TABLE"]
ALERT_EMAIL = os.environ["ALERT_EMAIL"]
SES_FROM_EMAIL = os.environ["SES_FROM_EMAIL"]


def handler(event, context):
    """Check if this week's brief was published and sent."""
    logger.info("Dead man's switch triggered")

    # Calculate expected brief date (previous Saturday)
    today = datetime.utcnow()
    days_since_saturday = (today.weekday() + 2) % 7
    last_saturday = today - timedelta(days=days_since_saturday)
    brief_id = last_saturday.strftime("%Y-%m-%d")

    logger.info(f"Checking for brief: {brief_id}")

    # Check 1: Do artifacts exist in S3?
    artifacts_exist = check_artifacts_exist(brief_id)

    # Check 2: Were emails sent?
    emails_sent = check_emails_sent(brief_id) if artifacts_exist else False

    # Determine alert status
    if not artifacts_exist:
        send_alert(
            subject="ALERT: IDEAL Brief pipeline failed",
            body=f"""
No brief artifacts found for {brief_id}.

The pipeline may have failed. Check:
1. ECS task logs in CloudWatch
2. GitHub Actions workflow status
3. S3 bucket: {ARTIFACTS_BUCKET}/briefs/{brief_id}/

This is an automated alert from the dead man's switch.
            """.strip()
        )
        return {"status": "alert_sent", "reason": "no_artifacts", "brief_id": brief_id}

    elif not emails_sent:
        send_alert(
            subject="ALERT: IDEAL Brief email not sent",
            body=f"""
Brief {brief_id} was generated but email distribution didn't happen.

Check:
1. API Gateway logs for webhook failures
2. Lambda logs for email-sender function
3. GitHub Actions deploy workflow

Artifacts exist at: s3://{ARTIFACTS_BUCKET}/briefs/{brief_id}/

Manual recovery:
aws lambda invoke --function-name ideal-brief-prod-email-sender \\
  --payload '{{"body": "{{\\"brief_date\\": \\"{brief_id}\\", \\"deployed_url\\": \\"https://idealbrief.org/briefs/{brief_id}/\\"}}"}}' \\
  /dev/stdout

This is an automated alert from the dead man's switch.
            """.strip()
        )
        return {"status": "alert_sent", "reason": "no_emails", "brief_id": brief_id}

    else:
        logger.info(f"Brief {brief_id} was published and sent successfully")
        return {"status": "ok", "brief_id": brief_id}


def check_artifacts_exist(brief_id: str) -> bool:
    """Check if brief artifacts exist in S3."""
    try:
        s3.head_object(Bucket=ARTIFACTS_BUCKET, Key=f"briefs/{brief_id}/meta.json")
        return True
    except s3.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False
        raise


def check_emails_sent(brief_id: str) -> bool:
    """Check if emails were sent for this brief."""
    try:
        response = dynamodb.query(
            TableName=EVENTS_TABLE,
            IndexName="brief-index",
            KeyConditionExpression="brief_id = :bid",
            FilterExpression="event_type = :send",
            ExpressionAttributeValues={
                ":bid": {"S": brief_id},
                ":send": {"S": "send"},
            },
            Limit=1,
        )
        return len(response.get("Items", [])) > 0
    except Exception as e:
        logger.error(f"Error checking emails: {e}")
        return False


def send_alert(subject: str, body: str):
    """Send alert email."""
    logger.warning(f"Sending alert: {subject}")

    try:
        ses.send_email(
            Source=SES_FROM_EMAIL,
            Destination={"ToAddresses": [ALERT_EMAIL]},
            Message={
                "Subject": {"Data": subject, "Charset": "UTF-8"},
                "Body": {"Text": {"Data": body, "Charset": "UTF-8"}},
            },
        )
        logger.info(f"Alert sent to {ALERT_EMAIL}")
    except Exception as e:
        logger.error(f"Failed to send alert: {e}")
        raise
