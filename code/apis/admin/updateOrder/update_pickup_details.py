import json
import boto3
import os
import pymysql
import random

def handler(event, context):
    print(event)

    order_id = event['orderId']
    pickup_code = random.randint(1111,9999)
    pickup_location = event['pickupLocation']
    pickup_status = "Pending"

    session = boto3.session.Session()
    client = session.client(
        service_name = 'secretsmanager'
    )

    secret_name = os.environ['MYSQL_SECRET']
    secretsmanager_response = client.get_secret_value(
        SecretId = secret_name
    )
    mysql_crendtials = json.loads(secretsmanager_response['SecretString'])

    update_pickup_details_response = {}
    conn = None
    try:
        columns = ["pickup_location", "pickup_code", "pickup_status"]
        conn = pymysql.connect(host = mysql_crendtials['host'], user = mysql_crendtials['username'], passwd = mysql_crendtials['password'], db = 'StoreManagement')

        if conn:
            cursor = conn.cursor()
            available = True
            cursor.callproc('update_pickup_details', [order_id, pickup_location, pickup_code, pickup_status])
            result = cursor.fetchone()
            print(result)
            for index, column in enumerate(columns):
                update_pickup_details_response[column] = result[index]
            print(update_pickup_details_response)

    except Exception as e:
        print(e)
        print("Error getting mysql connection")
    finally:
        conn.close()

    return update_pickup_details_response
