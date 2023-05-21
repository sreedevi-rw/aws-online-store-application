import json
import os
import boto3

def handler(event, context):
    print(event)
    event_body = json.loads(event['Records'][0]['body'])

    email_body = event_body['emailBody']
    email_subject = event_body['emailSubject']
    to_address = event_body['toAddress']

    email_message = {
        'Body': {
            'Text': {
                'Data': json.dumps(email_body),
            }
        },
        'Subject': {
            'Data': email_subject
        }
    }

    from_email = os.environ['FROM_EMAIL_ID']
    config_set_name = os.environ["SES_CONFIG_NAME"]

    client = boto3.client('ses')
    ses_response = client.send_email(
        Destination = {
            'ToAddresses': to_address
        },
        Message = email_message,
        Source = from_email,
        ConfigurationSetName = config_set_name
    )
    print(ses_response['MessageId'])

    return {
        'statusCode': 200,
        'body': json.dumps('Mail sent')
    }
