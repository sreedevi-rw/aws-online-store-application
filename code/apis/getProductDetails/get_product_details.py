import json
import boto3
import pymysql
import os

def handler(event, context):
    print(event)
    print(event['body'])
    event_body = json.loads(event['body'])
    product_name = event_body['productName']

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
    get_product_details_response = {}
    try:
        conn = pymysql.connect(host = mysql_crendtials['host'], user = mysql_crendtials['username'], passwd = mysql_crendtials['password'], db = 'StoreManagement')

        if conn:
            product_columns = ["product_id", "product_name", "available_count", "price", "location"]

            cursor = conn.cursor()

            print("call get_product_details_by_filter")
            cursor.callproc('get_product_details_by_filter', [product_name])

            product_row = cursor.fetchone()
            if product_row != None:
                print(product_row)
                product = {}
                for index,column in enumerate(product_columns):
                    product[column] = product_row[index]
                get_product_details_response['productDetails'] = product
            else:
                get_product_details_response =  "No such product present"

            print(get_product_details_response)

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
        "body": json.dumps(get_product_details_response)
    }
