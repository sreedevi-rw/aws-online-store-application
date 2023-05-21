import json
import boto3
import pymysql
import os

def handler(event, context):
    print(event)

    product_id = event['productId']
    price = event['price']

    update_product_response = {
        "msg": "Product update failed!"
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
    update_product_response = {}
    try:
        conn = pymysql.connect(host = mysql_crendtials['host'], user = mysql_crendtials['username'], passwd = mysql_crendtials['password'], db = 'StoreManagement')

        if conn:
            columns = ["product_id","name","available_count","location_in_store","price"]
            cursor = conn.cursor()

            print("call update_inventory_price")
            cursor.callproc('update_inventory_price', [product_id, price])

            rows = []
            for result in cursor.fetchall():
                print(result)
                row = {}
                for index,column in enumerate(columns):
                    row[column] = result[index]
                rows.append(row)

            if len(rows) > 0:
                update_product_response['msg'] = "A product's price has been updated"
                update_product_response['updatedRow'] = rows


    except Exception as e:
        print(e)
        print("Error getting mysql connection")
    finally:
        conn.close()

    return update_product_response