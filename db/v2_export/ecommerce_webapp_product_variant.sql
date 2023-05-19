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

-- Table structure for table `product_variant`

--

DROP TABLE IF EXISTS `product_variant`;

/*!40101 SET @saved_cs_client     = @@character_set_client */

;

/*!50503 SET character_set_client = utf8mb4 */

;

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