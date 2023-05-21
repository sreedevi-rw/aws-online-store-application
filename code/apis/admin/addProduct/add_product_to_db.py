import json
import boto3
import pymysql
import os

def handler(event, context):
    print(event)

    product_name = event['productName']
    product_qty = event['count']
    location = event['location']
    price = event['price']

    add_product_response = {
        "msg": "Product added successfully!"
    }

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
    try:
        conn = pymysql.connect(host = mysql_crendtials['host'], user = mysql_crendtials['username'], passwd = mysql_crendtials['password'], db = 'StoreManagement')

        if conn:
            columns = ["product_id","name","available_count","location_in_store","price"]
            cursor = conn.cursor()

            print("call add_product")
            cursor.callproc('add_product', [product_name, product_qty, price, location])

            rows = []
            for result in cursor.fetchall():
                print(result)
                row = {}
                for index,column in enumerate(columns):
                    row[column] = result[index]
                rows.append(row)
            add_product_response['addedRow'] = rows
    except Exception as e:
        print(e)
        print("Error getting mysql connection")
    finally:
        conn.close()

    return add_product_response