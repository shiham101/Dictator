-- MySQL dump 10.13  Distrib 5.7.15, for Linux (x86_64)
--
-- Host: localhost    Database: nmapscan
-- ------------------------------------------------------
-- Server version	5.7.15

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `IPbackup`
--

DROP TABLE IF EXISTS `IPbackup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `IPbackup` (
  `id` int(11) NOT NULL DEFAULT '0',
  `IPs` text,
  `PORTs` varchar(1000) CHARACTER SET utf8 NOT NULL DEFAULT '--',
  `status` varchar(500) CHARACTER SET utf8 NOT NULL DEFAULT 'Incomplete',
  `project` int(11) DEFAULT NULL,
  `Sevices_detected` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `IPexploits`
--

DROP TABLE IF EXISTS `IPexploits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `IPexploits` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Pid` int(11) NOT NULL,
  `Host` varchar(100) DEFAULT NULL,
  `Port` varchar(100) DEFAULT NULL,
  `Service` varchar(100) DEFAULT NULL,
  `project_status` varchar(30) DEFAULT NULL,
  `Exploits` json DEFAULT NULL,
  `service_type` varchar(100) DEFAULT NULL,
  `read_init_status` varchar(50) CHARACTER SET utf8 DEFAULT 'false',
  `read_final_status` varchar(50) CHARACTER SET utf8 DEFAULT 'false',
  `State` varchar(20) CHARACTER SET utf8 DEFAULT 'Open',
  `Version` varchar(100) CHARACTER SET utf8 DEFAULT '',
  `test_case_executed` varchar(20) CHARACTER SET utf8 DEFAULT 'false',
  PRIMARY KEY (`id`),
  KEY `fk_exploits` (`Pid`),
  CONSTRAINT `IPexploits_ibfk_1` FOREIGN KEY (`Pid`) REFERENCES `project` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20894 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `IPtable`
--

DROP TABLE IF EXISTS `IPtable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `IPtable` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `IPs` text,
  `PORTs` varchar(1000) CHARACTER SET utf8 NOT NULL DEFAULT '--',
  `status` varchar(500) CHARACTER SET utf8 NOT NULL DEFAULT 'Incomplete',
  `project` int(11) DEFAULT NULL,
  `Sevices_detected` text,
  PRIMARY KEY (`id`),
  KEY `IP_FK` (`project`),
  CONSTRAINT `IP_FK` FOREIGN KEY (`project`) REFERENCES `project` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2537 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `IPtable_history`
--

DROP TABLE IF EXISTS `IPtable_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `IPtable_history` (
  `id` int(11) NOT NULL DEFAULT '0',
  `IPs` text,
  `PORTs` varchar(1000) CHARACTER SET utf8 NOT NULL DEFAULT '--',
  `status` varchar(500) CHARACTER SET utf8 NOT NULL DEFAULT 'Incomplete',
  `project` int(11) DEFAULT NULL,
  `Sevices_detected` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Scan_Profiles`
--

