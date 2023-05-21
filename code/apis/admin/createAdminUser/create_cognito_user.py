import json
import boto3
import os

def handler(event, context):
    print(event)
    email = event['email']
    username = event['username']
    user_pool_id = os.environ["USER_POOL_ID"]

    cognito_client = boto3.client('cognito-idp')
    admin_create_user_response = cognito_client.admin_create_user(
        UserPoolId = user_pool_id,
        Username = username,
        UserAttributes = [
            { "Name": "email", "Value": email },
            { "Name": "email_verified", "Value": "true" }
        ],
        DesiredDeliveryMediums = ['EMAIL'])
    print("admin_create_user_response = ", admin_create_user_response)

    return json.dumps(admin_create_user_response['User'], default=str)

