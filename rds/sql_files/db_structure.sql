create database if not exists StoreManagement;

use StoreManagement;

CREATE TABLE IF NOT EXISTS `Inventory` (
  product_id INT NOT NULL AUTO_INCREMENT,
  name varchar(255) NOT NULL,
  available_count int NOT NULL,
  price float NOT NULL,
  location_in_store varchar(255) NOT NULL,
  PRIMARY KEY(`product_id`)
);

CREATE TABLE IF NOT EXISTS `Orders` (
  order_id INT NOT NULL AUTO_INCREMENT,
  user_id varchar(255) NOT NULL,
  order_time DATETIME NOT NULL,
  order_status varchar(255) NOT NULL,
  PRIMARY KEY(`order_id`)
);

CREATE TABLE IF NOT EXISTS `OrderProductsMapping` (
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  ordered_count int NOT NULL,
  PRIMARY KEY (`order_id`, `product_id`),
  INDEX `fk_OrderProductsMapping_has_Orders_idx` (`order_id` ASC) ,
  INDEX `fk_OrderProductsMapping_has_Inventory_idx` (`product_id` ASC) ,
  CONSTRAINT `fk_OrderProductsMapping_has_Orders_idx`
    FOREIGN KEY (`order_id`)
    REFERENCES `Orders` (`order_id`)
    ON DELETE CASCADE,
  CONSTRAINT `fk_OrderProductsMapping_has_Inventory_idx`
    FOREIGN KEY (`product_id`)
    REFERENCES `Inventory` (`product_id`)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `OrderPickupDetails` (
  order_id INT NOT NULL,
  location_in_store varchar(255) NOT NULL,
  pickup_code varchar(255) NOT NULL,
  pickup_status varchar(255) NOT NULL,
  PRIMARY KEY (`order_id`),
  INDEX `fk_OrderPickupDetails_has_Orders_idx` (`order_id` ASC) ,
  CONSTRAINT `fk_OrderPickupDetails_has_Orders_idx`
    FOREIGN KEY (`order_id`)
    REFERENCES `Orders` (`order_id`)
    ON DELETE CASCADE
);
