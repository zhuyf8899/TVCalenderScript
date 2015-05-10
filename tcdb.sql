-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- 主机: localhost
-- 生成日期: 2015-05-11 06:39:35
-- 服务器版本: 5.5.43-0ubuntu0.14.04.1
-- PHP 版本: 5.5.9-1ubuntu4.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 数据库: `tcdb`
--

-- --------------------------------------------------------

--
-- 表的结构 `config`
--

CREATE TABLE IF NOT EXISTS `config` (
  `c_id` int(100) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `c_name` varchar(255) NOT NULL COMMENT 'item name',
  `c_value` mediumtext NOT NULL,
  PRIMARY KEY (`c_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

--
-- 表的结构 `episode`
--

CREATE TABLE IF NOT EXISTS `episode` (
  `e_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `n_id` int(10) NOT NULL COMMENT 'name s id',
  `e_season` int(10) NOT NULL,
  `e_episode` int(10) NOT NULL,
  `e_name` varchar(255) DEFAULT NULL,
  `e_onAir` datetime DEFAULT NULL,
  `e_description` text,
  PRIMARY KEY (`e_id`,`n_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=8 ;

--
-- 触发器 `episode`
--
DROP TRIGGER IF EXISTS `tri_insertProtect`;
DELIMITER //
CREATE TRIGGER `tri_insertProtect` BEFORE INSERT ON `episode`
 FOR EACH ROW begin
DECLARE rows INT DEFAULT 0;
SELECT count(*) FROM episode where n_id = NEW.n_id and e_season = NEW.e_season and e_episode = NEW.e_episode and e_onAir = NEW.e_onAir INTO rows;
IF rows>0 THEN
SIGNAL sqlstate '45001' set message_text="The table has already have a same row";
end if;
end
//
DELIMITER ;

-- --------------------------------------------------------

--
-- 表的结构 `name`
--

CREATE TABLE IF NOT EXISTS `name` (
  `n_id` int(8) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `n_name` varchar(255) NOT NULL COMMENT 'a tv series name, unique',
  `n_photoLink` varchar(4096) DEFAULT NULL COMMENT 'a photo link when possible',
  PRIMARY KEY (`n_id`),
  UNIQUE KEY `n_name` (`n_name`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=8 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
