-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Waktu pembuatan: 15 Jun 2025 pada 10.51
-- Versi server: 9.1.0
-- Versi PHP: 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `service_kendaraan`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `akun_login`
--

DROP TABLE IF EXISTS `akun_login`;
CREATE TABLE IF NOT EXISTS `akun_login` (
  `id_user` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `role` enum('admin','teknisi') DEFAULT NULL,
  PRIMARY KEY (`id_user`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data untuk tabel `akun_login`
--

INSERT INTO `akun_login` (`id_user`, `username`, `password`, `role`) VALUES
(1, 'admin', 'admin123', 'admin'),
(2, 'teknisi', 'teknisi123', 'teknisi');

-- --------------------------------------------------------

--
-- Struktur dari tabel `kategori_kendaraan`
--

DROP TABLE IF EXISTS `kategori_kendaraan`;
CREATE TABLE IF NOT EXISTS `kategori_kendaraan` (
  `id_kategori` int NOT NULL AUTO_INCREMENT,
  `nama_kategori` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_kategori`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data untuk tabel `kategori_kendaraan`
--

INSERT INTO `kategori_kendaraan` (`id_kategori`, `nama_kategori`) VALUES
(1, 'Motor'),
(2, 'Mobil'),
(3, 'Truk'),
(4, 'Bus');

-- --------------------------------------------------------

--
-- Struktur dari tabel `kendaraan`
--

DROP TABLE IF EXISTS `kendaraan`;
CREATE TABLE IF NOT EXISTS `kendaraan` (
  `id_kendaraan` int NOT NULL AUTO_INCREMENT,
  `id_pelanggan` int DEFAULT NULL,
  `id_kategori` int DEFAULT NULL,
  `plat_nomor` varchar(20) DEFAULT NULL,
  `merk` varchar(50) DEFAULT NULL,
  `model` varchar(50) DEFAULT NULL,
  `tahun` int DEFAULT NULL,
  PRIMARY KEY (`id_kendaraan`),
  KEY `id_pelanggan` (`id_pelanggan`),
  KEY `id_kategori` (`id_kategori`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data untuk tabel `kendaraan`
--

INSERT INTO `kendaraan` (`id_kendaraan`, `id_pelanggan`, `id_kategori`, `plat_nomor`, `merk`, `model`, `tahun`) VALUES
(1, 1, 2, 'B 1234 CD', 'Toyota', 'Avanza', 2018),
(2, 2, 1, 'D 5678 EF', 'Honda', 'Vario', 2020),
(3, 3, 2, 'Z 9876 GH', 'Daihatsu', 'Xenia', 2019);

-- --------------------------------------------------------

--
-- Struktur dari tabel `montir`
--

DROP TABLE IF EXISTS `montir`;
CREATE TABLE IF NOT EXISTS `montir` (
  `id_montir` int NOT NULL AUTO_INCREMENT,
  `nama` varchar(100) DEFAULT NULL,
  `spesialisasi` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_montir`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data untuk tabel `montir`
--

INSERT INTO `montir` (`id_montir`, `nama`, `spesialisasi`) VALUES
(1, 'Joko Priyono', 'Mesin Mobil'),
(2, 'Dedi Supriyadi', 'Kelistrikan Motor'),
(3, 'Rahmat Hidayat', 'Transmisi dan Roda');

-- --------------------------------------------------------

--
-- Struktur dari tabel `pelanggan`
--

DROP TABLE IF EXISTS `pelanggan`;
CREATE TABLE IF NOT EXISTS `pelanggan` (
  `id_pelanggan` int NOT NULL AUTO_INCREMENT,
  `nama` varchar(100) DEFAULT NULL,
  `telepon` varchar(20) DEFAULT NULL,
  `alamat` text,
  PRIMARY KEY (`id_pelanggan`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data untuk tabel `pelanggan`
--

INSERT INTO `pelanggan` (`id_pelanggan`, `nama`, `telepon`, `alamat`) VALUES
(1, 'Budi Santoso', '081234567890', 'Jl. Merdeka No. 10'),
(2, 'Siti Aminah', '082112345678', 'Jl. Kartini No. 5'),
(3, 'Andi Wijaya', '083345678901', 'Jl. Sudirman No. 20');

-- --------------------------------------------------------

--
-- Struktur dari tabel `servis`
--

DROP TABLE IF EXISTS `servis`;
CREATE TABLE IF NOT EXISTS `servis` (
  `id_servis` int NOT NULL AUTO_INCREMENT,
  `id_kendaraan` int DEFAULT NULL,
  `tanggal_servis` date DEFAULT NULL,
  `keluhan` text,
  `tindakan` text,
  `biaya` int DEFAULT NULL,
  PRIMARY KEY (`id_servis`),
  KEY `id_kendaraan` (`id_kendaraan`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data untuk tabel `servis`
--

INSERT INTO `servis` (`id_servis`, `id_kendaraan`, `tanggal_servis`, `keluhan`, `tindakan`, `biaya`) VALUES
(1, 1, '2025-06-01', 'Mesin cepat panas', 'Ganti oli dan cek radiator', 350000),
(2, 2, '2025-06-05', 'Rem tidak pakem', 'Ganti kampas rem', 200000),
(3, 3, '2025-06-10', 'AC tidak dingin', 'Tambah freon dan periksa blower', 300000);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
