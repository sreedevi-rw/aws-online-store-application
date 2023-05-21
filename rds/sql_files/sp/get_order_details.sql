CREATE DEFINER=`root`@`%` PROCEDURE `get_order_details`(IN orderId INT)
BEGIN
	select Inventory.name, OrderProductsMapping.ordered_count, Orders.order_id, Orders.order_time, Orders.order_status, Orders.user_id from OrderProductsMapping
    INNER JOIN Inventory ON OrderProductsMapping.product_id = Inventory.product_id
    INNER JOIN Orders ON OrderProductsMapping.order_id = Orders.order_id
    where OrderProductsMapping.order_id = orderId;
END