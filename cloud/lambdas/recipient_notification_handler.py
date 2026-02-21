import json
import boto3
import logging
import os
logger = logging.getLogger()

logger.info('Loading function')

PHONE = os.getenv('ALERT_PHONE_NUMBER')
TEMPERATURE_MAX = float(os.getenv('TEMPERATURE_MAX', '100.0'))
TEMPERATURE_MIN = float(os.getenv('TEMPERATURE_MIN', '40.0'))

def lambda_handler(event, context):
    message = event['Records'][0]['Sns']['Message']

    # logger.info goes to CloudWatch so does the built in logger
    logger.info(f"Received message: {message}")
    
    try:
        data = json.loads(message)
        temperature = float(data.get("temperature_f"))
        if temperature is None:
            raise ValueError("Missing temperature_f field")
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        logger.error(f"Error processing message: {e}")
        return {'statusCode': 400, 'body': json.dumps('Invalid message')}

    logger.info(f"Temperature: {temperature}°F")

    if temperature <= TEMPERATURE_MIN or temperature >= TEMPERATURE_MAX:
        logger.info("Temperature out of range!")
        sns = boto3.client('sns')

        # TODO: SMS requires setup
        # response = sns.publish(
        #     PhoneNumber=PHONE,
        #     Message=f"Alert! Temperature out of range: {temperature}°F"
        # )
        # return response

        # TODO: Add email notification
    
    logger.info("Temperature within range")
    return {'statusCode': 200, 'body': json.dumps('Temperature within range')}