CREATE DEFINER=`root`@`%` PROCEDURE `get_product_details_by_filter`(IN productName varchar(255))
BEGIN
	select * from Inventory where name = productName;
END