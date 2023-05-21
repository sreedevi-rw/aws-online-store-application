CREATE DEFINER=`root`@`%` PROCEDURE `check_if_product_exists`(IN product_name varchar(255))
BEGIN
	select count(*) from Inventory where name = product_name;
END