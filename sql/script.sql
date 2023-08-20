-- phpMyAdmin SQL Dump
-- version 5.1.1deb5ubuntu1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Aug 19, 2023 at 04:02 AM
-- Server version: 8.0.34-0ubuntu0.22.04.1
-- PHP Version: 8.1.2-1ubuntu2.13

START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `baseballstats`
--

-- --------------------------------------------------------

--
-- Table structure for table `blocking_ips_game`
--

CREATE TABLE `blocking_ips_game` (
  `id` varchar(100) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `game_url` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `hitting`
--

CREATE TABLE `hitting` (
  `id` int NOT NULL,
  `GameDate` date DEFAULT NULL,
  `Date` varchar(100) DEFAULT NULL,
  `HomeTeam` varchar(100) DEFAULT NULL,
  `AwayTeam` varchar(100) DEFAULT NULL,
  `HomeScore` varchar(100) DEFAULT NULL,
  `AwayScore` varchar(100) DEFAULT NULL,
  `GameURL` varchar(300) DEFAULT NULL,
  `Batting` varchar(100) DEFAULT NULL,
  `AB` varchar(100) DEFAULT NULL,
  `R` varchar(100) DEFAULT NULL,
  `H` varchar(100) DEFAULT NULL,
  `RBI` varchar(100) DEFAULT NULL,
  `BB` varchar(100) DEFAULT NULL,
  `SO` varchar(100) DEFAULT NULL,
  `PA` varchar(100) DEFAULT NULL,
  `BA` varchar(100) DEFAULT NULL,
  `OBP` varchar(100) DEFAULT NULL,
  `SLG` varchar(100) DEFAULT NULL,
  `OPS` varchar(100) DEFAULT NULL,
  `Pit` varchar(100) DEFAULT NULL,
  `Str` varchar(100) DEFAULT NULL,
  `WPA` varchar(100) DEFAULT NULL,
  `aLI` varchar(100) DEFAULT NULL,
  `WPA+` varchar(100) DEFAULT NULL,
  `WPA-` varchar(100) DEFAULT NULL,
  `cWPA` varchar(100) DEFAULT NULL,
  `acLI` varchar(100) DEFAULT NULL,
  `RE24` varchar(100) DEFAULT NULL,
  `PO` varchar(100) DEFAULT NULL,
  `A` varchar(100) DEFAULT NULL,
  `Details` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `pitching`
--

CREATE TABLE `pitching` (
  `id` int NOT NULL,
  `GameDate` date DEFAULT NULL,
  `Date` varchar(100) DEFAULT NULL,
  `HomeTeam` varchar(100) DEFAULT NULL,
  `AwayTeam` varchar(100) DEFAULT NULL,
  `HomeScore` varchar(100) DEFAULT NULL,
  `AwayScore` varchar(100) DEFAULT NULL,
  `GameURL` varchar(300) DEFAULT NULL,
  `Pitching` varchar(100) DEFAULT NULL,
  `IP` varchar(100) DEFAULT NULL,
  `H` varchar(100) DEFAULT NULL,
  `R` varchar(100) DEFAULT NULL,
  `ER` varchar(100) DEFAULT NULL,
  `BB` varchar(100) DEFAULT NULL,
  `SO` varchar(100) DEFAULT NULL,
  `HR` varchar(100) DEFAULT NULL,
  `ERA` varchar(100) DEFAULT NULL,
  `BF` varchar(100) DEFAULT NULL,
  `Pit` varchar(100) DEFAULT NULL,
  `Str` varchar(100) DEFAULT NULL,
  `Ctct` varchar(100) DEFAULT NULL,
  `StS` varchar(100) DEFAULT NULL,
  `StL` varchar(100) DEFAULT NULL,
  `GB` varchar(100) DEFAULT NULL,
  `FB` varchar(100) DEFAULT NULL,
  `LD` varchar(100) DEFAULT NULL,
  `Unk` varchar(100) DEFAULT NULL,
  `GSc` varchar(100) DEFAULT NULL,
  `IR` varchar(100) DEFAULT NULL,
  `IS` varchar(100) DEFAULT NULL,
  `WPA` varchar(100) DEFAULT NULL,
  `aLI` varchar(100) DEFAULT NULL,
  `cWPA` varchar(100) DEFAULT NULL,
  `acLI` varchar(100) DEFAULT NULL,
  `RE24` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `hitting`
--
ALTER TABLE `hitting`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `pitching`
--
ALTER TABLE `pitching`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `hitting`
--
ALTER TABLE `hitting`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `pitching`
--
ALTER TABLE `pitching`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
