import json
import boto3
import os
import time

def handler(event, context):
    print(event)
    event_body = event['body']
    event_body['lambda-cognito-authorizer'] = event['lambda-cognito-authorizer']
    stepFnArn = event['stepFnARn']
    print(event_body)
    stepfunctions_client = boto3.client('stepfunctions')
    sf_start_exec_response = stepfunctions_client.start_execution(
        stateMachineArn = stepFnArn,
        input = json.dumps(event_body)
    )
    print(sf_start_exec_response)

    exec_arn = sf_start_exec_response['executionArn']
    output = {}

    for _ in range(5):
        time.sleep(5)
        sf_describe_execution_resp =  stepfunctions_client.describe_execution(
            executionArn = exec_arn
        )
        print(sf_describe_execution_resp)
        if 'output' in sf_describe_execution_resp.keys():
            output = json.loads(sf_describe_execution_resp['output'])
            print(output)
            if output['isEnd']:
                del output['isEnd']
                break

    return output