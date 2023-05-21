import json
import boto3
import os

def handler(event, context):
    print(event)

    username = event['username']
    user_pool_id = os.environ["USER_POOL_ID"]

    cognito_client = boto3.client('cognito-idp')

    admin_add_user_to_group_response = cognito_client.admin_add_user_to_group(
        UserPoolId = user_pool_id,
        Username = username,
        GroupName = os.environ["COGNITO_ADMIN_GROUP_NAME"]
    )
    print("admin_add_user_to_group_response = ", admin_add_user_to_group_response)

    return admin_add_user_to_group_response

