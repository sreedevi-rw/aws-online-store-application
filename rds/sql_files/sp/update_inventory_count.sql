CREATE DEFINER=`root`@`%` PROCEDURE `update_inventory_count`(IN id int, IN product_count int)
BEGIN
	update Inventory set available_count = product_count where product_id = id;
    select * from Inventory where product_id = id;
    commit;
END