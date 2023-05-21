import json
import boto3

def handler(event, context):
    print(event)

    username = event['userName']
    user_pool_id = event['userPoolId']
    email = event['request']['userAttributes']['email']

    cognito_client = boto3.client('cognito-idp')
    admin_add_user_to_group_response = cognito_client.admin_add_user_to_group(
        UserPoolId = user_pool_id,
        Username = username,
        GroupName = 'customers'
    )
    print("admin_add_user_to_group_response = ", admin_add_user_to_group_response)

    ses_client = boto3.client('ses')
    verify_email_identity_response = ses_client.verify_email_identity(
        EmailAddress = email
    )
    print("verify_email_identity_response = ", verify_email_identity_response)

    return event
