-- Active: 1683292094538@@127.0.0.1@3306@ecommerce_webapp

create database ecommerce_webapp;

use ecommerce_webapp;

CREATE TABLE
    `role` (
        `role_id` int NOT NULL AUTO_INCREMENT,
        `role_name` enum('admin', 'vendor', 'customer') NOT NULL,
        PRIMARY KEY (`role_id`)
    )

CREATE TABLE
    `user` (
        `user_id` int NOT NULL AUTO_INCREMENT,
        `role_id` int NOT NULL,
        `email` varchar(100) NOT NULL,
        `username` varchar(50) NOT NULL,
        `first_name` varchar(50) NOT NULL,
        `last_name` varchar(50) NOT NULL,
        `password` varchar(60) NOT NULL,
        PRIMARY KEY (`user_id`),
        UNIQUE KEY `email` (`email`),
        UNIQUE KEY `username` (`username`),
        KEY `user_role_fk` (`role_id`),
        CONSTRAINT `user_role_fk` FOREIGN KEY (`role_id`) REFERENCES `role` (`role_id`)
    )

CREATE TABLE
    `product` (
        `product_id` int NOT NULL AUTO_INCREMENT,
        `name` varchar(255) NOT NULL,
        `description` text,
        `rating` int DEFAULT '0',
        `rating_count` int DEFAULT '0',
        `category` enum(
            'sticky note',
            'notebook',
            'tablet',
            'bundle'
        ) DEFAULT NULL,
        PRIMARY KEY (`product_id`)
    )

CREATE TABLE
    `color` (
        `color_id` int NOT NULL AUTO_INCREMENT,
        `color_name` varchar(30) NOT NULL,
        PRIMARY KEY (`color_id`),
        UNIQUE KEY `color_name` (`color_name`)
    )

CREATE TABLE
    `size` (
        `size_id` int NOT NULL AUTO_INCREMENT,
        `size_name` varchar(30) NOT NULL,
        PRIMARY KEY (`size_id`),
        UNIQUE KEY `size_name` (`size_name`)
    )

