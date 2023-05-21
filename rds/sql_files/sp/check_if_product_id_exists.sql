CREATE DEFINER=`root`@`%` PROCEDURE `check_if_product_id_exists`(IN productId int)
BEGIN
	select count(*) from Inventory where product_id = productId;
END