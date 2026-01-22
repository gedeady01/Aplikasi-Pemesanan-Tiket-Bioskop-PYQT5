-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 19, 2026 at 07:18 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_bioskop`
--

-- --------------------------------------------------------

--
-- Table structure for table `detail_transaksi`
--

CREATE TABLE `detail_transaksi` (
  `id_detail` int(20) NOT NULL,
  `transaksi_id` int(20) DEFAULT NULL,
  `kursi_id` int(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `detail_transaksi`
--

INSERT INTO `detail_transaksi` (`id_detail`, `transaksi_id`, `kursi_id`) VALUES
(1, 1, 1),
(2, 1, 2),
(3, 2, 4),
(4, 3, 3),
(5, 5, 5),
(6, 7, 27),
(7, 7, 28),
(8, 7, 29),
(9, 8, 21),
(10, 8, 22),
(11, 8, 23),
(12, 9, 8),
(13, 9, 15),
(14, 9, 20),
(15, 10, 26);

-- --------------------------------------------------------

--
-- Table structure for table `film`
--

CREATE TABLE `film` (
  `id_film` int(20) NOT NULL,
  `judul` varchar(200) DEFAULT NULL,
  `genre` varchar(100) DEFAULT NULL,
  `durasi` int(20) DEFAULT NULL,
  `rating` varchar(10) DEFAULT NULL,
  `deskripsi` text DEFAULT NULL,
  `poster` varchar(255) DEFAULT NULL,
  `status` enum('tayang','cooming soon') DEFAULT NULL,
  `trailer_url` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `film`
--

INSERT INTO `film` (`id_film`, `judul`, `genre`, `durasi`, `rating`, `deskripsi`, `poster`, `status`, `trailer_url`) VALUES
(1, 'Avengers: Endgame', 'Action', 180, 'PG-13', 'Pertempuran terakhir melawan Thanos.', 'avengers-endgame.jpg', 'tayang', 'https://youtu.be/TcMBFSGVi1c?si=KzO7zoPLAvSkHiQE'),
(2, 'Frozen II', 'Animation', 103, 'G', 'Perjalanan Elsa mencari asal kekuatannya.', 'frozen2.jpg', 'tayang', 'https://youtu.be/Zi4LMpSDccc?si=oCwC9RtADHH-qYb4'),
(3, 'Joker', 'Drama', 122, 'R', 'Kisah asal mula musuh Batman.', 'joker.jpg', 'tayang', 'https://youtu.be/t433PEQGErc?si=X2xXUl_LkjSc65Nh'),
(4, 'The Batman', 'Action', 175, 'PG-13', 'Batman menghadapi Riddler di Gotham.', 'batman.jpg', 'tayang', 'https://youtu.be/mqqft2x_Aa4?si=BSjFZXRkQBjFCe2T'),
(5, 'Inside Out 2', 'Animation', 95, 'G', 'Petualangan emosi baru di kepala Riley.', 'inside-out2.jpg', 'tayang', 'https://youtu.be/LEjhY15eCx0?si=ps7a5rNfV0YFvb-6'),
(6, '28 Years Later', 'Horror, Thriller', 115, 'R', 'Sekuel legendaris yang mengambil latar 28 tahun setelah wabah virus \"Rage\". Fokus pada perjuangan manusia di dunia yang sudah hancur total.', '28-year-later.jpg', 'tayang', 'https://youtu.be/mcvLKldPM08?si=BrQnT5PdmcXM2foS'),
(7, 'Greenland 2: Migration', 'Action, Sci-Fi', 125, 'PG-13', 'Keluarga Garrity keluar dari bunker Greenland untuk melintasi Eropa yang beku demi mencari tempat tinggal baru yang aman.', 'greenland-migration2.jpg', 'tayang', 'https://youtu.be/H8ieN10lX40?si=5yNkfHA178SkXg80'),
(8, 'Send Help', 'Thriller, Survival', 100, 'R', 'Disutradarai Sam Raimi. Dua rekan kerja terdampar di pulau terpencil setelah kecelakaan pesawat dan harus bertahan hidup dari ancaman misterius.', 'send-help.jpg', 'tayang', 'https://youtu.be/R4wiXj9NmEE?si=Lfkvb0enENyOag56'),
(9, 'Project Hail Mary', 'Sci-Fi, Drama', 135, 'PG-13', 'Dibintangi Ryan Gosling. Seorang astronot terbangun di luar angkasa tanpa ingatan dan harus menggunakan sains untuk menyelamatkan Bumi.', 'project-hail-mary.jpg', 'tayang', 'https://youtu.be/m08TxIsFTRI?si=LOWSuroFiCMsDN2M'),
(10, 'Return to Silent Hill', 'Horor, Misteri', 110, 'R', 'Adaptasi baru dari gim horor ikonik. Seorang pria kembali ke kota berkabut Silent Hill untuk mencari cintanya yang hilang.', 'return-to-silenthill.jpg', 'tayang', 'https://youtu.be/eej34Jw7woA?si=68z_veIOImemWtAP');

-- --------------------------------------------------------

--
-- Table structure for table `jadwal`
--

CREATE TABLE `jadwal` (
  `id_jadwal` int(20) NOT NULL,
  `film_id` int(20) DEFAULT NULL,
  `studio_id` int(20) DEFAULT NULL,
  `tanggal` date DEFAULT NULL,
  `jam_mulai` time DEFAULT NULL,
  `harga` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `jadwal`
--

INSERT INTO `jadwal` (`id_jadwal`, `film_id`, `studio_id`, `tanggal`, `jam_mulai`, `harga`) VALUES
(1, 1, 1, '2025-10-22', '14:00:00', 50000.00),
(2, 1, 1, '2025-10-22', '19:00:00', 50000.00),
(3, 2, 2, '2025-10-22', '16:00:00', 45000.00),
(4, 3, 3, '2025-10-23', '20:00:00', 55000.00),
(5, 4, 4, '2025-10-24', '18:00:00', 60000.00),
(6, 5, 3, '2026-01-28', '18:00:00', 40000.00),
(7, 6, 1, '2026-01-27', '20:00:00', 45000.00),
(8, 7, 4, '2026-01-29', '19:00:00', 50000.00),
(9, 9, 4, '2026-01-25', '15:00:00', 65000.00),
(10, 10, 5, '2026-01-30', '14:00:00', 75000.00),
(11, 8, 2, '2026-01-27', '15:00:00', 45000.00);

-- --------------------------------------------------------

--
-- Table structure for table `kursi`
--

CREATE TABLE `kursi` (
  `id_kursi` int(20) NOT NULL,
  `studio_id` int(20) DEFAULT NULL,
  `kode_kursi` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `kursi`
--

INSERT INTO `kursi` (`id_kursi`, `studio_id`, `kode_kursi`) VALUES
(1, 1, 'A1'),
(2, 1, 'A2'),
(3, 1, 'B1'),
(4, 2, 'C1'),
(5, 2, 'C2'),
(6, 2, 'A1'),
(7, 2, 'A2'),
(8, 2, 'A3'),
(9, 2, 'A4'),
(10, 2, 'A5'),
(11, 2, 'A6'),
(12, 2, 'A7'),
(13, 2, 'B1'),
(14, 2, 'B2'),
(15, 2, 'B3'),
(16, 2, 'B4'),
(17, 2, 'B5'),
(18, 2, 'B6'),
(19, 2, 'B7'),
(20, 2, 'C3'),
(21, 2, 'C4'),
(22, 2, 'C5'),
(23, 2, 'C6'),
(24, 2, 'C7'),
(25, 2, 'D1'),
(26, 2, 'D2'),
(27, 2, 'D3'),
(28, 2, 'D4'),
(29, 2, 'D5'),
(30, 2, 'D6'),
(31, 2, 'D7');

-- --------------------------------------------------------

--
-- Table structure for table `studio`
--

CREATE TABLE `studio` (
  `id_studio` int(20) NOT NULL,
  `nama_studio` varchar(50) DEFAULT NULL,
  `kapasitas` int(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `studio`
--

INSERT INTO `studio` (`id_studio`, `nama_studio`, `kapasitas`) VALUES
(1, 'Studio 1', 100),
(2, 'Studio 2', 80),
(3, 'Studio 3', 120),
(4, 'Studio 4', 60),
(5, 'Studio 5', 150);

-- --------------------------------------------------------

--
-- Table structure for table `transaksi`
--

CREATE TABLE `transaksi` (
  `id_transaksi` int(20) NOT NULL,
  `user_id` int(20) DEFAULT NULL,
  `jadwal_id` int(20) DEFAULT NULL,
  `tanggal_pesan` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `total_harga` decimal(10,2) DEFAULT NULL,
  `status` enum('pending','paid','cancelled') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transaksi`
