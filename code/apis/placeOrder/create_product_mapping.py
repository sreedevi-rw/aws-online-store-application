import json
import boto3
import pymysql
import os

def handler(event, context):

    print(event)
    product = event['product']
    order_id = event['orderId']

    session = boto3.session.Session()
    client = session.client(
        service_name = 'secretsmanager'
    )

    secret_name = os.environ['MYSQL_SECRET']
    secretsmanager_response = client.get_secret_value(
        SecretId = secret_name
    )
    mysql_crendtials = json.loads(secretsmanager_response['SecretString'])

    conn = None
    productMapped = False
    try:
        conn = pymysql.connect(host = mysql_crendtials['host'], user = mysql_crendtials['username'], passwd = mysql_crendtials['password'], db = 'StoreManagement')

        if conn:
            product_id = product['productId']
            qty = product['qty']

            print("call create_order_product_mapping")
            cursor = conn.cursor()
            cursor.callproc('create_order_product_mapping', [order_id, product_id, qty])
            result = cursor.fetchone()
            print(result)
            if result != None :
                productMapped = True

    except Exception as e:
        print(e)
        print("Error getting mysql connection")
    finally:
        conn.close()

    return productMapped