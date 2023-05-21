import json
import boto3
import pymysql
import os

def handler(event, context):
    print(event)
    order_id = None
    return_json = False
    try:
        order_id = event['orderId']
    except:
        event_body = json.loads(event['body'])
        order_id = event_body['orderId']
        return_json = True
    print(order_id)

    session = boto3.session.Session()
    client = session.client(
        service_name = 'secretsmanager'
    )

    secret_name = os.environ['MYSQL_SECRET']
    secretsmanager_response = client.get_secret_value(
        SecretId = secret_name
    )
    mysql_crendtials = json.loads(secretsmanager_response['SecretString'])

    get_order_details_response = {}

    conn = None
    try:
        conn = pymysql.connect(host = mysql_crendtials['host'], user = mysql_crendtials['username'], passwd = mysql_crendtials['password'], db = 'StoreManagement')

        if conn:
            columns = ["product_name", "qty"]

            cursor = conn.cursor()

            print("call get_order_details")
            cursor.callproc('get_order_details', [order_id])

            rows = []
            last_result = []
            for result in cursor.fetchall():
                print(result)
                row = {}
                for index,column in enumerate(columns):
                    row[column] = result[index]
                rows.append(row)
                last_result = result
            if len(rows) > 0:
                get_order_details_response['customerEmailId'] = getEmailAddress(last_result[5])
                get_order_details_response['orderDetails'] = {
                    "order_id": last_result[2],
                    "order_time":  json.dumps(last_result[3], default = str),
                    "order_status": last_result[4],
                    "orderDetails": rows
                    }
                if 'pickupDetails' in event.keys():
                    get_order_details_response['orderDetails']['pickupDetails'] = event['pickupDetails']

            print(get_order_details_response)

    except Exception as e:
        print(e)
        print("Error getting mysql connection")
    finally:
        conn.close()

    if return_json:
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(get_order_details_response)
        }
    else:
        return get_order_details_response

def getEmailAddress(userID):
    email = ""
    cognito_client = boto3.client("cognito-idp")
    list_users_response = cognito_client.list_users(
        UserPoolId = os.environ['COGNITO_USER_POOL_ID'],
        AttributesToGet = ['email'],
        Filter = "sub = \"" + userID + "\""
    )
    print(list_users_response)
    users = list_users_response['Users']
    filteredUser = users[0]
    user_attributes = filteredUser['Attributes']
    for user_attribute in user_attributes:
        if user_attribute['Name'] == 'email':
            email = user_attribute['Value']
            break

    return email
