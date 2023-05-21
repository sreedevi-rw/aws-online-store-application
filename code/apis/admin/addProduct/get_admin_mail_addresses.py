import json
import boto3
import os

def handler(event, context):

    user_pool_id = os.environ['USER_POOL_ID']
    group_name = os.environ['ADMIN_GROUP']

    cognito_idp_client = boto3.client("cognito-idp")
    list_users_in_group_response = cognito_idp_client.list_users_in_group(
        UserPoolId = user_pool_id,
        GroupName = group_name
    )
    print(list_users_in_group_response)

    email_ids = []
    for user in list_users_in_group_response['Users']:
        print(user)
        attribute = next(attribute for attribute in user['Attributes'] if attribute['Name'] == "email")
        print(attribute)
        email_ids.append(attribute['Value'])
    print(email_ids)

    event["adminEmailIds"] = email_ids

    return event
