import json
from typing import Any
import boto3
import os

class WeatherDataPublisher:
    ARN = os.getenv("SNS_ARN")
    # TODO: Replace with cert
    ACCESS_KEY = os.getenv("ACCESS_KEY"),
    SECRET_KEY = os.getenv("SECRET_ACCESS_KEY")
    REGION = os.getenv("AWS_REGION")

    snsClient = boto3.client('sns', region_name=REGION, aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

    def publish(self, payload: Any):
        try:
            print(f"Publishing weather data: {payload}")
            response = self.snsClient.publish(TopicArn=self.ARN, Message=json.dumps(payload))
            print(f"SNS publish response: {response}")
        except Exception as error:
            print(f"Error publishing weather data: {error}")