import json
import boto3
import pymysql
import os

def handler(event, context):
    print(event)
    print(event['headers'])
    print(event['requestContext'])
    user_id = event['requestContext']['authorizer']['sub']

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
    get_my_orders_response = []
    try:
        conn = pymysql.connect(host = mysql_crendtials['host'], user = mysql_crendtials['username'], passwd = mysql_crendtials['password'], db = 'StoreManagement')

        if conn:
            order_columns = ["order_id", "user_id", "order_time", "order_status"]
            product_columns = ["product_name", "qty"]

            cursor = conn.cursor()

            print("call get_my_orders")
            cursor.callproc('get_my_orders', [user_id])

            orders = []
            last_result = []
            order_rows = cursor.fetchall()
            for order_row in order_rows:
                print(order_row)
                order = {}
                for index,column in enumerate(order_columns):
                    if column == 'order_time':
                        order[column] = json.dumps(order_row[index], default = str)
                    else:
                        order[column] = order_row[index]

                cursor.callproc('get_order_details', [order['order_id']])
                products = []
                for product_row in cursor.fetchall():
                    print(product_row)
                    product = {}
                    for index,column in enumerate(product_columns):

                        product[column] = product_row[index]
                    products.append(product)
                order['products'] = products
                orders.append(order)

            if len(orders) > 0:
                get_my_orders_response = orders
            else:
                get_my_orders_response = [ "No orders yet" ]

            print(get_my_orders_response)

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
        "body": json.dumps(get_my_orders_response)
    }
