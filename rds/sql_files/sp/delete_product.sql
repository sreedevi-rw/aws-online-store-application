CREATE DEFINER=`root`@`%` PROCEDURE `delete_product`(IN product_name varchar(255))
BEGIN
	delete from Inventory where name = product_name;
    select * from Inventory where name = product_name;
    commit;
END