import json
import boto3
import os

def handler(event, context):
    print(event)
    email = event['email']

    ses_client = boto3.client('ses')
    verify_email_identity_response = ses_client.verify_email_identity(
        EmailAddress = email
    )
    print("verify_email_identity_response = ", verify_email_identity_response)

    return verify_email_identity_response
