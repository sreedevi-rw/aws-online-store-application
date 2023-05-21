CREATE DEFINER=`root`@`%` PROCEDURE if not exists `get_product_details`()
BEGIN
    select * from Inventory;
END