CREATE TABLE
    `product_variant` (
        `prod_var_id` int NOT NULL AUTO_INCREMENT,
        `product_id` int NOT NULL,
        `color_id` int NOT NULL,
        `size_id` int DEFAULT NULL,
        `price` decimal(10, 2) NOT NULL DEFAULT '0.00',
        `inv_amount` int NOT NULL DEFAULT '1',
        `img_url` text,
        `disc_price` decimal(10, 2) DEFAULT NULL,
        `disc_end_date` date DEFAULT NULL,
        PRIMARY KEY (`prod_var_id`),
        KEY `prod_var_prod_fk` (`product_id`),
        KEY `prod_var_color_fk` (`color_id`),
        KEY `prod_var_size_fk` (`size_id`),
        CONSTRAINT `prod_var_color_fk` FOREIGN KEY (`color_id`) REFERENCES `color` (`color_id`),
        CONSTRAINT `prod_var_prod_fk` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`),
        CONSTRAINT `prod_var_size_fk` FOREIGN KEY (`size_id`) REFERENCES `size` (`size_id`)
    )

CREATE TABLE
    `vendor_product` (
        `vendor_prod_id` int NOT NULL AUTO_INCREMENT,
        `user_id` int NOT NULL,
        `prod_var_id` int NOT NULL,
        PRIMARY KEY (`vendor_prod_id`),
        KEY `vend_prod_user_fk` (`user_id`),
        KEY `vend_prod_prod_var_fk_idx` (`prod_var_id`),
        CONSTRAINT `vend_prod_prod_var_fk` FOREIGN KEY (`prod_var_id`) REFERENCES `product_variant` (`prod_var_id`),
        CONSTRAINT `vend_prod_user_fk` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
    )

CREATE TABLE
    `cart` (
        `cart_id` int NOT NULL AUTO_INCREMENT,
        `user_id` int NOT NULL,
        `total_price` decimal(10, 2) NOT NULL DEFAULT '0.00',
        PRIMARY KEY (`cart_id`),
        KEY `cart_user_fk` (`user_id`),
        CONSTRAINT `cart_user_fk` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
    )

CREATE TABLE
    `cart_item` (
        `cart_item_id` int NOT NULL AUTO_INCREMENT,
        `cart_id` int NOT NULL,
        `prod_var_id` int NOT NULL,
        `quantity` int NOT NULL DEFAULT '1',
        `price` decimal(10, 2) NOT NULL,
        PRIMARY KEY (`cart_item_id`),
        KEY `cart_item_cart_fk` (`cart_id`),
        KEY `cart_item_prod_var_fk` (`prod_var_id`),
        CONSTRAINT `cart_item_cart_fk` FOREIGN KEY (`cart_id`) REFERENCES `cart` (`cart_id`),
        CONSTRAINT `cart_item_prod_var_fk` FOREIGN KEY (`prod_var_id`) REFERENCES `product_variant` (`prod_var_id`)
    )

CREATE TABLE
    `invoice` (
        `order_id` int NOT NULL AUTO_INCREMENT,
        `user_id` int NOT NULL,
        `order_date` date NOT NULL DEFAULT (curdate()),
        `total_price` decimal(10, 2) NOT NULL DEFAULT '0.00',
        `order_status` enum(
            'pending',
            'confirmed',
            'shipped'
        ) NOT NULL DEFAULT 'pending',
        PRIMARY KEY (`order_id`),
        KEY `orders_user_fk` (`user_id`),
        CONSTRAINT `orders_user_fk` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
    )

CREATE TABLE
    `sold_product` (
        `sold_prod_id` int NOT NULL AUTO_INCREMENT,
        `order_id` int NOT NULL,
        `prod_var_id` int NOT NULL,
        `quantity` int NOT NULL,
        `price` decimal(10, 2) NOT NULL,
        PRIMARY KEY (`sold_prod_id`),
        KEY `purch_item_order_fk` (`order_id`),
        KEY `purch_item_prod_var_fk` (`prod_var_id`),
        CONSTRAINT `purch_item_order_fk` FOREIGN KEY (`order_id`) REFERENCES `invoice` (`order_id`),
        CONSTRAINT `purch_item_prod_var_fk` FOREIGN KEY (`prod_var_id`) REFERENCES `product_variant` (`prod_var_id`)
    )

CREATE TABLE
    `chat` (
        `chat_id` int NOT NULL AUTO_INCREMENT,
        `customer_id` int NOT NULL,
        `representative_id` int NOT NULL,
        PRIMARY KEY (`chat_id`),
        KEY `chat_rep_fk` (`representative_id`),
        KEY `chat_user_fk` (`customer_id`),
        CONSTRAINT `chat_rep_fk` FOREIGN KEY (`representative_id`) REFERENCES `user` (`user_id`),
        CONSTRAINT `chat_user_fk` FOREIGN KEY (`customer_id`) REFERENCES `user` (`user_id`)
    )

CREATE TABLE
    `message` (
        `message_id` int NOT NULL AUTO_INCREMENT,
        `chat_id` int NOT NULL,
        `sender_id` int NOT NULL,
        `msg_text` text NOT NULL,
        `msg_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (`message_id`),
        KEY `msg_chat_fk_idx` (`chat_id`),
        KEY `msg_sender_fk_idx` (`sender_id`),
        CONSTRAINT `msg_chat_fk` FOREIGN KEY (`chat_id`) REFERENCES `chat` (`chat_id`),
        CONSTRAINT `msg_sender_fk` FOREIGN KEY (`sender_id`) REFERENCES `user` (`user_id`)
    )

CREATE TABLE
    `dispute` (
        `dispute_id` int NOT NULL AUTO_INCREMENT,
        `dispute_customer` int NOT NULL,
        `dispute_admin` int NOT NULL,
        `chat_id` int NOT NULL,
        `order_id` int NOT NULL,
        `sold_prod_id` int NOT NULL,
        `request` enum('return', 'exchange') NOT NULL,
        `description` text NOT NULL,
        `dispute_date` date NOT NULL DEFAULT (curdate()),
        `dispute_status` enum(
            'pending',
            'rejected',
            'confirmed',
            'processing',
            'complete'
        ) NOT NULL DEFAULT 'pending',
        PRIMARY KEY (`dispute_id`),
        KEY `dispute_cust_fk` (`dispute_customer`),
        KEY `dispute_admin_fk` (`dispute_admin`),
        KEY `dispute_order_fk` (`order_id`),
        KEY `dispute_sold_prod_fk` (`sold_prod_id`),
        KEY `dispute_chat_fk_idx` (`chat_id`),
        CONSTRAINT `dispute_admin_fk` FOREIGN KEY (`dispute_admin`) REFERENCES `user` (`user_id`),
        CONSTRAINT `dispute_chat_fk` FOREIGN KEY (`chat_id`) REFERENCES `chat` (`chat_id`),
        CONSTRAINT `dispute_cust_fk` FOREIGN KEY (`dispute_customer`) REFERENCES `user` (`user_id`),
        CONSTRAINT `dispute_order_fk` FOREIGN KEY (`order_id`) REFERENCES `invoice` (`order_id`),
        CONSTRAINT `dispute_sold_prod_fk` FOREIGN KEY (`sold_prod_id`) REFERENCES `sold_product` (`sold_prod_id`)
    )

INSERT INTO role (role_name) VALUES ('admin', 'customer', 'representative');
