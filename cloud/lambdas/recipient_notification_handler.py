import json
import boto3

print('Loading function')

# TODO: Move to environment variables
PHONE = '+17778889999'
TEMPERATURE_MAX = 100.0
TEMPERATURE_MIN = 40.0

def lambda_handler(event, context):
    message = event['Records'][0]['Sns']['Message']

    # print goes to CloudWatch so does the built in logger
    print(f"Received message: {message}")
    
    data = json.loads(message)
    temperature = float(data["temperature_f"])
    print(f"Temperature: {temperature}°F")

    if temperature <= TEMPERATURE_MIN or temperature >= TEMPERATURE_MAX:
        print("Temperature out of range!")
        sns = boto3.client('sns')

        # TODO: SMS requires setup
        # response = sns.publish(
        #     PhoneNumber=PHONE,
        #     Message=f"Alert! Temperature out of range: {temperature}°F"
        # )
        # return response

        # TODO: Add email notification
    
    print("Temperature within range")
    return {'statusCode': 200, 'body': json.dumps('Temperature within range')}