DROP TABLE IF EXISTS `Scan_Profiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Scan_Profiles` (
  `p_id` int(11) NOT NULL AUTO_INCREMENT,
  `u_id` varchar(200) CHARACTER SET utf8 DEFAULT NULL,
  `p_name` varchar(300) CHARACTER SET utf8 NOT NULL,
  `p_catagory` varchar(200) CHARACTER SET utf8 DEFAULT 'Custom',
  `p_path` varchar(300) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`p_id`),
  UNIQUE KEY `p_name` (`p_name`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(50) CHARACTER SET utf8 NOT NULL,
  `user_password` varchar(200) CHARACTER SET utf8 DEFAULT NULL,
  `user_salt` varchar(200) CHARACTER SET utf8 DEFAULT NULL,
  `user_role` int(11) NOT NULL,
  `user_email` varchar(100) CHARACTER SET utf8 NOT NULL,
  `user_phone` varchar(10) CHARACTER SET utf8 NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `application_auth`
--

DROP TABLE IF EXISTS `application_auth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `application_auth` (
  `app_id` int(11) NOT NULL AUTO_INCREMENT,
  `app_type` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `app_key` varchar(100) CHARACTER SET utf8 DEFAULT '',
  PRIMARY KEY (`app_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `exploit_cve_mapping`
--

DROP TABLE IF EXISTS `exploit_cve_mapping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exploit_cve_mapping` (
  `QID` mediumtext NOT NULL,
  `EXPLOIT_SRC_NAME` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `EXPLOIT_REF` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `EXPLOIT_DESC` varchar(300) CHARACTER SET utf8 DEFAULT NULL,
  `EXPLOIT_LINK` varchar(100) CHARACTER SET utf8 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `exploit_cve_mapping_metasploit`
--

DROP TABLE IF EXISTS `exploit_cve_mapping_metasploit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exploit_cve_mapping_metasploit` (
  `id` int(11) DEFAULT NULL,
  `mtype` varchar(255) DEFAULT NULL,
  `fullname` longtext,
  `name` longtext
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `exploit_cve_mapping_metasploit_recent`
--

DROP TABLE IF EXISTS `exploit_cve_mapping_metasploit_recent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exploit_cve_mapping_metasploit_recent` (
  `id` int(11) DEFAULT NULL,
  `mtype` varchar(255) DEFAULT NULL,
  `fullname` longtext,
  `name` longtext
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `exploit_cve_mapping_recent`
--

DROP TABLE IF EXISTS `exploit_cve_mapping_recent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exploit_cve_mapping_recent` (
  `QID` mediumtext NOT NULL,
  `EXPLOIT_SRC_NAME` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `EXPLOIT_REF` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `EXPLOIT_DESC` varchar(300) CHARACTER SET utf8 DEFAULT NULL,
  `EXPLOIT_LINK` varchar(100) CHARACTER SET utf8 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `exploit_mapping_metasploit`
--

DROP TABLE IF EXISTS `exploit_mapping_metasploit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exploit_mapping_metasploit` (
  `id` int(11) DEFAULT NULL,
  `mtype` varchar(255) DEFAULT NULL,
  `fullname` longtext,
  `name` longtext
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ipbackup`
--

DROP TABLE IF EXISTS `ipbackup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ipbackup` (
  `id` int(11) NOT NULL DEFAULT '0',
  `IPs` text,
  `PORTs` varchar(1000) CHARACTER SET utf8 NOT NULL DEFAULT '--',
  `status` varchar(500) CHARACTER SET utf8 NOT NULL DEFAULT 'Incomplete',
  `project` int(11) DEFAULT NULL,
  `Sevices_detected` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mapping_table`
--

DROP TABLE IF EXISTS `mapping_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mapping_table` (
  `app_id` varchar(200) CHARACTER SET utf8 DEFAULT NULL,
  `project_id` varchar(200) CHARACTER SET utf8 DEFAULT NULL,
  `assessment_id` varchar(200) CHARACTER SET utf8 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `project`
--

DROP TABLE IF EXISTS `project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `project` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `projects` text,
  `IPrange` text,
  `project_status` varchar(50) CHARACTER SET utf8 DEFAULT 'incomplete',
  `Date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `port_range` varchar(500) CHARACTER SET utf8 DEFAULT NULL,
  `process_id` varchar(100) CHARACTER SET utf8 DEFAULT '-100',
  `exploits_process_id` varchar(200) CHARACTER SET utf8 DEFAULT '-100',
  `project_status_exploits` varchar(50) CHARACTER SET utf8 DEFAULT 'incomplete',
  `exploit_process_id_list` varchar(400) CHARACTER SET utf8 DEFAULT '100',
  `mode` varchar(30) CHARACTER SET utf8 DEFAULT 'sequential',
  `switch` varchar(100) CHARACTER SET utf8 DEFAULT '-T4 -A -n',
  `profile_id` int(11) DEFAULT '2',
  PRIMARY KEY (`id`),
  KEY `fk_profile` (`profile_id`)
) ENGINE=InnoDB AUTO_INCREMENT=729 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `project_user_mapping`
--

DROP TABLE IF EXISTS `project_user_mapping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `project_user_mapping` (
  `project_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  KEY `project_id` (`project_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `project_user_mapping_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `project` (`id`),
  CONSTRAINT `project_user_mapping_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `Users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rep`
--

DROP TABLE IF EXISTS `rep`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rep` (
  `Pid` int(11) NOT NULL,
  `Host` varchar(50) CHARACTER SET utf8 NOT NULL,
  `Source` varchar(20) CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `report_details`
--

DROP TABLE IF EXISTS `report_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `report_details` (
  `Pid` int(11) NOT NULL,
  `Host` varchar(50) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `Service` varchar(50) CHARACTER SET utf8 DEFAULT '',
  `Port` varchar(50) CHARACTER SET utf8 DEFAULT '',
  `host_name` varchar(50) CHARACTER SET utf8 DEFAULT '',
  `os` varchar(50) CHARACTER SET utf8 DEFAULT '',
  `system_type` varchar(50) CHARACTER SET utf8 DEFAULT '',
  `plugin_id` varchar(50) CHARACTER SET utf8 DEFAULT '',
  `severity` varchar(50) CHARACTER SET utf8 DEFAULT '',
  `protocol` varchar(50) CHARACTER SET utf8 DEFAULT '',
  `synopsis` blob,
  `description` blob,
  `solution` blob,
  `title` blob,
  `result` blob,
  `dignosis` blob,
  `Source` varchar(20) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `sub_type` varchar(30) CHARACTER SET utf8 DEFAULT '',
  `plugin_name` blob,
  `ref` blob,
  `cvss` blob,
  `risk_vec` blob,
  KEY `F_k` (`Pid`,`Host`,`Source`),
  CONSTRAINT `FK_PR` FOREIGN KEY (`Pid`) REFERENCES `project` (`id`),
  CONSTRAINT `F_k` FOREIGN KEY (`Pid`, `Host`, `Source`) REFERENCES `report_mapping` (`Pid`, `Host`, `Source`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `report_mapping`
--

DROP TABLE IF EXISTS `report_mapping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `report_mapping` (
  `Pid` int(11) NOT NULL,
  `Host` varchar(50) CHARACTER SET utf8 NOT NULL,
  `Source` varchar(20) CHARACTER SET utf8 NOT NULL,
  PRIMARY KEY (`Pid`,`Host`,`Source`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `roles` (
  `role_id` int(11) NOT NULL,
  `description` varchar(20) CHARACTER SET utf8 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sqlite_sequence`
--

DROP TABLE IF EXISTS `sqlite_sequence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sqlite_sequence` (
  `name` text,
  `seq` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `switches`
--

DROP TABLE IF EXISTS `switches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `switches` (
  `switch_id` int(11) NOT NULL AUTO_INCREMENT,
  `switch_name` varchar(200) CHARACTER SET utf8 DEFAULT NULL,
  `switch` varchar(200) CHARACTER SET utf8 DEFAULT NULL,
  `switch_catagory` varchar(100) CHARACTER SET utf8 DEFAULT 'general',
  PRIMARY KEY (`switch_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tab_test`
--

DROP TABLE IF EXISTS `tab_test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tab_test` (
  `name` varchar(20) CHARACTER SET utf8 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `test`
--

DROP TABLE IF EXISTS `test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `test` (
  `f1` int(11) DEFAULT NULL,
  `f2` varchar(10) DEFAULT NULL,
  `f3` varchar(10) DEFAULT NULL,
  `f4` varchar(10) DEFAULT NULL,
  `f5` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `test1`
--

DROP TABLE IF EXISTS `test1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `test1` (
  `val1` varchar(10) DEFAULT NULL,
  `val2` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `test2`
--

DROP TABLE IF EXISTS `test2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `test2` (
  `val1` varchar(10) DEFAULT NULL,
  `val2` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-07-12 13:18:34
