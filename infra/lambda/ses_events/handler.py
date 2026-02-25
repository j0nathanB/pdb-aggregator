"""
SES event handler - processes bounces, complaints, and delivery notifications.
Auto-unsubscribes on bounces and complaints.
"""

import boto3
import json
import logging
import os
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.client("dynamodb")
SUBSCRIBERS_TABLE = os.environ["SUBSCRIBERS_TABLE"]
EVENTS_TABLE = os.environ["EVENTS_TABLE"]


def handler(event, context):
    """Process SNS messages from SES."""
    logger.info(f"Received event: {json.dumps(event)}")

    for record in event.get("Records", []):
        try:
            sns_message = json.loads(record["Sns"]["Message"])
            process_ses_event(sns_message)
        except Exception as e:
            logger.error(f"Error processing record: {e}")


def process_ses_event(message: dict):
    """Process a single SES event."""
    event_type = message.get("eventType", message.get("notificationType", ""))
    mail = message.get("mail", {})

    # Get recipient email(s)
    destination = mail.get("destination", [])
    if not destination:
        logger.warning("No destination in message")
        return

    email = destination[0]
    timestamp = mail.get("timestamp", datetime.utcnow().isoformat())
    message_id = mail.get("messageId", "")

    # Extract brief_id from tags if available
    brief_id = ""
    for tag in mail.get("tags", {}).get("brief_id", []):
        brief_id = tag
        break

    logger.info(f"Processing {event_type} for {email}")

    # Record the event
    record_event(email, timestamp, event_type.lower(), brief_id, message_id)

    # Auto-unsubscribe on bounce or complaint
    if event_type in ("Bounce", "bounce"):
        bounce_info = message.get("bounce", {})
        bounce_type = bounce_info.get("bounceType", "")

        # Only auto-unsubscribe on permanent bounces
        if bounce_type == "Permanent":
            auto_unsubscribe(email, "bounced", f"Permanent bounce: {bounce_info.get('bounceSubType', '')}")
        else:
            logger.info(f"Transient bounce for {email}, not unsubscribing")

    elif event_type in ("Complaint", "complaint"):
        complaint_info = message.get("complaint", {})
        complaint_type = complaint_info.get("complaintFeedbackType", "unknown")
        auto_unsubscribe(email, "complained", f"Complaint: {complaint_type}")


def record_event(email: str, timestamp: str, event_type: str, brief_id: str, message_id: str):
    """Record event in DynamoDB."""
    try:
        item = {
            "email": {"S": email},
            "event_timestamp": {"S": timestamp},
            "event_type": {"S": event_type},
            "ttl": {"N": str(int(datetime.utcnow().timestamp()) + 90 * 24 * 3600)},
        }

        if brief_id:
            item["brief_id"] = {"S": brief_id}
        if message_id:
            item["message_id"] = {"S": message_id}

        dynamodb.put_item(TableName=EVENTS_TABLE, Item=item)
    except Exception as e:
        logger.error(f"Error recording event: {e}")


def auto_unsubscribe(email: str, status: str, reason: str):
    """Auto-unsubscribe a subscriber due to bounce/complaint."""
    try:
        dynamodb.update_item(
            TableName=SUBSCRIBERS_TABLE,
            Key={"email": {"S": email}},
            UpdateExpression="SET #s = :status, updated_at = :now, unsubscribe_reason = :reason",
            ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={
                ":status": {"S": status},
                ":now": {"S": datetime.utcnow().isoformat()},
                ":reason": {"S": reason},
            },
        )
        logger.warning(f"Auto-unsubscribed {email}: {reason}")
    except Exception as e:
        logger.error(f"Error auto-unsubscribing {email}: {e}")
