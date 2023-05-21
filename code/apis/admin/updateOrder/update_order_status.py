import json
import boto3
import os
import pymysql

def handler(event, context):
    print(event)

    order_id = event['orderId']
    order_status = event['status']

    session = boto3.session.Session()
    client = session.client(
        service_name = 'secretsmanager'
    )

    secret_name = os.environ['MYSQL_SECRET']
    secretsmanager_response = client.get_secret_value(
        SecretId = secret_name
    )
    mysql_crendtials = json.loads(secretsmanager_response['SecretString'])

    update_order_response = {}
    conn = None
    columns = ["order_id","user_id","order_time","order_status"]
    try:
        conn = pymysql.connect(host = mysql_crendtials['host'], user = mysql_crendtials['username'], passwd = mysql_crendtials['password'], db = 'StoreManagement')

        if conn:
            cursor = conn.cursor()
            available = True
            cursor.callproc('update_order_status', [order_id, order_status])
            result = cursor.fetchone()
            print(result)
            for index, column in enumerate(columns):
                if column == 'order_time':
                    update_order_response[column] = json.dumps(result[index], default = str)
                else:
                    update_order_response[column] = result[index]
            print(update_order_response)

    except Exception as e:
        print(e)
        print("Error getting mysql connection")
    finally:
        conn.close()

    return update_order_response
