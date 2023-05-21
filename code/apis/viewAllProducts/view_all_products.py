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

    conn = None
    view_all_products_response = []
    try:
        conn = pymysql.connect(host = mysql_crendtials['host'], user = mysql_crendtials['username'], passwd = mysql_crendtials['password'], db = 'StoreManagement')

        if conn:
            product_columns = ["product_id", "product_name", "available_count", "location", "price"]

            cursor = conn.cursor()

            print("call get_all_product_details")
            cursor.callproc('get_all_product_details', [])

            products = []
            product_rows = cursor.fetchall()
            for product_row in product_rows:
                print(product_row)
                product = {}
                for index,column in enumerate(product_columns):
                    product[column] = product_row[index]
                products.append(product)

            if len(products) > 0:
                view_all_products_response = products
            else:
                view_all_products_response = [ "No products present" ]

            print(view_all_products_response)

    except Exception as e:
        print(e)
        print("Error getting mysql connection")
    finally:
        conn.close()

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(view_all_products_response)
    }
