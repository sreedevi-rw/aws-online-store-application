CREATE DEFINER=`root`@`%` PROCEDURE `create_order_product_mapping`(IN orderId INT, IN productId INT, IN qty INT)
BEGIN
	insert into OrderProductsMapping (order_id, product_id, ordered_count) values(orderId, productId, qty);
    select * from OrderProductsMapping where order_id = orderId;
    commit;
END