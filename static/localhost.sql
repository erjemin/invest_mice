-- phpMyAdmin SQL Dump
-- version 3.4.10.1deb1
-- http://www.phpmyadmin.net
--
-- Хост: localhost
-- Время создания: Мар 04 2013 г., 22:38
-- Версия сервера: 5.5.29
-- Версия PHP: 5.3.10-1ubuntu3.5

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- База данных: `db_stocks`
--
CREATE DATABASE `db_stocks` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `db_stocks`;

-- --------------------------------------------------------

--
-- Структура таблицы `tbIndexName`
--

CREATE TABLE IF NOT EXISTS `tbIndexName` (
  `szTICKER` char(16) NOT NULL COMMENT 'Название тикера',
  `szTICKERfullnameRU` varchar(128) NOT NULL DEFAULT 'I do not understand that... Garbage some...' COMMENT 'Полное наименование Тикера на русском',
  `szTICKERfullnameEN` varchar(128) NOT NULL DEFAULT 'I do not understand that... Garbage some...' COMMENT 'Полное наименование Тикера на английском',
  `szPathForParsing` varchar(128) DEFAULT NULL COMMENT 'Базовый путь для парсинга тикра из базы данных РБК',
  PRIMARY KEY (`szTICKER`),
  UNIQUE KEY `szTICKER` (`szTICKER`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `tbIndexName`
--

INSERT INTO `tbIndexName` (`szTICKER`, `szTICKERfullnameRU`, `szTICKERfullnameEN`, `szPathForParsing`) VALUES
('AEX', 'Индекс фондовой биржи Нидерландов', 'Amsterdam Exchange index', '/free/index.0/free.fcgi?'),
('ASE', 'Греческая фондовая биржа', 'Greece General Share', '/free/index.0/free.fcgi?'),
('ASX', 'Австралийская фондовая биржа', 'Australian Securities Exchange', '/free/index.0/free.fcgi?'),
('ATX', 'Фондовый индекс Австрии', 'Austrian Traded Index', '/free/index.0/free.fcgi?'),
('BSE', 'Индкс бомбейской фондовой биржи', 'The Bombay Stock Exchange Limited', '/free/index.0/free.fcgi?'),
('BUSP', 'Бразильская фондовая биржа Сан-Паулу', 'Bolsa de Valores de São Paulo', '/free/index.0/free.fcgi?'),
('BUX', 'Будапештская фондовая биржа', 'Budapesti Értéktőzsde', '/free/index.0/free.fcgi?'),
('CAC', 'Фондовый индекс Франции (CAC-40)', 'Cotation Assistée en Continu', '/free/index.0/free.fcgi?'),
('DAX', 'Фондовый индекс Германии', 'Deutscher Aktienindex', '/free/index.0/free.fcgi?'),
('DJI', 'Промышленный индекс Доу-Джонса (США)', 'Dow Jones Industrial Average', '/free/index.0/free.fcgi?'),
('FTSE', 'Индекс лондонской фондовой биржи', 'Financial Times Stock Exchange Index', '/free/index.0/free.fcgi?'),
('FUX', 'Ценные бумаги Казначейства США (5-Year Note)', 'Treasury 5-Year Note', '/free/index.0/free.fcgi?'),
('HSI', 'Индекс Гонконгской биржи', 'Hong Kong Hang Seng', '/free/index.0/free.fcgi?'),
('IGBM', 'Madrid Stock Exchange General Index (Spain)', 'Madrid Stock Exchange General Index (Spain)', '/free/index.0/free.fcgi?'),
('IPC', 'Индекс Мексиканской фондовой биржи', 'Índice de Precios y Cotizaciones', '/free/index.0/free.fcgi?'),
('IPSA', 'Фондовая биржа Сантьяго (Чили)', 'Bolsa de Comercio de Santiago (Chili)', '/free/index.0/free.fcgi?'),
('IPX', 'Ценные бумаги Казначейства США (13-Week Bill)', 'Treasury 13-Week Bill', '/free/index.0/free.fcgi?'),
('JKSE', 'Фондовая биржа Джакарты (Индонезия)', 'JSX Composite (Indonesia)', '/free/index.0/free.fcgi?'),
('JSE', 'Йоханнесбургская фондовая биржа', 'Johannesburg Stock Exchange', '/free/index.0/free.fcgi?'),
('KLSE', 'KLSE (Малайзия)', 'Kuala Lumpur Stock Exchange', '/free/index.0/free.fcgi?'),
('KS11', 'I do not understand that... Garbage some...', 'KOSPI (Korea Composite Stock Price Index)', '/free/index.0/free.fcgi?'),
('MERVAL', 'Фондовая биржа Буэнос-Айреса (Аргентина)', 'Bolsa de Comercio de Buenos Aires', '/free/index.0/free.fcgi?'),
('MICEX', 'Индекс ММВБ', 'MICEX Index ', '/free/index.0/free.fcgi?'),
('MICEX10INDEX', '', 'MICEX 10 Index', '/free/rusindex.0/free.fcgi?'),
('MICEXBNDPRCI', '', 'The MICEX index - Russian corporate bonds ', '/free/rusindex.0/free.fcgi?'),
('MICEXCBICP', '', 'The index of corporate bonds on MICEX (net price) ', '/free/rusindex.0/free.fcgi?'),
('MICEXCBICP3Y', '', 'The index of corporate bonds on MICEX (net price) 1-3 years ', '/free/rusindex.0/free.fcgi?'),
('MICEXCBICP5Y', '', 'The index of corporate bonds on MICEX (net price) 3-5 years ', '/free/rusindex.0/free.fcgi?'),
('MICEXCBIGP', '', 'The index of corporate bonds on MICEX (gross) ', '/free/rusindex.0/free.fcgi?'),
('MICEXCBIGP3Y', '', 'The index of corporate bonds on MICEX (gross) 1-3 years ', '/free/rusindex.0/free.fcgi?'),
('MICEXCBIGP5Y', '', 'The index of corporate bonds on MICEX (gross) 3-5 years ', '/free/rusindex.0/free.fcgi?'),
('MICEXCBITR', '', 'The index of corporate bonds on MICEX (total return)', '/free/rusindex.0/free.fcgi?'),
('MICEXCBITR3Y', '', 'The index of corporate bonds on MICEX (total return) 1-3 years', '/free/rusindex.0/free.fcgi?'),
('MICEXCBITR5Y', '', 'The index of corporate bonds on MICEX (total return) 3-5 years', '/free/rusindex.0/free.fcgi?'),
('MICEXCGS', '', 'The MICEX index - consumer sector ', '/free/rusindex.0/free.fcgi?'),
('MICEXCHM', '', 'The MICEX index - chemicals and petrochemicals ', '/free/rusindex.0/free.fcgi?'),
('MICEXFNL', '', 'The MICEX index - finance', '/free/rusindex.0/free.fcgi?'),
('MICEXINDEXCF', '', 'MICEX Index ', '/free/rusindex.0/free.fcgi?'),
('MICEXLC', '', 'MICEX Index - large-cap companies ', '/free/rusindex.0/free.fcgi?'),
('MICEXMANDM', '', 'MICEX Index - metallurgy ', '/free/rusindex.0/free.fcgi?'),
('MICEXMBICP', '', 'Index municipal reg. MICEX (price)', '/free/rusindex.0/free.fcgi?'),
('MICEXMBIGP', '', 'Index municipal reg. MICEX (gross)', '/free/rusindex.0/free.fcgi?'),
('MICEXMBITR', '', 'Index municipal reg. MICEX (total return)', '/free/rusindex.0/free.fcgi?'),
('MICEXMC', '', 'The MICEX index - the standard of capitalization ', '/free/rusindex.0/free.fcgi?'),
('MICEXMNF', '', 'MICEX Index - mechanical engineering ', '/free/rusindex.0/free.fcgi?'),
('MICEXOANDG', '', 'MICEX Index - oil & gas', '/free/rusindex.0/free.fcgi?'),
('MICEXPWR', '', 'MICEX Index - energy', '/free/rusindex.0/free.fcgi?'),
('MICEXSC', '', 'The MICEX index - the base of the company capitalization ', '/free/rusindex.0/free.fcgi?'),
('MICEXTLC', '', 'MICEX Index - Telecoms ', '/free/rusindex.0/free.fcgi?'),
('NASD', 'Nasdaq Composite', 'Nasdaq Composite', '/free/index.0/free.fcgi?'),
('NDX', 'Nasdaq 100', 'Nasdaq 100', '/free/index.0/free.fcgi?'),
('NIKKEI', 'Никей 225', ' Nikkei 225', '/free/index.0/free.fcgi?'),
('NYA', 'NYSE', 'NYSE Composite', '/free/index.0/free.fcgi?'),
('PFTS', 'PFTS index (Украина)', 'PFTS index (Ukraine)', '/free/index.0/free.fcgi?'),
('PX50', 'Пражская фондовая биржа (Чехия)', 'Prague Stock Exchange ', '/free/index.0/free.fcgi?'),
('RGBI', '', 'The index of government bonds in Russia (MICEX) ', '/free/rusindex.0/free.fcgi?'),
('RGBIG', '', 'Russia Government Bond Index (gross) MICEX ', '/free/rusindex.0/free.fcgi?'),
('RGBITR', '', 'Russia Government Bond Index (total return) MICEX ', '/free/rusindex.0/free.fcgi?'),
('RTS2', '', 'RTS - second-tier stocks, RTS-2 ', '/free/rts.1/free.fcgi?'),
('RTScr', '', 'RTS Index - consumer goods & retail', '/free/rts.1/free.fcgi?'),
('RTSeu', '', 'RTS Index - electric utilities', '/free/rts.1/free.fcgi?'),
('RTSfn', '', 'RTS Index - financials', '/free/rts.1/free.fcgi?'),
('RTSI', '', 'RTS Index ', '/free/index.0/free.fcgi?'),
('RTSin', '', 'RTS Index - industrial', '/free/rts.1/free.fcgi?'),
('RTSmm', '', 'RTS Index - metals & mining', '/free/rts.1/free.fcgi?'),
('RTSog', '', 'RTS Index - oil & gas', '/free/rts.1/free.fcgi?'),
('RTSSIB', '', 'RTS Index - Siberia', '/free/rts.1/free.fcgi?'),
('RTSSTD', '', 'Index RTS - Standard ', '/free/rusindex.0/free.fcgi?'),
('RTStl', '', 'RTS - Telecom ', '/free/rts.1/free.fcgi?'),
('RU10D', 'RU10D', 'DJ RusIndex Titans 10 USD', '/free/index.0/free.fcgi?'),
('RU10R', 'RU10R', 'DJ RusIndex Titans 10 Ruble (USA)', '/free/index.0/free.fcgi?'),
('SPX', 'Standard & Poor''s 500 (S&P 500)', 'Standard & Poor''s 500 (S&P 500)', '/free/index.0/free.fcgi?'),
('SSEC', 'Индекс шанхайской фондовой биржа (Китай)', 'Shanghai Stock Exchange Composite (China)', '/free/index.0/free.fcgi?'),
('SSMI', 'Swiss Market Index (SMI)', 'Swiss Market Index (SMI)', '/free/index.0/free.fcgi?'),
('STI', 'Straits Times Index (Singapore)', 'Straits Times Index (Singapore)', '/free/index.0/free.fcgi?'),
('TA100', 'Тель-Авив 100', 'Tel Aviv 100', '/free/index.0/free.fcgi?'),
('TECHIND', '', 'Technical Index (MICEX) ', '/free/rusindex.0/free.fcgi?'),
('TECHINDBOND', '', 'Technical Bond Index (MICEX) ', '/free/rusindex.0/free.fcgi?'),
('TECHINDSHARE', '', 'Technical index of shares (MICEX)', '/free/rusindex.0/free.fcgi?'),
('TNX', 'Treasury 10-Year Note', 'Ценные бумаги Казначейства США (10-Year Note_', '/free/index.0/free.fcgi?'),
('TSE', 'Фондовая биржа Торонто (Канада)', 'Toronto Stock Exchange (Canada)', '/free/index.0/free.fcgi?'),
('TYX', 'Ценные бумаги Казначейства США (30-Year Bond)', 'Treasury 30-Year Bond', '/free/index.0/free.fcgi?'),
('USD000000TOD', 'Курс ЦБ RUB/USD сегодня', 'RUB/USD Today', '/free/selt.0/free.fcgi?'),
('XU100', 'ISE-100 Index (Турция)', 'Istanbul Stock Exchange 100 (Turkey)', '/free/index.0/free.fcgi?');

-- --------------------------------------------------------

--
-- Структура таблицы `tbIndexValue`
--

CREATE TABLE IF NOT EXISTS `tbIndexValue` (
  `szTICKER` varchar(16) NOT NULL COMMENT 'Краткая запись тиккера',
  `tmDATE` datetime NOT NULL COMMENT 'Дата',
  `fOPEN` double DEFAULT '0' COMMENT 'Цена открытия',
  `fHIGH` double DEFAULT '0' COMMENT 'Максимальная цена',
  `fLOW` double DEFAULT '0' COMMENT 'Минимальная цена',
  `fCLOSE` double DEFAULT '0' COMMENT 'Цена закрытия',
  `fOPENpercent` double NOT NULL DEFAULT '0',
  `fHIGHpercent` double NOT NULL DEFAULT '0',
  `fLOWpercent` double NOT NULL DEFAULT '0',
  `fCLOSEpercent` double NOT NULL DEFAULT '0',
  KEY `szTICKER` (`szTICKER`),
  KEY `tmDATE` (`tmDATE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=136;

