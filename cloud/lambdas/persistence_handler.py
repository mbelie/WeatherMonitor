import json
import boto3

print('Loading function')

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Weather')

# TODO: Replace string literals with constants
def lambda_handler(event, context):

    message = event['Records'][0]['Sns']['Message']

    # print goes to CloudWatch so does the built in logger
    print(f"Received message: {message}")
    
    data = json.loads(message)
    
    temperature = float(data["temperature_f"])
    humidity = float(data["humidity"])
    pressure = float(data["pressure"])
    deviceId = data["device_id"]
    accountId = data["account_id"]
    timestamp = data["timestamp"]

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

    print(f"DynamoDB put_item response: {response}")

    return {'statusCode': 200, 'body': json.dumps('Weather data processed')}

