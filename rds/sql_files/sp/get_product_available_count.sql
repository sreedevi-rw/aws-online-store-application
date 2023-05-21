CREATE DEFINER=`root`@`%` PROCEDURE `get_product_available_count`(in id int)
BEGIN
	select available_count from Inventory where product_id = id;
END