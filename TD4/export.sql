-- Adminer 4.2.5 MySQL dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

DROP TABLE IF EXISTS `Administration`;
CREATE TABLE `Administration` (
  `id_infirmier` int(10) unsigned NOT NULL,
  `IPP` int(10) unsigned NOT NULL,
  `cip` int(10) unsigned NOT NULL,
  `date_heure_administration` datetime NOT NULL,
  PRIMARY KEY (`id_infirmier`,`IPP`,`cip`),
  KEY `IPP` (`IPP`),
  KEY `cip` (`cip`),
  CONSTRAINT `Administration_ibfk_1` FOREIGN KEY (`id_infirmier`) REFERENCES `Infirmier` (`ADELI`),
  CONSTRAINT `Administration_ibfk_2` FOREIGN KEY (`IPP`) REFERENCES `Patient` (`IPP`),
  CONSTRAINT `Administration_ibfk_3` FOREIGN KEY (`cip`) REFERENCES `Medicament` (`cip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `ATC1`;
CREATE TABLE `ATC1` (
  `code_ATC1` varchar(8) NOT NULL,
  `libelle_ATC1` varchar(255) NOT NULL,
  PRIMARY KEY (`code_ATC1`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `ATC1` (`code_ATC1`, `libelle_ATC1`) VALUES
('C',	'Système cardio-vasculaire'),
('J',	'Anti-infectieux (usage systémique)'),
('N',	'Système nerveux');

DROP TABLE IF EXISTS `ATC2`;
CREATE TABLE `ATC2` (
  `code_ATC2` varchar(8) NOT NULL,
  `libelle_ATC2` varchar(255) NOT NULL,
  `code_ATC1` varchar(8) NOT NULL,
  PRIMARY KEY (`code_ATC2`),
  KEY `code_ATC1` (`code_ATC1`),
  CONSTRAINT `ATC2_ibfk_1` FOREIGN KEY (`code_ATC1`) REFERENCES `ATC1` (`code_ATC1`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `ATC2` (`code_ATC2`, `libelle_ATC2`, `code_ATC1`) VALUES
('C03',	'Diurétiques',	'C'),
('C07',	'Agents betabloquants',	'C'),
('J01',	'Antibactériens (usage systémique)',	'J'),
('N02',	'Analgésiques',	'N');

DROP TABLE IF EXISTS `ATC3`;
CREATE TABLE `ATC3` (
  `code_ATC3` varchar(8) NOT NULL,
  `libelle_ATC3` varchar(255) NOT NULL,
  `code_ATC2` varchar(8) NOT NULL,
  PRIMARY KEY (`code_ATC3`),
  KEY `code_ATC2` (`code_ATC2`),
  CONSTRAINT `ATC3_ibfk_1` FOREIGN KEY (`code_ATC2`) REFERENCES `ATC2` (`code_ATC2`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `ATC3` (`code_ATC3`, `libelle_ATC3`, `code_ATC2`) VALUES
('C03A',	'Diurétiques low-ceiling, thiazidiques',	'C03'),
('C07A',	'Bêtabloquants',	'C07'),
('J01C',	'Antibactériens bêta-lactamines, pénicillines',	'J01'),
('J01D',	'Autres antibactériens bêta-lactamines',	'J01'),
('J01M',	'Antibactériens quinolones',	'J01'),
('N02B',	'Autres analgésiques et antipyrétiques',	'N02');

DROP TABLE IF EXISTS `ATC4`;
CREATE TABLE `ATC4` (
  `code_ATC4` varchar(8) NOT NULL,
  `libelle_ATC4` varchar(255) NOT NULL,
  `code_ATC3` varchar(8) NOT NULL,
  PRIMARY KEY (`code_ATC4`),
  KEY `code_ATC3` (`code_ATC3`),
  CONSTRAINT `ATC4_ibfk_1` FOREIGN KEY (`code_ATC3`) REFERENCES `ATC3` (`code_ATC3`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `ATC4` (`code_ATC4`, `libelle_ATC4`, `code_ATC3`) VALUES
('C03AA',	'Thiazidiques non associés',	'C03A'),
('C07AB',	'Bêtabloquants sélectifs',	'C07A'),
('J01CA',	'Pénicillines à spectre large',	'J01C'),
('J01DD',	'Céphalisporines de troisième génération',	'J01D'),
('J01MA',	'Fluoroquinolones',	'J01M'),
('N02BE',	'Anilides',	'N02B');

DROP TABLE IF EXISTS `ATC5`;
CREATE TABLE `ATC5` (
  `code_ATC5` varchar(8) NOT NULL,
  `libelle_ATC5` varchar(255) NOT NULL,
  `code_ATC4` varchar(8) NOT NULL,
  PRIMARY KEY (`code_ATC5`),
  KEY `code_ATC4` (`code_ATC4`),
  CONSTRAINT `ATC5_ibfk_1` FOREIGN KEY (`code_ATC4`) REFERENCES `ATC4` (`code_ATC4`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `Dispensation`;
CREATE TABLE `Dispensation` (
  `RPPS` int(10) unsigned NOT NULL,
  `IPP` int(10) unsigned NOT NULL,
  `cip` int(10) unsigned NOT NULL,
  `date_heure_dispensation` datetime NOT NULL,
  PRIMARY KEY (`RPPS`,`IPP`,`cip`),
  KEY `IPP` (`IPP`),
  KEY `cip` (`cip`),
  CONSTRAINT `Dispensation_ibfk_1` FOREIGN KEY (`RPPS`) REFERENCES `Medecin` (`RPPS`),
  CONSTRAINT `Dispensation_ibfk_2` FOREIGN KEY (`IPP`) REFERENCES `Patient` (`IPP`),
  CONSTRAINT `Dispensation_ibfk_3` FOREIGN KEY (`cip`) REFERENCES `Medicament` (`cip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `Infirmier`;
CREATE TABLE `Infirmier` (
  `ADELI` int(10) unsigned NOT NULL,
  `type_infirmier` varchar(100) NOT NULL,
  PRIMARY KEY (`ADELI`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `Medecin`;
CREATE TABLE `Medecin` (
  `RPPS` int(10) unsigned NOT NULL,
  `specialite` varchar(100) NOT NULL DEFAULT 'Generaliste',
  PRIMARY KEY (`RPPS`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `Medicament`;
CREATE TABLE `Medicament` (
  `cip` int(10) unsigned NOT NULL,
  `DCI` varchar(255) NOT NULL,
  `code_ATC5` varchar(8) NOT NULL,
  PRIMARY KEY (`cip`),
  KEY `code_ATC5` (`code_ATC5`),
  CONSTRAINT `Medicament_ibfk_1` FOREIGN KEY (`code_ATC5`) REFERENCES `ATC5` (`code_ATC5`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `Patient`;
CREATE TABLE `Patient` (
  `IPP` int(10) unsigned NOT NULL,
  `nom` varchar(100) NOT NULL,
  `prenom` varchar(100) NOT NULL,
  `sexe` enum('H','F') DEFAULT NULL,
  `date_naissance` date DEFAULT NULL,
  PRIMARY KEY (`IPP`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `Personnel`;
CREATE TABLE `Personnel` (
  `id_personnel` int(10) unsigned NOT NULL,
  `nom` varchar(100) NOT NULL,
  `prenom` varchar(100) NOT NULL,
  PRIMARY KEY (`id_personnel`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `Pharmacien`;
CREATE TABLE `Pharmacien` (
  `RPPS` int(10) unsigned NOT NULL,
  PRIMARY KEY (`RPPS`),
  CONSTRAINT `Pharmacien_ibfk_1` FOREIGN KEY (`RPPS`) REFERENCES `Medecin` (`RPPS`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `Prescription`;
CREATE TABLE `Prescription` (
  `RPPS` int(10) unsigned NOT NULL,
  `IPP` int(10) unsigned NOT NULL,
  `cip` int(10) unsigned NOT NULL,
  `date_heure_prescription` datetime NOT NULL,
  PRIMARY KEY (`RPPS`,`IPP`,`cip`),
  KEY `IPP` (`IPP`),
  KEY `cip` (`cip`),
  CONSTRAINT `Prescription_ibfk_1` FOREIGN KEY (`RPPS`) REFERENCES `Medecin` (`RPPS`),
  CONSTRAINT `Prescription_ibfk_2` FOREIGN KEY (`IPP`) REFERENCES `Patient` (`IPP`),
  CONSTRAINT `Prescription_ibfk_3` FOREIGN KEY (`cip`) REFERENCES `Medicament` (`cip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- 2019-02-18 15:59:46
