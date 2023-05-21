import json
import boto3
import pymysql
import os

def handler(event, context):
    print(event)

    session = boto3.session.Session()
    client = session.client(
        service_name = 'secretsmanager'
    )

    secret_name = os.environ['MYSQL_SECRET']
    secretsmanager_response = client.get_secret_value(
        SecretId = secret_name
    )
    mysql_crendtials = json.loads(secretsmanager_response['SecretString'])

    available = False

    conn = None
    try:
        conn = pymysql.connect(host = mysql_crendtials['host'], user = mysql_crendtials['username'], passwd = mysql_crendtials['password'], db = 'StoreManagement')

        if conn:
            cursor = conn.cursor()
            id = event['productId']
            qty = event['qty']

            print("call get_product_available_count")
            cursor.callproc('get_product_available_count', [id])

            result = cursor.fetchone()
            print(result)
            if result != None and result[0] > qty:
                available = True

    except Exception as e:
        print(e)
        print("Error getting mysql connection")
    finally:
        conn.close()

    return available
