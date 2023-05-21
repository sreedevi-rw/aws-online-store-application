CREATE DEFINER=`root`@`%` PROCEDURE `update_inventory_price`(IN id int, IN product_price float)
BEGIN
	update Inventory set price = product_price where product_id = id;
    select * from Inventory where product_id = id;
    commit;
END