--

INSERT INTO `transaksi` (`id_transaksi`, `user_id`, `jadwal_id`, `tanggal_pesan`, `total_harga`, `status`) VALUES
(1, 2, 1, '2025-10-21 02:00:00', 100000.00, 'paid'),
(2, 3, 3, '2025-10-21 03:30:00', 45000.00, 'pending'),
(3, 4, 2, '2025-10-21 04:00:00', 50000.00, 'paid'),
(4, 5, 4, '2025-10-22 01:15:00', 55000.00, 'cancelled'),
(5, 2, 5, '2025-10-22 02:45:00', 60000.00, 'paid'),
(6, 2, 1, '2026-01-18 06:06:09', 100000.00, 'paid'),
(7, 1, 3, '2026-01-19 03:26:19', 135000.00, 'paid'),
(8, 2, 3, '2026-01-19 03:31:02', 135000.00, 'paid'),
(9, 2, 3, '2026-01-19 03:31:41', 135000.00, 'paid'),
(10, 1, 3, '2026-01-19 03:51:06', 49000.00, 'paid'),
(11, 1, 4, '2026-01-19 04:02:57', 59000.00, 'paid'),
(12, 1, 6, '2026-01-19 04:17:17', 80000.00, 'paid'),
(13, 1, 8, '2026-01-19 05:11:23', 50000.00, 'paid'),
(14, 1, 8, '2026-01-19 05:17:30', 104000.00, 'paid');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id_user` int(20) NOT NULL,
  `nama` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  `no_hp` varchar(20) DEFAULT NULL,
  `role` enum('customer','admin') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id_user`, `nama`, `email`, `password`, `no_hp`, `role`) VALUES
