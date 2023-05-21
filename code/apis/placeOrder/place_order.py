import json
import boto3
import os
import pymysql

def handler(event, context):
    print(event)

    user_details = event['lambda-cognito-authorizer']

    session = boto3.session.Session()
    client = session.client(
        service_name = 'secretsmanager'
    )

    secret_name = os.environ['MYSQL_SECRET']
    secretsmanager_response = client.get_secret_value(
        SecretId = secret_name
    )
    mysql_crendtials = json.loads(secretsmanager_response['SecretString'])

    orderId = None
    conn = None
    try:
        conn = pymysql.connect(host = mysql_crendtials['host'], user = mysql_crendtials['username'], passwd = mysql_crendtials['password'], db = 'StoreManagement')

        if conn:
            cursor = conn.cursor()
            available = True
            cursor.callproc('create_order', [user_details['sub']])
            columns = ["order_id","user_id","order_time","order_status"]
            result = cursor.fetchone()
            print(result)
            order_id = result[0]

    except Exception as e:
        print(e)
        print("Error getting mysql connection")
    finally:
        conn.close()

    return order_id
