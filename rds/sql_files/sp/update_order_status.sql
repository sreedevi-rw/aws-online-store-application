CREATE DEFINER=`root`@`%` PROCEDURE `update_order_status`(IN orderId INT, IN orderStatus varchar(255))
BEGIN
	update Orders set order_status = orderStatus where order_id = orderId;
    select * from Orders where order_id = orderId;
    commit;
END