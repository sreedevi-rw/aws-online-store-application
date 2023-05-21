CREATE DEFINER=`root`@`%` PROCEDURE `update_pickup_details`(IN orderId INT, IN pickupLocation varchar(255), IN pickupCode INT, IN pickupStatus varchar(255))
BEGIN
	insert into OrderPickupDetails values(orderId, pickupLocation, pickupCode, pickupStatus);
    select  location_in_store, pickup_code, pickup_status from OrderPickupDetails where order_id = orderId;
    commit;
END