(1, 'Admin Bioskop', 'admin@bioskop.com', 'admin123', '081234567890', 'admin'),
(2, 'Nabil Jago', 'nabil@gmail.com', 'nabil123', '081222334455', 'customer'),
(3, 'Siti Aminah', 'siti@gmail.com', 'siti123', '081233445566', 'customer'),
(4, 'Budi Santoso', 'budi@gmail.com', 'budi123', '081244556677', 'customer'),
(5, 'Dewi Anggraini', 'dewi@gmail.com', 'dewi123', '081255667788', 'customer');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `detail_transaksi`
--
ALTER TABLE `detail_transaksi`
  ADD PRIMARY KEY (`id_detail`),
  ADD KEY `fk_transaksi` (`transaksi_id`),
  ADD KEY `fk_kursi` (`kursi_id`);

--
-- Indexes for table `film`
--
ALTER TABLE `film`
  ADD PRIMARY KEY (`id_film`);

--
-- Indexes for table `jadwal`
--
ALTER TABLE `jadwal`
  ADD PRIMARY KEY (`id_jadwal`),
  ADD KEY `fk_film` (`film_id`),
  ADD KEY `fk_studio` (`studio_id`);

--
-- Indexes for table `kursi`
--
ALTER TABLE `kursi`
  ADD PRIMARY KEY (`id_kursi`),
  ADD KEY `fk_studio_kursi` (`studio_id`);

--
-- Indexes for table `studio`
--
ALTER TABLE `studio`
  ADD PRIMARY KEY (`id_studio`);

--
-- Indexes for table `transaksi`
--
ALTER TABLE `transaksi`
  ADD PRIMARY KEY (`id_transaksi`),
  ADD KEY `fk_user` (`user_id`),
  ADD KEY `fk_jadwal` (`jadwal_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id_user`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `detail_transaksi`
--
ALTER TABLE `detail_transaksi`
  MODIFY `id_detail` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `film`
--
ALTER TABLE `film`
  MODIFY `id_film` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `jadwal`
--
ALTER TABLE `jadwal`
  MODIFY `id_jadwal` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `kursi`
--
ALTER TABLE `kursi`
  MODIFY `id_kursi` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `studio`
--
ALTER TABLE `studio`
  MODIFY `id_studio` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `transaksi`
--
ALTER TABLE `transaksi`
  MODIFY `id_transaksi` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id_user` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `detail_transaksi`
--
ALTER TABLE `detail_transaksi`
  ADD CONSTRAINT `fk_kursi` FOREIGN KEY (`kursi_id`) REFERENCES `kursi` (`id_kursi`),
  ADD CONSTRAINT `fk_transaksi` FOREIGN KEY (`transaksi_id`) REFERENCES `transaksi` (`id_transaksi`);

--
-- Constraints for table `jadwal`
--
ALTER TABLE `jadwal`
  ADD CONSTRAINT `fk_film` FOREIGN KEY (`film_id`) REFERENCES `film` (`id_film`),
  ADD CONSTRAINT `fk_studio` FOREIGN KEY (`studio_id`) REFERENCES `studio` (`id_studio`);

--
-- Constraints for table `kursi`
--
ALTER TABLE `kursi`
  ADD CONSTRAINT `fk_studio_kursi` FOREIGN KEY (`studio_id`) REFERENCES `studio` (`id_studio`);

--
-- Constraints for table `transaksi`
--
ALTER TABLE `transaksi`
  ADD CONSTRAINT `fk_jadwal` FOREIGN KEY (`jadwal_id`) REFERENCES `jadwal` (`id_jadwal`),
  ADD CONSTRAINT `fk_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id_user`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
