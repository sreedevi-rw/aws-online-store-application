CREATE DEFINER=`root`@`%` PROCEDURE `get_all_product_details`()
BEGIN
	select * from Inventory;
END