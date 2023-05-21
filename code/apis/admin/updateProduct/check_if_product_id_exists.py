import json
import boto3
import pymysql
import os

def handler(event, context):
    print(event)
    product_id = event['productId']

    session = boto3.session.Session()

    client = session.client(
        service_name = 'secretsmanager'
    )

    secret_name = os.environ['MYSQL_SECRET']
    secretsmanager_response = client.get_secret_value(
        SecretId = secret_name
    )

    mysql_crendtials = json.loads(secretsmanager_response['SecretString'])
    print(mysql_crendtials)

    conn = None
    try:
        event["productExists"] = True

        conn = pymysql.connect(host = mysql_crendtials['host'], user = mysql_crendtials['username'], passwd = mysql_crendtials['password'], db = 'StoreManagement')

        if conn:
            cursor = conn.cursor()
            print("call check_if_product_id_exists")
            cursor.callproc('check_if_product_id_exists', [product_id])

            for result in cursor.fetchall():
                print(result)
                if result[0] > 0:
                    event["productExists"] = True
                else:
                    event["productExists"] = False

    except Exception as e:
        print(e)
        print("Error getting mysql connection")
    finally:
        conn.close()

    return event