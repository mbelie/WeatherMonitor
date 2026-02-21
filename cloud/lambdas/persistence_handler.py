import json
import boto3
import logging

TABLE_NAME = 'Weather'

logger = logging.getLogger()

logger.info('Loading function')

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table(TABLE_NAME)

# TODO: Replace string literals with constants
def lambda_handler(event, context):

    message = event['Records'][0]['Sns']['Message']

    # logger.info goes to CloudWatch so does the built in logger
    logger.info(f"Received message: {message}")
    
    try:
        data = json.loads(message)
        
        temperature = float(data["temperature_f"])
        humidity = float(data["humidity"])
        pressure = float(data["pressure"])
        deviceId = data["device_id"]
        accountId = data["account_id"]
        timestamp = data["timestamp"]
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON: {e}")
        return {'statusCode': 400, 'body': json.dumps('Invalid message format')}
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        return {'statusCode': 500, 'body': json.dumps('Error processing weather data')}

    requiredFields = ["temperature_f", "humidity", "pressure", "device_id", "account_id", "timestamp"]
    
    if not all(field in data for field in requiredFields):
        raise ValueError(f"Missing required fields")

    # TODO: error handling
    response = table.put_item(
        Item={
            'DeviceId': deviceId,
            'AccountId': accountId,
            'Timestamp': timestamp,
            'TemperatureF': temperature,
            'Humidity': humidity,
            'Pressure': pressure
        }
    )

    logger.info(f"DynamoDB put_item response: {response}")

    return {'statusCode': 200, 'body': json.dumps('Weather data processed')}

