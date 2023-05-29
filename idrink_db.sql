-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: May 29, 2023 at 02:41 AM
-- Server version: 8.0.33-0ubuntu0.20.04.2
-- PHP Version: 7.4.3-4ubuntu2.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `idrink_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `idorder` int NOT NULL,
  `drink` varchar(20) DEFAULT NULL,
  `user` varchar(20) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`idorder`, `drink`, `user`, `created_at`) VALUES
(1, 'tequila_sunrise', 'client1', NULL),
(2, 'desarmador', 'client1', NULL),
(3, 'greyhound', 'client1', NULL),
(4, 'cosmopolitan', 'client1', NULL),
(5, 'desarmador', 'client2', NULL),
(6, 'desarmador', 'client2', NULL),
(7, 'desarmador', 'client2', NULL),
(8, 'desarmador', 'client2', NULL),
(9, 'desarmador', 'client2', NULL),
(10, 'desarmador', 'admin', NULL),
(11, 'cosmopolitan', 'admin', NULL),
(12, 'desarmador', 'admin', NULL),
(13, 'cosmopolitan', 'admin', NULL),
(14, 'desarmador', 'admin', NULL),
(15, 'tequila_sunrise', 'admin', NULL),
(16, 'cosmopolitan', 'admin', NULL),
(17, 'cosmopolitan', 'admin', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `status`
--

CREATE TABLE `status` (
  `id` int NOT NULL,
  `bottle1` varchar(100) DEFAULT NULL,
  `bottle2` varchar(100) DEFAULT NULL,
  `bottle3` varchar(100) DEFAULT NULL,
  `bottle4` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `status`
--

INSERT INTO `status` (`id`, `bottle1`, `bottle2`, `bottle3`, `bottle4`, `created_at`) VALUES
(1, '123.2', '122.12', '1243.2', '1234.1', '2023-05-16 06:45:58');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `full_name` varchar(300) DEFAULT NULL,
  `disabled` int DEFAULT '1',
  `password` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `email`, `full_name`, `disabled`, `password`) VALUES
(1, 'admin', 'admin admin admin', 1, 'admin'),
(2, 'client1', 'client1', 1, 'client1'),
(3, 'client2', 'client2', 1, 'client2');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`idorder`);

--
-- Indexes for table `status`
--
ALTER TABLE `status`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `idorder` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `status`
--
ALTER TABLE `status`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
