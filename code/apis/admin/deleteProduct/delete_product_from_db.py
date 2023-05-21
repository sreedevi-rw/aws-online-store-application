import json
import boto3
import pymysql
import os

def handler(event, context):
    print(event)

    product_name = event['productName']

    delete_product_response = {
        "msg": "Product deleted successfully!"
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
            cursor = conn.cursor()

            print("call delete_product")
            cursor.callproc('delete_product', [product_name])

            if len(cursor.fetchall()) > 0:
                delete_product_response["msg"] = "Deletion failed"
            else:
                delete_product_response['deletedProduct'] = product_name + " has been deleted"

    except Exception as e:
        print(e)
        print("Error getting mysql connection")
    finally:
        conn.close()

    return delete_product_response



    ""