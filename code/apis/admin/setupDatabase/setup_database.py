import json
import boto3
import pymysql
import os

def handler(event, context):
    print(event)

    session = boto3.session.Session()
    print("boto session")
    client = session.client(
        service_name = 'secretsmanager'
    )
    print("boto client")
    secret_name = os.environ['MYSQL_SECRET']
    print("secret_name: ", secret_name)
    secretsmanager_response = client.get_secret_value(
        SecretId = secret_name
    )
    print("response from secret: ", secretsmanager_response)
    mysql_crendtials = json.loads(secretsmanager_response['SecretString'])

    conn = None
    get_product_details_response = {}
    try:
        conn = pymysql.connect(host = mysql_crendtials['host'], user = mysql_crendtials['username'], passwd = mysql_crendtials['password'])

        if conn:
            cursor = conn.cursor()
            cursor.execute("select @@version")
            print(cursor.fetchall())
            sql_qry = "create database if not exists StoreManagement;"
            cursor.execute(sql_qry)
            print(cursor.fetchall())
            cursor.execute("show databases;")
            print(cursor.fetchall())
            sql_qry = "use StoreManagement;"
            cursor.execute(sql_qry)
            sql_qry = "CREATE TABLE IF NOT EXISTS Inventory (product_id INT NOT NULL AUTO_INCREMENT,name varchar(255) NOT NULL,available_count int NOT NULL,price float NOT NULL,location_in_store varchar(255) NOT NULL,PRIMARY KEY(product_id));"
            cursor.execute(sql_qry)
            print(cursor.fetchall())
            sql_qry = "CREATE TABLE IF NOT EXISTS Orders (order_id INT NOT NULL AUTO_INCREMENT,user_id varchar(255) NOT NULL,order_time DATETIME NOT NULL,order_status varchar(255) NOT NULL,PRIMARY KEY(order_id));"
            cursor.execute(sql_qry)
            print(cursor.fetchall())
            sql_qry = "CREATE TABLE IF NOT EXISTS OrderProductsMapping (order_id INT NOT NULL,product_id INT NOT NULL,ordered_count int NOT NULL,PRIMARY KEY (order_id, product_id),INDEX fk_OrderProductsMapping_has_Orders_idx (order_id ASC),INDEX fk_OrderProductsMapping_has_Inventory_idx (product_id ASC) ,CONSTRAINT fk_OrderProductsMapping_has_Orders_idx FOREIGN KEY (order_id) REFERENCES Orders (order_id) ON DELETE CASCADE, CONSTRAINT fk_OrderProductsMapping_has_Inventory_idx FOREIGN KEY (product_id) REFERENCES Inventory (product_id) ON DELETE CASCADE);"
            cursor.execute(sql_qry)
            print(cursor.fetchall())
            sql_qry = "CREATE TABLE IF NOT EXISTS OrderPickupDetails (order_id INT NOT NULL, location_in_store varchar(255) NOT NULL, pickup_code varchar(255) NOT NULL, pickup_status varchar(255) NOT NULL, PRIMARY KEY (order_id), INDEX fk_OrderPickupDetails_has_Orders_idx (order_id ASC) , CONSTRAINT fk_OrderPickupDetails_has_Orders_idx FOREIGN KEY (order_id) REFERENCES Orders (order_id) ON DELETE CASCADE);"
            cursor.execute(sql_qry)
            print(cursor.fetchall())

          # /***************************************************************************************
          #  * PyMySQL Stored Procedure Creation *
          #  * Referred from :  Github Issues - PyMySQL Stored Procedure Creation *
          #  * Availability: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secret.html *
          #  * Accessed: 11th April, 2023
          #  * **************************************************************************************/

            cursor.execute("""
              CREATE PROCEDURE if not exists add_product(IN product_name varchar(255), IN product_count int, IN product_price float, IN location varchar(255))
              BEGIN
                insert into Inventory (name, available_count, price, location_in_store) values (product_name, product_count, product_price, location);
            	select * from Inventory where product_id = last_insert_id();
            	commit;
              END
            """)
            cursor.execute("show create procedure add_product;")
            print(cursor.fetchall())
            
            cursor.execute("""
                CREATE PROCEDURE if not exists check_if_product_exists(IN product_name varchar(255))
                BEGIN
                	select count(*) from Inventory where name = product_name;
                END
            """)
            cursor.execute("show create procedure check_if_product_exists;")
            print(cursor.fetchall())
            
            cursor.execute("""
                CREATE PROCEDURE if not exists check_if_product_id_exists(IN productId int)
                BEGIN
                	select count(*) from Inventory where product_id = productId;
                END
            """)
            cursor.execute("show create procedure check_if_product_id_exists;")
            print(cursor.fetchall())
            
            cursor.execute("""
                CREATE PROCEDURE if not exists create_order(in user_sub varchar(255))
                BEGIN
                	insert into Orders(user_id, order_time, order_status) values (user_sub, now(), "Order placed");
                    select * from Orders where order_id = last_insert_id();
                    commit;
                END
            """)
            cursor.execute("show create procedure create_order;")
            print(cursor.fetchall())
            
            cursor.execute("""
                CREATE PROCEDURE if not exists create_order_product_mapping(IN orderId INT, IN productId INT, IN qty INT)
                BEGIN
                	insert into OrderProductsMapping (order_id, product_id, ordered_count) values(orderId, productId, qty);
                    select * from OrderProductsMapping where order_id = orderId;
                    commit;
                END
            """)
            cursor.execute("show create procedure create_order_product_mapping;")
            print(cursor.fetchall())
            
            cursor.execute("""
                CREATE PROCEDURE if not exists delete_product(IN product_name varchar(255))
                BEGIN
                	delete from Inventory where name = product_name;
                    select * from Inventory where name = product_name;
                    commit;
                END
            """)
            cursor.execute("show create procedure delete_product;")
            print(cursor.fetchall())
            
            cursor.execute("""
                CREATE PROCEDURE if not exists get_all_product_details()
                BEGIN
                	select * from Inventory;
                END
            """)
            cursor.execute("show create procedure get_all_product_details;")
            print(cursor.fetchall())
            
            cursor.execute("""
                CREATE PROCEDURE if not exists get_my_orders(IN userId INT)
                BEGIN
                	select * from Orders where user_id = userId;
                END
            """)
            cursor.execute("show create procedure get_my_orders;")
            print(cursor.fetchall())
            
            cursor.execute("""
                CREATE PROCEDURE if not exists get_order_details(IN orderId INT)
                BEGIN
                	select Inventory.name, OrderProductsMapping.ordered_count, Orders.order_id, Orders.order_time, Orders.order_status, Orders.user_id from OrderProductsMapping
                    INNER JOIN Inventory ON OrderProductsMapping.product_id = Inventory.product_id
                    INNER JOIN Orders ON OrderProductsMapping.order_id = Orders.order_id
                    where OrderProductsMapping.order_id = orderId;
                END
            """)
            cursor.execute("show create procedure get_order_details;")
            print(cursor.fetchall())
            
            cursor.execute("""
                CREATE PROCEDURE if not exists get_product_available_count(in id int)
                BEGIN
                	select available_count from Inventory where product_id = id;
                END
            """)
            cursor.execute("show create procedure get_product_available_count;")
            print(cursor.fetchall())
            
            cursor.execute("""
                CREATE PROCEDURE if not exists get_product_details()
                BEGIN
                	select * from Inventory;
                END
            """)
            cursor.execute("show create procedure get_product_details;")
            print(cursor.fetchall())
            
            cursor.execute("""
                CREATE PROCEDURE if not exists get_product_details_by_filter(IN productName varchar(255))
                BEGIN
                	select * from Inventory where name = productName;
                END
            """)
            cursor.execute("show create procedure get_product_details_by_filter;")
            print(cursor.fetchall())
            
            cursor.execute("""
                CREATE PROCEDURE if not exists update_inventory_count(IN id int, IN product_count int)
                BEGIN
                	update Inventory set available_count = product_count where product_id = id;
                    select * from Inventory where product_id = id;
                    commit;
                END
            """)
            cursor.execute("show create procedure update_inventory_count;")
            print(cursor.fetchall())
            
            cursor.execute("""
                CREATE PROCEDURE if not exists update_inventory_price(IN id int, IN product_price float)
                BEGIN
                	update Inventory set price = product_price where product_id = id;
                    select * from Inventory where product_id = id;
                    commit;
                END
            """)
            cursor.execute("show create procedure update_inventory_price;")
            print(cursor.fetchall())
            
            cursor.execute("""
                CREATE PROCEDURE if not exists update_order_status(IN orderId INT, IN orderStatus varchar(255))
                BEGIN
                	update Orders set order_status = orderStatus where order_id = orderId;
                    select * from Orders where order_id = orderId;
                    commit;
                END
            """)
            cursor.execute("show create procedure update_order_status;")
            print(cursor.fetchall())
            
            cursor.execute("""
                CREATE PROCEDURE if not exists update_pickup_details(IN orderId INT, IN pickupLocation varchar(255), IN pickupCode INT, IN pickupStatus varchar(255))
                BEGIN
                	insert into OrderPickupDetails values(orderId, pickupLocation, pickupCode, pickupStatus);
                    select  location_in_store, pickup_code, pickup_status from OrderPickupDetails where order_id = orderId;
                    commit;
                END
            """)
            cursor.execute("show create procedure update_pickup_details;")
            print(cursor.fetchall())
            
            cursor.execute("SHOW PROCEDURE STATUS WHERE Db = 'StoreManagement';")
            print(cursor.fetchall())
            
            cursor.execute("show tables;")
            print(cursor.fetchall())

    except Exception as e:
        print(e)
        print("Error getting mysql connection")
    finally:
        conn.close()

    return "Created database, tables and stored procedures!"
