import json
import logging
import os
from typing import Any

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

class WeatherDataPublisher:
    """Publishes weather data to AWS SNS topic."""
    
    def __init__(self):
        """Initialize the publisher with validated environment variables."""
        self.arn = os.getenv("SNS_ARN")
        self.region = os.getenv("AWS_REGION")
        
        # Validate required environment variables
        missing_vars = []
        if not self.arn:
            missing_vars.append("SNS_ARN")
        if not self.region:
            missing_vars.append("AWS_REGION")
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        # Use default AWS credential chain (IAM roles, environment variables, etc.)
        self.sns_client = boto3.client('sns', region_name=self.region)

    def publish(self, payload: Any) -> dict:
        """Publish weather data to SNS topic.
        
        Args:
            payload: The weather data to publish.
            
        Returns:
            The SNS publish response containing MessageId.
            
        Raises:
            ValueError: If payload is empty.
            ClientError: If SNS publish fails.
        """
        if not payload:
            raise ValueError("Payload cannot be empty")
        
        try:
            response = self.sns_client.publish(TopicArn=self.arn, Message=json.dumps(payload))
            logger.info(f"SNS publish response: {response}")
            return response
        except ClientError as error:
            logger.error(f"AWS error publishing weather data: {error}")
            raise
        except Exception as error:
            logger.error(f"Unexpected error publishing weather data: {error}")
            raise