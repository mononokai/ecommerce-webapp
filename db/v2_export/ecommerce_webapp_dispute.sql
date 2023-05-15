-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)

--

-- Host: 127.0.0.1    Database: ecommerce_webapp

-- ------------------------------------------------------

-- Server version	8.0.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */

;

/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */

;

/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */

;

/*!50503 SET NAMES utf8 */

;

/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */

;

/*!40103 SET TIME_ZONE='+00:00' */

;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */

;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */

;

/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */

;

/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */

;

--

-- Table structure for table `dispute`

--

DROP TABLE IF EXISTS `dispute`;

/*!40101 SET @saved_cs_client     = @@character_set_client */

;

/*!50503 SET character_set_client = utf8mb4 */

;

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
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

/*!40101 SET character_set_client = @saved_cs_client */

;

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */

;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */

;

/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */

;

/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */

;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */

;

/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */

;

/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */

;

/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */

;

-- Dump completed on 2023-05-15  0:21:50