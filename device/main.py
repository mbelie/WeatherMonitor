import json
import logging
import os
from datetime import datetime, timezone
import boto3

# Region, access key and secret access key come from AWS configuration
snsClient = boto3.client('sns')
logger = logging.getLogger(__name__)

try:
   # Test payload
   payload = {
        "device_id": 1,
        "account_id": 2,
        "temperature_f": 39,
        "humidity": 50,
        "pressure": 1000,
        "timestamp": f"{datetime.now(timezone.utc).isoformat()}"
    }
   
   arn = os.getenv('SNS_ARN')

   if not arn:
         raise ValueError("SNS_ARN environment variable is not set.")
   
   arn = arn.strip()

   logger.info(f"Publishing weather data: {payload}...")

   response = snsClient.publish(TopicArn=arn, Message=json.dumps(payload))
   
   logger.info(f"SNS publish response: {response}")

except Exception as error:
    logger.info(f"Error publishing weather data: {error}")