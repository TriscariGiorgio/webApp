-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Creato il: Feb 09, 2024 alle 09:43
-- Versione del server: 10.4.32-MariaDB
-- Versione PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `museo`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `artista`
--

CREATE TABLE `artista` (
  `id_artista` int(11) NOT NULL,
  `nome` varchar(255) NOT NULL,
  `nazionalita` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `artista`
--

INSERT INTO `artista` (`id_artista`, `nome`, `nazionalita`) VALUES
(1, 'Robert Arneson\r\n', 'American\r\n'),
(2, 'Doroteo Arnaiz\r\n', 'Spanish\r\n'),
(3, 'Folke Arstrom\r\n', 'Swedish\r\n');

-- --------------------------------------------------------

--
-- Struttura della tabella `opera`
--

CREATE TABLE `opera` (
  `id_opera` int(11) NOT NULL,
  `titolo` varchar(255) NOT NULL,
  `data` varchar(255) NOT NULL,
  `tumbnail` varchar(255) NOT NULL,
  `id_artista` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `opera`
--

INSERT INTO `opera` (`id_opera`, `titolo`, `data`, `tumbnail`, `id_artista`) VALUES
(1, 'Gated Wall, Perspective and elevation\r\n', '1938', 'http://www.moma.org/media/W1siZiIsIjYwMTI0Il0sWyJwIiwiY29udmVydCIsIi1yZXNpemUgMzAweDMwMFx1MDAzZSJdXQ.jpg?sha=7e27882e1418ef6a\r\n', 1),
(2, 'City Hall, project, North Canton, Ohio, Perspective sketch', '1890', 'http://www.moma.org/media/W1siZiIsIjIxMjgiXSxbInAiLCJjb252ZXJ0IiwiLXJlc2l6ZSAzMDB4MzAwXHUwMDNlIl1d.jpg?sha=62d5e18053f62b75\r\n', 1),
(3, 'Housing, project, Elevation', '1678', 'http://www.moma.org/media/W1siZiIsIjExNTkyIl0sWyJwIiwiY29udmVydCIsIi1yZXNpemUgMzAweDMwMFx1MDAzZSJdXQ.jpg?sha=de90181fa4aaf2a4\r\n', 1),
(4, 'Orange Sound, project', '1457', 'http://www.moma.org/media/W1siZiIsIjU5ODQyIl0sWyJwIiwiY29udmVydCIsIi1yZXNpemUgMzAweDMwMFx1MDAzZSJdXQ.jpg?sha=f23229b7c1e8f38a', 2),
(5, 'Is Stool\r\n', '1987', 'http://www.moma.org/media/W1siZiIsIjIxMDAxOCJdLFsicCIsImNvbnZlcnQiLCItcmVzaXplIDMwMHgzMDBcdTAwM2UiXV0.jpg?sha=dcd6ac985b601f1a', 2),
(6, 'Floor Lamp', '1590', 'http://www.moma.org/media/W1siZiIsIjYyMzM2Il0sWyJwIiwiY29udmVydCIsIi1yZXNpemUgMzAweDMwMFx1MDAzZSJdXQ.jpg?sha=787abcbf3d53d6ce', 2);

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `artista`
--
ALTER TABLE `artista`
  ADD PRIMARY KEY (`id_artista`);

--
-- Indici per le tabelle `opera`
--
ALTER TABLE `opera`
  ADD PRIMARY KEY (`id_opera`),
  ADD KEY `artista_id_fk` (`id_artista`);

--
-- AUTO_INCREMENT per le tabelle scaricate
--

--
-- AUTO_INCREMENT per la tabella `artista`
--
ALTER TABLE `artista`
  MODIFY `id_artista` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT per la tabella `opera`
--
ALTER TABLE `opera`
  MODIFY `id_opera` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Limiti per le tabelle scaricate
--

--
-- Limiti per la tabella `opera`
--
ALTER TABLE `opera`
  ADD CONSTRAINT `artista_id_fk` FOREIGN KEY (`id_artista`) REFERENCES `artista` (`id_artista`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
