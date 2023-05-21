CREATE DEFINER=`root`@`%` PROCEDURE `create_order`(in user_sub varchar(255))
BEGIN
	insert into Orders(user_id, order_time, order_status) values (user_sub, now(), "Order placed");
    select * from Orders where order_id = last_insert_id();
    commit;
END