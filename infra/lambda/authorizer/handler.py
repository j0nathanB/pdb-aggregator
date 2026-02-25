"""
API Key authorizer Lambda - validates x-api-key header against Secrets Manager.
"""

import boto3
import json
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

secrets = boto3.client("secretsmanager")
API_KEY_SECRET_ARN = os.environ["API_KEY_SECRET_ARN"]

# Cache the API key to avoid repeated Secrets Manager calls
_cached_api_key = None


def handler(event, context):
    """
    Validate API key from x-api-key header.
    Returns simple response for API Gateway 2.0 payload format.
    """
    logger.info(f"Authorizer invoked")

    # Get the API key from headers
    headers = event.get("headers", {})
    provided_key = headers.get("x-api-key", "")

    if not provided_key:
        logger.warning("No API key provided")
        return {"isAuthorized": False}

    # Get the expected API key
    expected_key = get_api_key()
    if not expected_key:
        logger.error("Failed to retrieve API key from Secrets Manager")
        return {"isAuthorized": False}

    # Constant-time comparison to prevent timing attacks
    if secrets_equal(provided_key, expected_key):
        logger.info("API key validated successfully")
        return {"isAuthorized": True}
    else:
        logger.warning("Invalid API key")
        return {"isAuthorized": False}


def get_api_key() -> str:
    """Get API key from Secrets Manager, with caching."""
    global _cached_api_key

    if _cached_api_key:
        return _cached_api_key

    try:
        response = secrets.get_secret_value(SecretId=API_KEY_SECRET_ARN)
        secret = json.loads(response["SecretString"])
        _cached_api_key = secret.get("api_key", "")
        return _cached_api_key
    except Exception as e:
        logger.error(f"Error retrieving secret: {e}")
        return ""


def secrets_equal(a: str, b: str) -> bool:
    """Constant-time string comparison."""
    if len(a) != len(b):
        return False

    result = 0
    for x, y in zip(a.encode(), b.encode()):
        result |= x ^ y

    return result == 0
