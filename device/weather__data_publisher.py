import json
from typing import Any
import boto3
import os

class WeatherDataPublisher:
    ARN = os.getenv("SNS_ARN")
    snsClient = boto3.client('sns', region_name='us-west-1')

    def publish(self, payload: Any):
        print(f"Publishing weather data: {payload}")
        response = self.snsClient.publish(TopicArn=self.ARN, Message=json.dumps(payload))
        print(f"SNS publish response: {response}")