CREATE DEFINER=`root`@`%` PROCEDURE `get_my_orders`(IN userId INT)
BEGIN
	select * from Orders where user_id = userId;
END