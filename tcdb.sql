-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- 主机: localhost
-- 生成日期: 2016-01-13 11:07:49
-- 服务器版本: 5.5.46-0ubuntu0.14.04.2
-- PHP 版本: 5.5.9-1ubuntu4.14

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
-- 创建时间: 2016-01-11 06:33:36
--

CREATE TABLE IF NOT EXISTS `config` (
  `c_id` int(100) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `c_name` varchar(255) NOT NULL COMMENT 'item name',
  `c_value` mediumtext NOT NULL,
  PRIMARY KEY (`c_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

-- --------------------------------------------------------

--
-- 表的结构 `episode`
--
-- 创建时间: 2016-01-13 02:48:09
--

CREATE TABLE IF NOT EXISTS `episode` (
  `e_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `n_id` int(10) NOT NULL COMMENT 'name s id',
  `e_season` int(10) NOT NULL,
  `e_episode` int(10) NOT NULL,
  `e_name` varchar(255) DEFAULT NULL,
  `e_onAir` date DEFAULT NULL,
  `e_description` text,
  PRIMARY KEY (`e_id`,`n_id`),
  KEY `FK_episode_TO_name` (`n_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1190 ;

--
-- 表的关联 `episode`:
--   `n_id`
--       `name` -> `n_id`
--

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
-- 创建时间: 2016-01-11 06:33:36
--

CREATE TABLE IF NOT EXISTS `name` (
  `n_id` int(8) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `n_name` varchar(255) NOT NULL COMMENT 'a tv series name, unique',
  `n_photoLink` varchar(4096) DEFAULT NULL COMMENT 'a photo link when possible',
  PRIMARY KEY (`n_id`),
  UNIQUE KEY `n_name` (`n_name`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1190 ;

-- --------------------------------------------------------

--
-- 表的结构 `nameInfo`
--
-- 创建时间: 2016-01-13 02:48:59
--

CREATE TABLE IF NOT EXISTS `nameInfo` (
  `n_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '与n_id一致的主键',
  `name_chinese` varchar(255) DEFAULT NULL COMMENT '剧集中文翻译',
  `name_description` text COMMENT '剧情介绍',
  `name_year` year(4) DEFAULT NULL COMMENT '上映年（最早）',
  PRIMARY KEY (`n_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- 表的关联 `nameInfo`:
--   `n_id`
--       `name` -> `n_id`
--

-- --------------------------------------------------------

--
-- 表的结构 `season`
--
-- 创建时间: 2016-01-13 03:07:21
--

CREATE TABLE IF NOT EXISTS `season` (
  `n_id` int(11) NOT NULL COMMENT '与n_id一致的主键',
  `season` int(11) NOT NULL COMMENT '季',
  `s_description` text COMMENT '季介绍',
  `s_year` year(4) DEFAULT NULL COMMENT '上映年',
  `s_photolink` varchar(2038) DEFAULT NULL,
  PRIMARY KEY (`n_id`,`season`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 限制导出的表
--

--
-- 限制表 `episode`
--
ALTER TABLE `episode`
  ADD CONSTRAINT `FK_episode_TO_name` FOREIGN KEY (`n_id`) REFERENCES `name` (`n_id`);

--
-- 限制表 `nameInfo`
--
ALTER TABLE `nameInfo`
  ADD CONSTRAINT `FK_nameInfo_TO_name` FOREIGN KEY (`n_id`) REFERENCES `name` (`n_id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
