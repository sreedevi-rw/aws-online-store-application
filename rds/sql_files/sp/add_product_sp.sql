CREATE DEFINER=`root`@`%` PROCEDURE `add_product`(IN product_name varchar(255), IN product_count int, IN product_price float, IN location varchar(255))
BEGIN
	insert into Inventory (name, available_count, price, location_in_store) values (product_name, product_count, product_price, location);
	select * from Inventory where product_id = last_insert_id();
	commit;
END