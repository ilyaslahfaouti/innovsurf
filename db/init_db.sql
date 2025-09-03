-- --------------------------------------------------------
-- Hôte:                         127.0.0.1
-- Version du serveur:           8.0.30 - MySQL Community Server - GPL
-- SE du serveur:                Win64
-- HeidiSQL Version:             12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Listage de la structure de la base pour yala_surf
CREATE DATABASE IF NOT EXISTS `yala_surf` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `yala_surf`;

-- Listage de la structure de table yala_surf. AppWeb_contact
CREATE TABLE IF NOT EXISTS `AppWeb_contact` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `email` varchar(254) NOT NULL,
  `message` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table yala_surf.AppWeb_contact : ~0 rows (environ)

-- Listage de la structure de table yala_surf. AppWeb_customuser
CREATE TABLE IF NOT EXISTS `AppWeb_customuser` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `last_login` datetime(6) DEFAULT NULL,
  `email` varchar(254) NOT NULL,
  `password` varchar(128) NOT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `is_surfer` tinyint(1) NOT NULL,
  `is_surfclub` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table yala_surf.AppWeb_customuser : ~25 rows (environ)
INSERT INTO `AppWeb_customuser` (`id`, `last_login`, `email`, `password`, `phone_number`, `address`, `is_surfer`, `is_surfclub`, `is_staff`, `is_superuser`) VALUES
	(1, '2024-09-09 22:51:17.246861', 'surf@gmail.com', 'pbkdf2_sha256$870000$1dQFYwIjysP9TAV0di31dk$k9FG2LRtGlVIg4X0QMnrCdTTFLHIjdl21uXQ+DU8u4Y=', NULL, NULL, 0, 0, 1, 1),
	(20, NULL, 'club1@gmail.com', 'pbkdf2_sha256$870000$pOeysXcIBxepT2meWguARo$nTd+rpYmu/1Jj/+anEpYoIsYBQiaCzCQqWxY8gcyRIM=', '212612345678', 'Rue des Surfers, Taghazout, Maroc', 0, 1, 0, 0),
	(21, NULL, 'club2@gmail.com', 'pbkdf2_sha256$870000$7WKz8gzKde5EKgfIs42KXB$iATnQMHnhN9WDg7jo0orhdnNiAFjrjbl6OlTCS17jU0=', '212613456789', 'Plage Anchor, Taghazout, Maroc', 0, 1, 0, 0),
	(22, NULL, 'club3@gmail.com', 'pbkdf2_sha256$870000$drkzpDBir6y9r4pYJ8NNM9$8GpbOMh49sTmZaWtzqFLz3/Vg/2IZV1M0uQwyJEl1t8=', '212614567887', 'Taghazout Beach, Taghazout, Maroc', 0, 1, 0, 0),
	(23, NULL, 'club4@gmail.com', 'pbkdf2_sha256$870000$oLD1OejVlcRBnpoWmEiOkd$mm7BMl96u/+m9MG24m5Ht3dFfd8KaSPDQ2X8/76xtdw=', '212615678901', 'Route d’Essaouira, Taghazout, Maroc', 0, 1, 0, 0),
	(24, NULL, 'club5@gmail.com', 'pbkdf2_sha256$870000$1YLhJtJq0GxvRfmi3ok6Ji$yBNamwu26W5Dbts8CB6ktWhkNdIIdf8IZ8zbSBB4LCA=', '212616789012', 'Avenue Hassan II, Agadir, Maroc', 0, 1, 0, 0),
	(25, NULL, 'club6@gmail.com', 'pbkdf2_sha256$870000$mcZErWeJp2jXyx7pP46CUe$ugJj28zYoA5jVhuKPQoJ6IOPEGh2nKH+a78J2syFsLQ=', '212617890122', 'Plage Anza, Agadir, Maroc', 0, 1, 0, 0),
	(26, NULL, 'club7@gmail.com', 'pbkdf2_sha256$870000$asBZr8dOzKbfhpn3xPWWL0$2bvQaxH3IG58w3DHkxpPd1dLXULNhrSkv4qwUGo0fPQ=', '212618901234', 'Quartier Anza, Agadir, Maroc', 0, 1, 0, 0),
	(27, NULL, 'club8@gmail.com', 'pbkdf2_sha256$870000$7qzBtmx0B8mPHahr6hez9k$+/54UEu46CHYK8Vj3mv3bOqAd578Ng9pPCVmuFvEOlA=', '212619012344', 'Chemin des Plages, Anza, Maroc', 0, 1, 0, 0),
	(28, NULL, 'club9@gmail.com', 'pbkdf2_sha256$870000$E75onGLVfPnnp2St66E2x3$kQAcClobpGQAQMpUX03/lb/zuMQg+QW1dr4eThwLTgo=', '212620123455', 'Plage de la Crique, Bouznika, Maroc', 0, 1, 0, 0),
	(29, NULL, 'club10@gmail.com', 'pbkdf2_sha256$870000$R5lYwzy6bPr2c0uPuRsKcA$xD06UyUb+lTpb2EJYa6k8sLmAlUumnXHLa9qf1mYhNU=', '212621234565', 'Avenue Mohammed V, Bouznika, Maroc', 0, 1, 0, 0),
	(30, NULL, 'club11@gmail.com', 'pbkdf2_sha256$870000$CfkSD4LPYT7hOKNi7rtDuQ$AOSpKlS1OruKaeXi6DWMU4bVVsXoWS4LXPV4VRnD8oo=', '212622345677', 'Bord de mer, Bouznika, Maroc', 0, 1, 0, 0),
	(31, NULL, 'club12@gmail.com', 'pbkdf2_sha256$870000$QbueHb8ImYJLGreobhlrMf$tFThYT0IMJO1nvE8sigf9C4pePzmSE5q906oVa2w3Fc=', '212623456789', 'Quartier la Crique, Bouznika, Maroc', 0, 1, 0, 0),
	(32, NULL, 'club13@gmail.com', 'pbkdf2_sha256$870000$FxqizhzhHUVlUugvFeMTAc$cVRqP0uJ+5GBaQ8Liu4qOUwTQa81a/F7srFneC4cRPg=', '212624567890', 'Plage des Oudayas, Rabat, Maroc', 0, 1, 0, 0),
	(33, NULL, 'club14@gmail.com', 'pbkdf2_sha256$870000$fGdjuYTmd6Nljsla2XtSdL$RWQXPmOWSHtb0kT+pMZLUY/fMpNWh1HRZsUdCe+e+SE=', '212625678901', 'Rue des Oudayas, Rabat, Maroc', 0, 1, 0, 0),
	(34, NULL, 'surfer1@gmail.com', 'pbkdf2_sha256$870000$1scbXL8NjwTFX3fTY14nst$D7k4Ko63+04pEEVD498yYDlwe/ODpsagAMUzvUR8k0k=', '0610750250', '31 bd lascrosses, Toulouse', 1, 0, 0, 0),
	(35, NULL, 'club15@gmail.com', 'pbkdf2_sha256$870000$HFyASi1IsyPeDCkx0pSiU7$Y7+1mErlw9wSRj4tI+Zmhzz6hQOtOfk55fbTGUjYh7M=', '212626789012', 'Place des Oudayas, Rabat, Maroc', 0, 1, 0, 0),
	(36, NULL, 'club17@gmail.com', 'pbkdf2_sha256$870000$PtVd8yMBdYVMdguEOBux1t$oGy8aTF0JqnZ10PLwTOdn+xFhAV+0t//deFOCllZQuQ=', '212628901234', 'Plage Banana, Aourir, Maroc', 0, 1, 0, 0),
	(37, NULL, 'club18@gmail.com', 'pbkdf2_sha256$870000$nmpCwKCnSRkuzaE17GweFv$6vgdAPa7+d4Xc330AbsjGmEjt2MHO4/08b6mvrXOiSM=', '212629012345', 'Avenue Banana, Aourir, Maroc', 0, 1, 0, 0),
	(38, NULL, 'club19@gmail.com', 'pbkdf2_sha256$870000$QT3UNelkOuGxorq6cCYkJ4$KCDy2+EPzBdi2DrZM+Hm55GdOCaEIUfYMdlVq8juo/o=', '212630123456', 'Rue de l’Océan, Aourir, Maroc', 0, 1, 0, 0),
	(39, NULL, 'club21@gmail.com', 'pbkdf2_sha256$870000$hy1ziHl7ZQbmnIFLsPcABE$+KZc3//l7IwzJUPfzkad9xTDAdxroTBH+LuDpHFfEo0=', '212632345678', 'Plage Killer Point, Taghazout, Maroc', 0, 1, 0, 0),
	(40, NULL, 'club22@gmail.com', 'pbkdf2_sha256$870000$mG9Xccde9dZBkvDLaxyzdT$qQqzUBdNCRsgX+SyWcvftP30Qtwi3U5RloVRkUnJXso=', '212633456789', 'Quartier Killer Point, Taghazout, Maroc', 0, 1, 0, 0),
	(41, NULL, 'club24@gmail.com', 'pbkdf2_sha256$870000$u05d20tvDaT1W9MywMaHLw$L2wrQgI5avTmA4BOuYQaJ960cJ1T+F72TwbkB/PvU9c=', '212635678901', 'Avenue Killer, Taghazout, Maroc', 0, 1, 0, 0),
	(42, NULL, 'surfer2@gmail.com', 'pbkdf2_sha256$870000$yv22qMpO0lW8DRqj6WHh1R$ccBZLzoZdSf40ZmOs6UeyAEqz/eDXDQkAOU/s2kKOb8=', '610853957', '31 bd lascrosses, Toulouse', 1, 0, 0, 0),
	(43, NULL, 'surfer3@gmail.Com', 'pbkdf2_sha256$870000$8JVyRGpNxP2E25Qya2r9Y6$FiVj38suSWP+p5B+AHoG2F2OTKEwDQawl+2EWKviQNg=', '0610750250', '31 bd Lascrosses', 1, 0, 0, 0);

-- Listage de la structure de table yala_surf. AppWeb_customuser_groups
CREATE TABLE IF NOT EXISTS `AppWeb_customuser_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `AppWeb_customuser_groups_customuser_id_group_id_d88f841a_uniq` (`customuser_id`,`group_id`),
  KEY `AppWeb_customuser_groups_group_id_7aa7440f_fk_auth_group_id` (`group_id`),
  CONSTRAINT `AppWeb_customuser_gr_customuser_id_3a75e4ab_fk_AppWeb_cu` FOREIGN KEY (`customuser_id`) REFERENCES `AppWeb_customuser` (`id`),
  CONSTRAINT `AppWeb_customuser_groups_group_id_7aa7440f_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table yala_surf.AppWeb_customuser_groups : ~0 rows (environ)

-- Listage de la structure de table yala_surf. AppWeb_customuser_user_permissions
CREATE TABLE IF NOT EXISTS `AppWeb_customuser_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `AppWeb_customuser_user_p_customuser_id_permission_454aacc2_uniq` (`customuser_id`,`permission_id`),
  KEY `AppWeb_customuser_us_permission_id_028041c8_fk_auth_perm` (`permission_id`),
  CONSTRAINT `AppWeb_customuser_us_customuser_id_064d336c_fk_AppWeb_cu` FOREIGN KEY (`customuser_id`) REFERENCES `AppWeb_customuser` (`id`),
  CONSTRAINT `AppWeb_customuser_us_permission_id_028041c8_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table yala_surf.AppWeb_customuser_user_permissions : ~0 rows (environ)

-- Listage de la structure de table yala_surf. AppWeb_equipment
CREATE TABLE IF NOT EXISTS `AppWeb_equipment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `size` varchar(50) NOT NULL,
  `state` varchar(50) NOT NULL,
  `material_type` varchar(4) NOT NULL,
  `sale_price` decimal(10,2) DEFAULT NULL,
  `rent_price` decimal(10,2) DEFAULT NULL,
  `equipment_type_id` bigint NOT NULL,
  `surf_club_id` bigint NOT NULL,
  `quantity` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `AppWeb_equipment_equipment_type_id_b31afc4d_fk_AppWeb_eq` (`equipment_type_id`),
  KEY `AppWeb_equipment_surf_club_id_9b0ea9c9_fk_AppWeb_surfclub_id` (`surf_club_id`),
  CONSTRAINT `AppWeb_equipment_equipment_type_id_b31afc4d_fk_AppWeb_eq` FOREIGN KEY (`equipment_type_id`) REFERENCES `AppWeb_equipmenttype` (`id`),
  CONSTRAINT `AppWeb_equipment_surf_club_id_9b0ea9c9_fk_AppWeb_surfclub_id` FOREIGN KEY (`surf_club_id`) REFERENCES `AppWeb_surfclub` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=150 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table yala_surf.AppWeb_equipment : ~133 rows (environ)
INSERT INTO `AppWeb_equipment` (`id`, `name`, `description`, `size`, `state`, `material_type`, `sale_price`, `rent_price`, `equipment_type_id`, `surf_club_id`, `quantity`) VALUES
	(12, 'Al merick', 'This surfboard is designed to deliver optimal performance in small to medium-sized waves. Crafted with lightweight and durable EPS foam, it offers excellent buoyancy, making paddling and catching waves easier.', '6"3', 'new', 'sale', 668.00, NULL, 1, 5, 40),
	(14, 'NSP Fish', 'This high-performance shortboard is built for speed, precision, and agility in powerful, fast-breaking waves. Crafted from lightweight yet durable fiberglass, it offers the perfect balance of strength and flexibility.', '5"11', 'new', 'rent', NULL, 24.00, 1, 5, 5),
	(15, 'Rip Curl SurfSuit', 'This high-quality surf suit is designed to keep you comfortable and protected in the water, offering both flexibility and warmth. Made from premium neoprene material, it provides excellent thermal insulation, ensuring that you stay warm even in colder water conditions.', '3/2', 'used', 'rent', NULL, 14.00, 3, 5, 8),
	(16, 'Rip Curl Surfboard', 'A high-performance surfboard designed for speed and agility.', '6\'1"', 'new', 'sale', 500.00, NULL, 1, 5, 18),
	(17, 'O\'Neill Surfboard', 'A durable surfboard ideal for rentals and beginners.', '6\'3"', 'used', 'rent', NULL, 20.00, 1, 5, 9),
	(18, 'FCS Leash', 'A professional leash for maximum durability.', '6 feet', 'new', 'sale', 30.00, NULL, 2, 5, 5),
	(19, 'Dakine Leash', 'A strong leash ideal for rentals and beginners.', '6 feet', 'used', 'rent', NULL, 5.00, 2, 5, 10),
	(20, 'Rip Curl Surfsuit', 'A high-quality surfsuit for maximum flexibility.', '3/2', 'new', 'sale', 150.00, NULL, 3, 5, 5),
	(21, 'O\'Neill Surfsuit', 'A durable surfsuit ideal for rentals.', '3/2', 'used', 'rent', NULL, 10.00, 3, 5, 10),
	(22, 'Quiksilver Surfboard', 'A performance board built for speed.', '5\'10"', 'new', 'sale', 550.00, NULL, 1, 6, 5),
	(23, 'O\'Neill Surfboard', 'A solid rental surfboard for beginners.', '6\'2"', 'used', 'rent', NULL, 18.00, 1, 6, 10),
	(24, 'FCS Leash', 'A top-quality leash for advanced surfers.', '6 feet', 'new', 'sale', 25.00, NULL, 2, 6, 5),
	(25, 'Dakine Leash', 'A durable leash for daily rental use.', '6 feet', 'used', 'rent', NULL, 6.00, 2, 6, 10),
	(26, 'Billabong Surfsuit', 'A flexible surfsuit designed for advanced surfers.', '4/3', 'new', 'sale', 170.00, NULL, 3, 6, 5),
	(27, 'O\'Neill Surfsuit', 'A reliable surfsuit for rental.', '3/2', 'used', 'rent', NULL, 12.00, 3, 6, 10),
	(28, 'Rip Curl Surfboard', 'A lightweight board for intermediate surfers.', '5\'11"', 'new', 'sale', 600.00, NULL, 1, 7, 5),
	(29, 'Quiksilver Surfboard', 'A great surfboard for rentals.', '6\'0"', 'used', 'rent', NULL, 22.00, 1, 7, 10),
	(30, 'Dakine Leash', 'A premium leash for professional use.', '7 feet', 'new', 'sale', 35.00, NULL, 2, 7, 5),
	(31, 'FCS Leash', 'A durable leash for rental use.', '6 feet', 'used', 'rent', NULL, 8.00, 2, 7, 10),
	(32, 'O\'Neill Surfsuit', 'A high-performance surfsuit.', '4/3', 'new', 'sale', 160.00, NULL, 3, 7, 5),
	(33, 'Rip Curl Surfsuit', 'A durable surfsuit perfect for rentals.', '3/2', 'used', 'rent', NULL, 14.00, 3, 7, 10),
	(34, 'Billabong Surfboard', 'A high-performance surfboard for advanced surfers.', '6\'2"', 'new', 'sale', 620.00, NULL, 1, 8, 5),
	(35, 'O\'Neill Surfboard', 'A durable rental board.', '6\'1"', 'used', 'rent', NULL, 20.00, 1, 8, 8),
	(36, 'Dakine Leash', 'A durable leash ideal for professional surfers.', '7 feet', 'new', 'sale', 40.00, NULL, 2, 8, 5),
	(37, 'FCS Leash', 'A reliable leash for rentals.', '6 feet', 'used', 'rent', NULL, 6.00, 2, 8, 7),
	(38, 'Rip Curl Surfsuit', 'A top-quality surfsuit for advanced performance.', '3/2', 'new', 'sale', 180.00, NULL, 3, 8, 5),
	(39, 'Billabong Surfsuit', 'A rental surfsuit designed for durability.', '3/2', 'used', 'rent', NULL, 12.00, 3, 8, 10),
	(40, 'O\'Neill Surfboard', 'A premium surfboard for intermediate and advanced surfers.', '6\'0"', 'new', 'sale', 500.00, NULL, 1, 9, 5),
	(41, 'Quiksilver Surfboard', 'A durable rental surfboard.', '6\'3"', 'used', 'rent', NULL, 22.00, 1, 9, 10),
	(42, 'Rip Curl Leash', 'A professional-grade leash for performance surfers.', '6 feet', 'new', 'sale', 28.00, NULL, 2, 9, 5),
	(43, 'Dakine Leash', 'A solid leash for rental use.', '6 feet', 'used', 'rent', NULL, 6.00, 2, 9, 10),
	(44, 'Billabong Surfsuit', 'A high-performance surfsuit for advanced use.', '4/3', 'new', 'sale', 160.00, NULL, 3, 9, 5),
	(45, 'O\'Neill Surfsuit', 'A durable rental surfsuit.', '3/2', 'used', 'rent', NULL, 12.00, 3, 9, 10),
	(46, 'Quiksilver Surfboard', 'A top-tier surfboard for large waves.', '6\'4"', 'new', 'sale', 640.00, NULL, 1, 10, 4),
	(47, 'O\'Neill Surfboard', 'A solid rental board for beginners and intermediates.', '6\'1"', 'used', 'rent', NULL, 20.00, 1, 10, 9),
	(48, 'Dakine Leash', 'A premium leash for large waves.', '8 feet', 'new', 'sale', 40.00, NULL, 2, 10, 5),
	(49, 'FCS Leash', 'A durable rental leash.', '7 feet', 'used', 'rent', NULL, 7.00, 2, 10, 10),
	(50, 'Rip Curl Surfsuit', 'A performance surfsuit for colder waters.', '5/4', 'new', 'sale', 200.00, NULL, 3, 10, 5),
	(51, 'O\'Neill Surfsuit', 'A reliable rental surfsuit.', '3/2', 'used', 'rent', NULL, 15.00, 3, 10, 10),
	(52, 'Billabong Surfboard', 'A high-performance board for intermediate surfers.', '6\'3"', 'new', 'sale', 550.00, NULL, 1, 11, 2),
	(53, 'O\'Neill Surfboard', 'A reliable surfboard for rentals.', '6\'0"', 'used', 'rent', NULL, 19.00, 1, 11, 10),
	(54, 'FCS Leash', 'A professional-grade leash for speed.', '6 feet', 'new', 'sale', 25.00, NULL, 2, 11, 5),
	(55, 'Dakine Leash', 'A strong leash for rental use.', '6 feet', 'used', 'rent', NULL, 5.00, 2, 11, 10),
	(56, 'Rip Curl Surfsuit', 'A flexible surfsuit for high-performance surfing.', '3/2', 'new', 'sale', 180.00, NULL, 3, 11, 5),
	(57, 'O\'Neill Surfsuit', 'A durable rental surfsuit for daily use.', '3/2', 'used', 'rent', NULL, 10.00, 3, 11, 10),
	(58, 'Quiksilver Surfboard', 'A lightweight performance surfboard for pros.', '6\'0"', 'new', 'sale', 600.00, NULL, 1, 12, 5),
	(59, 'Rip Curl Surfboard', 'A durable rental board for all surfers.', '6\'2"', 'used', 'rent', NULL, 22.00, 1, 12, 9),
	(60, 'Dakine Leash', 'A high-quality leash for professional use.', '7 feet', 'new', 'sale', 35.00, NULL, 2, 12, 5),
	(61, 'FCS Leash', 'A strong leash ideal for rental use.', '6 feet', 'used', 'rent', NULL, 6.00, 2, 12, 10),
	(62, 'O\'Neill Surfsuit', 'A high-performance surfsuit for professional use.', '4/3', 'new', 'sale', 170.00, NULL, 3, 12, 5),
	(63, 'Rip Curl Surfsuit', 'A reliable rental surfsuit for beginners.', '3/2', 'used', 'rent', NULL, 12.00, 3, 12, 9),
	(64, 'Billabong Surfboard', 'A high-performance surfboard for small to medium waves.', '5\'11"', 'new', 'sale', 580.00, NULL, 1, 13, 5),
	(65, 'Quiksilver Surfboard', 'A rental board for beginners.', '6\'1"', 'used', 'rent', NULL, 20.00, 1, 13, 10),
	(66, 'Rip Curl Leash', 'A premium leash for small waves.', '6 feet', 'new', 'sale', 28.00, NULL, 2, 13, 5),
	(67, 'Dakine Leash', 'A durable leash for rental use.', '6 feet', 'used', 'rent', NULL, 7.00, 2, 13, 10),
	(68, 'O\'Neill Surfsuit', 'A high-quality surfsuit for flexibility.', '4/3', 'new', 'sale', 190.00, NULL, 3, 13, 5),
	(69, 'Rip Curl Surfsuit', 'A reliable surfsuit for rentals.', '3/2', 'used', 'rent', NULL, 12.00, 3, 13, 10),
	(70, 'Rip Curl Surfboard', 'A lightweight surfboard perfect for students.', '6\'0"', 'new', 'sale', 520.00, NULL, 1, 14, 5),
	(71, 'O\'Neill Surfboard', 'A durable surfboard for rental use.', '6\'2"', 'used', 'rent', NULL, 22.00, 1, 14, 10),
	(72, 'FCS Leash', 'A professional leash for beginner surfers.', '6 feet', 'new', 'sale', 30.00, NULL, 2, 14, 5),
	(73, 'Dakine Leash', 'A durable leash for rental use.', '6 feet', 'used', 'rent', NULL, 5.00, 2, 14, 10),
	(74, 'Rip Curl Surfsuit', 'A high-quality surfsuit for maximum comfort.', '3/2', 'new', 'sale', 150.00, NULL, 3, 14, 5),
	(75, 'O\'Neill Surfsuit', 'A reliable surfsuit for rental use.', '3/2', 'used', 'rent', NULL, 12.00, 3, 14, 10),
	(76, 'Quiksilver Surfboard', 'A high-performance surfboard designed for intermediate surfers.', '6\'1"', 'new', 'sale', 590.00, NULL, 1, 15, 5),
	(77, 'Rip Curl Surfboard', 'A rental surfboard designed for all levels.', '6\'2"', 'used', 'rent', NULL, 23.00, 1, 15, 10),
	(78, 'Dakine Leash', 'A top-tier leash for maximum durability.', '6 feet', 'new', 'sale', 32.00, NULL, 2, 15, 5),
	(79, 'FCS Leash', 'A durable leash for rental use.', '6 feet', 'used', 'rent', NULL, 6.00, 2, 15, 10),
	(80, 'O\'Neill Surfsuit', 'A high-performance surfsuit for advanced surfers.', '4/3', 'new', 'sale', 170.00, NULL, 3, 15, 5),
	(81, 'Rip Curl Surfsuit', 'A comfortable surfsuit for rental.', '3/2', 'used', 'rent', NULL, 14.00, 3, 15, 10),
	(82, 'Billabong Surfboard', 'A high-quality surfboard for advanced surfers.', '6\'3"', 'new', 'sale', 600.00, NULL, 1, 16, 5),
	(83, 'O\'Neill Surfboard', 'A reliable rental surfboard.', '6\'0"', 'used', 'rent', NULL, 20.00, 1, 16, 10),
	(84, 'Rip Curl Leash', 'A durable leash for high-performance surfing.', '6 feet', 'new', 'sale', 35.00, NULL, 2, 16, 5),
	(85, 'Dakine Leash', 'A solid leash designed for rental use.', '6 feet', 'used', 'rent', NULL, 7.00, 2, 16, 10),
	(86, 'FCS Surfsuit', 'A flexible surfsuit for high-performance surfing.', '3/2', 'new', 'sale', 160.00, NULL, 3, 16, 5),
	(87, 'O\'Neill Surfsuit', 'A durable surfsuit ideal for rentals.', '3/2', 'used', 'rent', NULL, 12.00, 3, 16, 10),
	(88, 'Quiksilver Surfboard', 'A lightweight board for advanced surfers.', '5\'11"', 'new', 'sale', 580.00, NULL, 1, 17, 5),
	(89, 'Rip Curl Surfboard', 'A rental board for beginners.', '6\'1"', 'used', 'rent', NULL, 19.00, 1, 17, 10),
	(90, 'FCS Leash', 'A premium leash for maximum durability.', '6 feet', 'new', 'sale', 30.00, NULL, 2, 17, 5),
	(91, 'Dakine Leash', 'A durable leash designed for rentals.', '6 feet', 'used', 'rent', NULL, 6.00, 2, 17, 10),
	(92, 'O\'Neill Surfsuit', 'A flexible surfsuit for colder waters.', '4/3', 'new', 'sale', 180.00, NULL, 3, 17, 5),
	(93, 'Rip Curl Surfsuit', 'A reliable surfsuit perfect for rentals.', '3/2', 'used', 'rent', NULL, 12.00, 3, 17, 10),
	(94, 'Billabong Surfboard', 'A high-performance board designed for speed.', '6\'0"', 'new', 'sale', 600.00, NULL, 1, 18, 5),
	(95, 'Quiksilver Surfboard', 'A reliable rental surfboard.', '6\'2"', 'used', 'rent', NULL, 20.00, 1, 18, 10),
	(96, 'Rip Curl Leash', 'A professional-grade leash for surfing.', '6 feet', 'new', 'sale', 35.00, NULL, 2, 18, 5),
	(97, 'Dakine Leash', 'A strong leash designed for rentals.', '6 feet', 'used', 'rent', NULL, 5.00, 2, 18, 10),
	(98, 'O\'Neill Surfsuit', 'A performance surfsuit for advanced surfers.', '4/3', 'new', 'sale', 160.00, NULL, 3, 18, 5),
	(99, 'Rip Curl Surfsuit', 'A durable surfsuit ideal for rentals.', '3/2', 'used', 'rent', NULL, 12.00, 3, 18, 10),
	(100, 'Rip Curl Surfboard', 'A lightweight surfboard for school beginners.', '5\'10"', 'new', 'sale', 550.00, NULL, 1, 19, 5),
	(101, 'O\'Neill Surfboard', 'A durable rental surfboard for all levels.', '6\'0"', 'used', 'rent', NULL, 18.00, 1, 19, 10),
	(102, 'FCS Leash', 'A premium leash for professional surfers.', '6 feet', 'new', 'sale', 30.00, NULL, 2, 19, 5),
	(103, 'Dakine Leash', 'A solid leash designed for rental use.', '6 feet', 'used', 'rent', NULL, 6.00, 2, 19, 10),
	(104, 'Billabong Surfsuit', 'A comfortable surfsuit for colder waters.', '4/3', 'new', 'sale', 170.00, NULL, 3, 19, 5),
	(105, 'Rip Curl Surfsuit', 'A durable surfsuit for school rental.', '3/2', 'used', 'rent', NULL, 14.00, 3, 19, 10),
	(106, 'Quiksilver Surfboard', 'A high-performance board for intermediate surfers.', '6\'2"', 'new', 'sale', 600.00, NULL, 1, 20, 5),
	(107, 'Rip Curl Surfboard', 'A durable rental board for beginners.', '6\'0"', 'used', 'rent', NULL, 20.00, 1, 20, 10),
	(108, 'Dakine Leash', 'A professional leash for performance surfing.', '6 feet', 'new', 'sale', 28.00, NULL, 2, 20, 5),
	(109, 'FCS Leash', 'A strong leash for rental use.', '6 feet', 'used', 'rent', NULL, 5.00, 2, 20, 10),
	(110, 'Billabong Surfsuit', 'A high-performance surfsuit for advanced surfers.', '3/2', 'new', 'sale', 180.00, NULL, 3, 20, 5),
	(111, 'O\'Neill Surfsuit', 'A reliable surfsuit for rentals.', '3/2', 'used', 'rent', NULL, 12.00, 3, 20, 10),
	(112, 'Quiksilver Surfboard', 'A high-performance board for intermediate surfers.', '6\'2"', 'new', 'sale', 600.00, NULL, 1, 20, 5),
	(113, 'Rip Curl Surfboard', 'A durable rental board for beginners.', '6\'0"', 'used', 'rent', NULL, 20.00, 1, 20, 10),
	(114, 'Dakine Leash', 'A professional leash for performance surfing.', '6 feet', 'new', 'sale', 28.00, NULL, 2, 20, 5),
	(117, 'O\'Neill Surfsuit', 'A reliable surfsuit for rentals.', '3/2', 'used', 'rent', NULL, 12.00, 3, 20, 10),
	(118, 'Rip Curl Surfboard', 'A lightweight board perfect for surf school students.', '5\'11"', 'new', 'sale', 580.00, NULL, 1, 21, 5),
	(119, 'O\'Neill Surfboard', 'A rental board designed for beginners.', '6\'1"', 'used', 'rent', NULL, 22.00, 1, 21, 10),
	(120, 'FCS Leash', 'A premium leash for beginner surfers.', '6 feet', 'new', 'sale', 30.00, NULL, 2, 21, 5),
	(121, 'Dakine Leash', 'A strong leash designed for school rentals.', '6 feet', 'used', 'rent', NULL, 5.00, 2, 21, 10),
	(122, 'Rip Curl Surfsuit', 'A flexible surfsuit for students.', '3/2', 'new', 'sale', 150.00, NULL, 3, 21, 5),
	(123, 'O\'Neill Surfsuit', 'A reliable surfsuit for rental students.', '3/2', 'used', 'rent', NULL, 12.00, 3, 21, 10),
	(124, 'Quiksilver Surfboard', 'A high-quality surfboard for advanced surfers.', '6\'2"', 'new', 'sale', 620.00, NULL, 1, 22, 5),
	(125, 'Rip Curl Surfboard', 'A durable surfboard for rentals.', '6\'1"', 'used', 'rent', NULL, 22.00, 1, 22, 10),
	(126, 'FCS Leash', 'A strong leash for performance surfing.', '6 feet', 'new', 'sale', 32.00, NULL, 2, 22, 5),
	(127, 'Dakine Leash', 'A durable leash for rental use.', '6 feet', 'used', 'rent', NULL, 7.00, 2, 22, 10),
	(128, 'O\'Neill Surfsuit', 'A high-performance surfsuit for professional surfers.', '4/3', 'new', 'sale', 170.00, NULL, 3, 22, 5),
	(129, 'Rip Curl Surfsuit', 'A reliable surfsuit for rentals.', '3/2', 'used', 'rent', NULL, 14.00, 3, 22, 10),
	(130, 'Billabong Surfboard', 'A lightweight surfboard for advanced surfers.', '6\'3"', 'new', 'sale', 630.00, NULL, 1, 23, 5),
	(131, 'O\'Neill Surfboard', 'A reliable rental surfboard.', '6\'0"', 'used', 'rent', NULL, 21.00, 1, 23, 10),
	(132, 'FCS Leash', 'A professional leash for big wave surfing.', '6 feet', 'new', 'sale', 35.00, NULL, 2, 23, 5),
	(133, 'Dakine Leash', 'A durable leash for rental surfers.', '6 feet', 'used', 'rent', NULL, 8.00, 2, 23, 10),
	(134, 'Rip Curl Surfsuit', 'A high-quality surfsuit for extreme conditions.', '4/3', 'new', 'sale', 190.00, NULL, 3, 23, 5),
	(135, 'O\'Neill Surfsuit', 'A durable surfsuit for rental use.', '3/2', 'used', 'rent', NULL, 12.00, 3, 23, 10),
	(136, 'Quiksilver Surfboard', 'A high-performance surfboard for aggressive surfers.', '6\'2"', 'new', 'sale', 600.00, NULL, 1, 24, 5),
	(137, 'Rip Curl Surfboard', 'A reliable rental surfboard.', '6\'1"', 'used', 'rent', NULL, 23.00, 1, 24, 10),
	(138, 'Dakine Leash', 'A professional leash for maximum control.', '6 feet', 'new', 'sale', 30.00, NULL, 2, 24, 5),
	(139, 'FCS Leash', 'A strong leash for rental use.', '6 feet', 'used', 'rent', NULL, 7.00, 2, 24, 10),
	(140, 'Billabong Surfsuit', 'A flexible surfsuit for colder conditions.', '4/3', 'new', 'sale', 180.00, NULL, 3, 24, 5),
	(141, 'Rip Curl Surfsuit', 'A durable surfsuit for rental surfers.', '3/2', 'used', 'rent', NULL, 14.00, 3, 24, 10),
	(142, 'O\'Neill Surfboard', 'A lightweight surfboard for students.', '6\'0"', 'new', 'sale', 580.00, NULL, 1, 25, 5),
	(143, 'Rip Curl Surfboard', 'A rental surfboard for beginners.', '6\'2"', 'used', 'rent', NULL, 20.00, 1, 25, 10),
	(144, 'FCS Leash', 'A professional leash for surf students.', '6 feet', 'new', 'sale', 30.00, NULL, 2, 25, 5),
	(145, 'Dakine Leash', 'A durable leash for rental students.', '6 feet', 'used', 'rent', NULL, 6.00, 2, 25, 10),
	(146, 'Billabong Surfsuit', 'A high-quality surfsuit for school students.', '3/2', 'new', 'sale', 160.00, NULL, 3, 25, 5),
	(147, 'Rip Curl Surfsuit', 'A durable rental surfsuit for beginners.', '3/2', 'used', 'rent', NULL, 12.00, 3, 25, 10);

-- Listage de la structure de table yala_surf. AppWeb_equipmentselection
CREATE TABLE IF NOT EXISTS `AppWeb_equipmentselection` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantity` int unsigned NOT NULL,
  `equipment_id` bigint NOT NULL,
  `surf_lesson_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `AppWeb_equipmentselectio_surf_lesson_id_equipment_b7aa86af_uniq` (`surf_lesson_id`,`equipment_id`),
  KEY `AppWeb_equipmentsele_equipment_id_a40d36bd_fk_AppWeb_eq` (`equipment_id`),
  CONSTRAINT `AppWeb_equipmentsele_equipment_id_a40d36bd_fk_AppWeb_eq` FOREIGN KEY (`equipment_id`) REFERENCES `AppWeb_equipment` (`id`),
  CONSTRAINT `AppWeb_equipmentsele_surf_lesson_id_da3724ad_fk_AppWeb_su` FOREIGN KEY (`surf_lesson_id`) REFERENCES `AppWeb_surflesson` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table yala_surf.AppWeb_equipmentselection : ~9 rows (environ)
INSERT INTO `AppWeb_equipmentselection` (`id`, `quantity`, `equipment_id`, `surf_lesson_id`) VALUES
	(12, 2, 35, 9),
	(13, 3, 37, 9),
	(14, 1, 59, 10),
	(15, 1, 63, 10),
	(17, 1, 47, 12),
	(18, 1, 15, 13),
	(19, 1, 14, 13),
	(20, 1, 15, 14),
	(21, 1, 17, 14);

-- Listage de la structure de table yala_surf. AppWeb_equipmenttype
CREATE TABLE IF NOT EXISTS `AppWeb_equipmenttype` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `type` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table yala_surf.AppWeb_equipmenttype : ~3 rows (environ)
INSERT INTO `AppWeb_equipmenttype` (`id`, `type`) VALUES
	(1, 'surfboard'),
	(2, 'leash'),
	(3, 'surfsuit');

-- Listage de la structure de table yala_surf. AppWeb_forum
CREATE TABLE IF NOT EXISTS `AppWeb_forum` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `surf_spot_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `surf_spot_id` (`surf_spot_id`),
  CONSTRAINT `AppWeb_forum_surf_spot_id_e651e3a0_fk_AppWeb_surfspot_id` FOREIGN KEY (`surf_spot_id`) REFERENCES `AppWeb_surfspot` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table yala_surf.AppWeb_forum : ~6 rows (environ)
INSERT INTO `AppWeb_forum` (`id`, `surf_spot_id`) VALUES
	(1, 4),
	(2, 5),
	(5, 6),
	(6, 7),
	(3, 8),
	(4, 9);

-- Listage de la structure de table yala_surf. AppWeb_lessonschedule
CREATE TABLE IF NOT EXISTS `AppWeb_lessonschedule` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `start_time` time(6) NOT NULL,
  `end_time` time(6) NOT NULL,
  `day` date NOT NULL,
  `surf_club_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `AppWeb_lessonschedul_surf_club_id_bdd12258_fk_AppWeb_su` (`surf_club_id`),
  CONSTRAINT `AppWeb_lessonschedul_surf_club_id_bdd12258_fk_AppWeb_su` FOREIGN KEY (`surf_club_id`) REFERENCES `AppWeb_surfclub` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table yala_surf.AppWeb_lessonschedule : ~65 rows (environ)
INSERT INTO `AppWeb_lessonschedule` (`id`, `start_time`, `end_time`, `day`, `surf_club_id`) VALUES
	(1, '02:59:22.000000', '02:59:26.000000', '2028-09-21', 5),
	(4, '08:00:00.000000', '10:00:00.000000', '2024-09-20', 5),
	(5, '11:00:00.000000', '14:00:00.000000', '2024-09-15', 5),
	(6, '15:00:00.000000', '16:30:00.000000', '2024-09-23', 5),
	(7, '09:00:00.000000', '11:30:00.000000', '2024-09-10', 6),
	(8, '13:00:00.000000', '16:00:00.000000', '2024-09-11', 6),
	(9, '17:00:00.000000', '19:00:00.000000', '2024-09-12', 6),
	(10, '08:30:00.000000', '10:30:00.000000', '2024-09-10', 7),
	(11, '12:00:00.000000', '13:30:00.000000', '2024-09-11', 7),
	(12, '14:00:00.000000', '17:00:00.000000', '2024-09-12', 7),
	(13, '07:00:00.000000', '09:00:00.000000', '2024-09-10', 8),
	(14, '10:30:00.000000', '12:30:00.000000', '2024-09-11', 8),
	(15, '14:00:00.000000', '16:30:00.000000', '2024-09-12', 8),
	(16, '08:00:00.000000', '09:30:00.000000', '2024-09-10', 9),
	(17, '11:00:00.000000', '13:00:00.000000', '2024-09-11', 9),
	(18, '14:30:00.000000', '17:30:00.000000', '2024-09-12', 9),
	(19, '07:30:00.000000', '09:30:00.000000', '2024-09-10', 10),
	(20, '10:00:00.000000', '12:00:00.000000', '2024-09-11', 10),
	(21, '13:00:00.000000', '15:00:00.000000', '2024-09-12', 10),
	(22, '08:00:00.000000', '11:00:00.000000', '2024-09-10', 11),
	(23, '12:30:00.000000', '15:00:00.000000', '2024-09-11', 11),
	(24, '16:00:00.000000', '18:00:00.000000', '2024-09-12', 11),
	(25, '09:00:00.000000', '12:00:00.000000', '2024-09-10', 12),
	(26, '13:00:00.000000', '15:00:00.000000', '2024-09-11', 12),
	(27, '16:00:00.000000', '17:30:00.000000', '2024-09-12', 12),
	(28, '07:00:00.000000', '09:00:00.000000', '2024-09-10', 13),
	(29, '10:00:00.000000', '13:00:00.000000', '2024-09-11', 13),
	(30, '14:00:00.000000', '16:30:00.000000', '2024-09-12', 13),
	(31, '08:30:00.000000', '10:30:00.000000', '2024-09-10', 14),
	(32, '11:30:00.000000', '14:00:00.000000', '2024-09-11', 14),
	(33, '15:30:00.000000', '18:00:00.000000', '2024-09-12', 14),
	(34, '07:30:00.000000', '09:30:00.000000', '2024-09-10', 15),
	(35, '10:30:00.000000', '13:00:00.000000', '2024-09-11', 15),
	(36, '14:30:00.000000', '16:30:00.000000', '2024-09-12', 15),
	(37, '08:00:00.000000', '11:00:00.000000', '2024-09-10', 16),
	(38, '12:30:00.000000', '14:30:00.000000', '2024-09-11', 16),
	(39, '15:00:00.000000', '17:00:00.000000', '2024-09-12', 16),
	(40, '09:00:00.000000', '12:00:00.000000', '2024-09-10', 17),
	(41, '13:00:00.000000', '15:00:00.000000', '2024-09-11', 17),
	(42, '16:00:00.000000', '18:30:00.000000', '2024-09-12', 17),
	(43, '08:00:00.000000', '10:00:00.000000', '2024-09-10', 18),
	(44, '11:00:00.000000', '14:00:00.000000', '2024-09-11', 18),
	(45, '15:00:00.000000', '17:00:00.000000', '2024-09-12', 18),
	(46, '07:30:00.000000', '09:30:00.000000', '2024-09-10', 19),
	(47, '10:00:00.000000', '12:00:00.000000', '2024-09-11', 19),
	(48, '13:00:00.000000', '16:00:00.000000', '2024-09-12', 19),
	(49, '09:00:00.000000', '11:00:00.000000', '2024-09-10', 20),
	(50, '12:00:00.000000', '14:00:00.000000', '2024-09-11', 20),
	(51, '15:00:00.000000', '17:30:00.000000', '2024-09-12', 20),
	(52, '08:30:00.000000', '10:30:00.000000', '2024-09-10', 21),
	(53, '11:00:00.000000', '13:00:00.000000', '2024-09-11', 21),
	(54, '14:00:00.000000', '16:00:00.000000', '2024-09-12', 21),
	(55, '07:00:00.000000', '09:00:00.000000', '2024-09-10', 22),
	(56, '10:30:00.000000', '13:00:00.000000', '2024-09-11', 22),
	(57, '14:00:00.000000', '17:00:00.000000', '2024-09-12', 22),
	(58, '09:00:00.000000', '12:00:00.000000', '2024-09-10', 23),
	(59, '13:00:00.000000', '15:30:00.000000', '2024-09-11', 23),
	(60, '16:00:00.000000', '17:30:00.000000', '2024-09-12', 23),
	(61, '08:00:00.000000', '10:30:00.000000', '2024-09-10', 24),
	(62, '11:30:00.000000', '14:00:00.000000', '2024-09-11', 24),
	(63, '15:00:00.000000', '17:30:00.000000', '2024-09-12', 24),
	(64, '09:30:00.000000', '11:30:00.000000', '2024-09-10', 25),
	(65, '12:00:00.000000', '14:30:00.000000', '2024-09-11', 25),
	(66, '15:30:00.000000', '18:00:00.000000', '2024-09-12', 25),
	(67, '15:30:00.000000', '16:30:00.000000', '2024-09-14', 5);

-- Listage de la structure de table yala_surf. AppWeb_message
CREATE TABLE IF NOT EXISTS `AppWeb_message` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `content` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `forum_id` bigint NOT NULL,
  `sender_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `AppWeb_message_forum_id_e48167f1_fk_AppWeb_forum_id` (`forum_id`),
  KEY `AppWeb_message_sender_id_8b25e2a5_fk_AppWeb_surfer_id` (`sender_id`),
  CONSTRAINT `AppWeb_message_forum_id_e48167f1_fk_AppWeb_forum_id` FOREIGN KEY (`forum_id`) REFERENCES `AppWeb_forum` (`id`),
  CONSTRAINT `AppWeb_message_sender_id_8b25e2a5_fk_AppWeb_surfer_id` FOREIGN KEY (`sender_id`) REFERENCES `AppWeb_surfer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table yala_surf.AppWeb_message : ~5 rows (environ)
INSERT INTO `AppWeb_message` (`id`, `content`, `created_at`, `forum_id`, `sender_id`) VALUES
	(54, 'Salut les gars  ! \nQuelqu\'un va surfer demain ??', '2024-09-10 10:35:35.038870', 1, 12),
	(55, 'Peut etre moi !', '2024-09-10 10:39:35.147026', 1, 13),
	(56, 'Parfait je part vers 8h', '2024-09-10 10:40:59.500818', 1, 12),
	(57, 'ok let\'s goo!', '2024-09-10 10:41:38.157606', 1, 13),
	(58, 'moi je viens vers 14h après les cours', '2024-09-10 10:43:23.546671', 1, 14);

-- Listage de la structure de table yala_surf. AppWeb_monitor
CREATE TABLE IF NOT EXISTS `AppWeb_monitor` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `birthday` date NOT NULL,
  `active` tinyint(1) NOT NULL,
  `photo` varchar(100) DEFAULT NULL,
  `surf_club_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `AppWeb_monitor_surf_club_id_d89f9996_fk_AppWeb_surfclub_id` (`surf_club_id`),
  CONSTRAINT `AppWeb_monitor_surf_club_id_d89f9996_fk_AppWeb_surfclub_id` FOREIGN KEY (`surf_club_id`) REFERENCES `AppWeb_surfclub` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=80 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table yala_surf.AppWeb_monitor : ~67 rows (environ)
INSERT INTO `AppWeb_monitor` (`id`, `first_name`, `last_name`, `birthday`, `active`, `photo`, `surf_club_id`) VALUES
	(7, 'Yassin', 'Lahfaouti', '2004-04-12', 1, 'uploads/ga1_K199efL.jpg', 5),
	(8, 'Marouane', 'lklech', '2001-03-11', 1, 'uploads/ga3_kDk3SFD.jpg', 5),
	(14, 'zineb', 'Bourich', '2001-11-05', 1, 'uploads/fille2.jpg', 5),
	(15, 'Sarah', 'Bennani', '1999-02-14', 1, 'uploads/fille1_yhTzPEL.jpg', 6),
	(16, 'Mehdi', 'Toumi', '1998-12-05', 1, 'uploads/ga3_zFYDQrR.jpg', 6),
	(17, 'Omar', 'El Hariri', '2000-03-28', 0, 'uploads/ga1_U6Fjyv2.jpg', 6),
	(18, 'Khadija', 'El Mansouri', '1997-05-21', 1, 'uploads/fille2_YGBSGLq.jpg', 7),
	(19, 'Rachid', 'El Ghazali', '2001-08-15', 0, 'uploads/ga2.jpg', 7),
	(20, 'Lina', 'Bouzaid', '1998-09-30', 1, 'uploads/fille1_lDZovuL.jpg', 7),
	(21, 'Said', 'Bouazza', '2002-02-19', 1, 'uploads/ga2_oRPD6a0.jpg', 8),
	(22, 'Noura', 'Farissi', '2000-01-08', 1, 'uploads/fille2_MfFsX14.jpg', 8),
	(23, 'Ayoub', 'Karim', '1999-03-14', 0, 'uploads/ga1_7UCwasE.jpg', 8),
	(24, 'Youssef', 'El Madi', '2003-09-25', 1, 'uploads/ga3_soJxbg1.jpg', 8),
	(25, 'Meryem', 'Zaidi', '2000-10-11', 1, 'uploads/fille2_kuzWvEK.jpg', 9),
	(26, 'Adil', 'Souissi', '1997-04-17', 1, 'uploads/ga3_zT39zj5.jpg', 9),
	(27, 'Fouad', 'Idrissi', '2001-07-19', 0, 'uploads/ga1_BnkvNlc.jpg', 9),
	(28, 'Samir', 'Alaoui', '1999-03-22', 1, 'uploads/ga3_Lt8a5Hj.jpg', 10),
	(29, 'Amina', 'Ben Salah', '1998-01-11', 0, 'uploads/fille1_9e4183D.jpg', 10),
	(30, 'Ismail', 'Zarhouni', '2002-09-29', 0, 'uploads/ga2_4rlBNZ4.jpg', 10),
	(31, 'Oussama', 'Lahlou', '2001-06-24', 0, 'uploads/ga2_775FpDb.jpg', 11),
	(32, 'Imane', 'Nouichi', '1997-11-13', 1, 'uploads/fille2_gjGxSp3.jpg', 11),
	(33, 'Rania', 'Touhami', '2003-05-07', 1, 'uploads/fille1_qwMuGHU.jpg', 11),
	(34, 'Reda', 'Hassani', '1999-08-01', 1, '', 12),
	(35, 'Kenza', 'Bennani', '1998-10-23', 0, NULL, 12),
	(36, 'Hamza', 'Kettani', '2000-06-12', 1, '', 12),
	(37, 'Fayçal', 'Azzouzi', '2001-09-05', 1, 'uploads/ga3_wjJng7s.jpg', 13),
	(38, 'Sara', 'Mouline', '2002-04-30', 1, 'uploads/fille1_YJpwe5A.jpg', 13),
	(39, 'Hassan', 'Majidi', '1997-12-22', 1, 'uploads/ga1_IEmsFqg.jpg', 13),
	(40, 'Youssef', 'Ghani', '2001-11-02', 1, 'uploads/ga2_tvAmG21.jpg', 14),
	(41, 'Karima', 'Essaidi', '2000-01-10', 0, 'uploads/fille2_tb8yXsk.jpg', 14),
	(42, 'Adil', 'Amraoui', '1999-07-18', 1, 'uploads/ga3_5JHqnvh.jpg', 14),
	(43, 'Soufiane', 'El Khoufi', '2003-02-12', 0, 'uploads/ga1_QHOXHpb.jpg', 15),
	(44, 'Aicha', 'Berraoui', '1998-03-27', 1, 'uploads/fille1_yy1OK62.jpg', 15),
	(45, 'Nabil', 'Tazi', '1999-05-25', 1, 'uploads/ga2_PlyGifR.jpg', 15),
	(46, 'Mehdi', 'Lalami', '1997-06-15', 1, 'uploads/ga2_NIVwP2I.jpg', 16),
	(47, 'Fatima', 'Bousfiha', '2002-07-20', 0, 'uploads/fille2_JLTIIrq.jpg', 16),
	(48, 'Ali', 'Toubkal', '2000-08-19', 1, 'uploads/ga3_jwcuidM.jpg', 16),
	(49, 'Yassine', 'Ouadghiri', '1997-12-04', 1, 'uploads/ga3_xcZCmJ4.jpg', 17),
	(50, 'Rim', 'Charif', '1999-11-08', 0, 'uploads/fille2_PQKPspr.jpg', 17),
	(51, 'Samira', 'Amin', '2002-03-11', 1, 'uploads/fille1_NdSZnGt.jpg', 17),
	(52, 'Nizar', 'Chafik', '1998-05-18', 1, 'uploads/ga1_DNWiRkB.jpg', 18),
	(53, 'Laila', 'El Fassi', '2000-02-23', 1, 'uploads/fille1_0tgJD2C.jpg', 18),
	(54, 'Mohammed', 'Rokni', '1999-06-17', 0, 'uploads/ga2_ccdusTe.jpg', 18),
	(55, 'Karim', 'Ouhamou', '2002-07-13', 1, 'uploads/ga3_FURgADz.jpg', 19),
	(56, 'Hanane', 'Abderrahmane', '1999-04-09', 1, 'uploads/fille2_Y7X0GbL.jpg', 19),
	(57, 'Walid', 'Sefiani', '1998-11-21', 0, 'uploads/ga2_uLOycjb.jpg', 19),
	(58, 'Souhail', 'Benyahia', '2000-06-29', 1, 'uploads/ga1_H0ntyae.jpg', 20),
	(59, 'Manal', 'Tazi', '2003-09-10', 0, 'uploads/fille1_MwG84lk.jpg', 20),
	(60, 'Zineb', 'El Bali', '1998-10-15', 1, 'uploads/fille2_5xwVHc2.jpg', 20),
	(61, 'Salma', 'El Kheir', '1999-02-24', 0, 'uploads/fille2_PShbbU3.jpg', 21),
	(62, 'Anas', 'Kabbaj', '2002-05-09', 1, 'uploads/ga3_Rk2wI3n.jpg', 21),
	(63, 'Rachid', 'Bensouda', '1997-10-31', 1, 'uploads/ga1_Ur25CTT.jpg', 21),
	(64, 'Ayoub', 'El Alami', '2000-07-12', 0, 'uploads/ga2_8W9zP04.jpg', 22),
	(65, 'Fatima', 'Hariri', '1998-04-25', 1, 'uploads/fille1_IgCCgim.jpg', 22),
	(66, 'Younes', 'Maarouf', '2001-03-28', 1, 'uploads/ga1_MSkAN4J.jpg', 22),
	(67, 'Khalid', 'Benhar', '1999-01-14', 0, 'uploads/ga3.jpg', 23),
	(68, 'Ikram', 'Tarfaya', '2000-02-21', 1, 'uploads/fille1.jpg', 23),
	(69, 'Ahmed', 'Naciri', '1997-11-30', 1, 'uploads/ga1.jpg', 23),
	(70, 'Aymane', 'Baroudi', '2002-12-17', 0, 'uploads/ga3_XWmTuYi.jpg', 24),
	(71, 'Sara', 'Majdoubi', '1998-06-22', 1, 'uploads/fille1_Kk44YRg.jpg', 24),
	(72, 'Mohamed', 'El Ouali', '2001-10-11', 1, 'uploads/fille2_pummeXr.jpg', 24),
	(73, 'Hassan', 'Ouaziz', '2003-01-29', 0, NULL, 25),
	(74, 'Laila', 'Essamadi', '1998-09-05', 1, '', 25),
	(75, 'Walid', 'Bennani', '2002-04-14', 1, '', 25),
	(76, 'Ines', 'Lafi', '2004-01-25', 0, 'uploads/fille1_oxOctYX.jpg', 5),
	(77, 'Salah Eddine', 'Ouramdan', '2003-02-13', 0, 'uploads/ga1_bXEtV4Y.jpg', 7),
	(78, 'Amina', 'Fakir', '2002-06-23', 0, 'uploads/woman-with-surfboard-beach.jpg', 5);

-- Listage de la structure de table yala_surf. AppWeb_order
CREATE TABLE IF NOT EXISTS `AppWeb_order` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order_date` date NOT NULL,
  `total_price` decimal(10,2) NOT NULL,
  `surf_club_id` bigint NOT NULL,
  `surfer_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `AppWeb_order_surf_club_id_77d1b6e3_fk_AppWeb_surfclub_id` (`surf_club_id`),
  KEY `AppWeb_order_surfer_id_17edf075_fk_AppWeb_surfer_id` (`surfer_id`),
  CONSTRAINT `AppWeb_order_surf_club_id_77d1b6e3_fk_AppWeb_surfclub_id` FOREIGN KEY (`surf_club_id`) REFERENCES `AppWeb_surfclub` (`id`),
  CONSTRAINT `AppWeb_order_surfer_id_17edf075_fk_AppWeb_surfer_id` FOREIGN KEY (`surfer_id`) REFERENCES `AppWeb_surfer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table yala_surf.AppWeb_order : ~4 rows (environ)
INSERT INTO `AppWeb_order` (`id`, `order_date`, `total_price`, `surf_club_id`, `surfer_id`) VALUES
	(8, '2024-09-10', 4172.00, 5, 12),
	(9, '2024-09-10', 1650.00, 11, 12),
	(10, '2024-09-10', 640.00, 10, 12),
	(11, '2024-09-10', 1000.00, 5, 13);

-- Listage de la structure de table yala_surf. AppWeb_orderitem
CREATE TABLE IF NOT EXISTS `AppWeb_orderitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantity` int unsigned NOT NULL,
  `equipment_id` bigint NOT NULL,
  `order_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `AppWeb_orderitem_equipment_id_254f74cf_fk_AppWeb_equipment_id` (`equipment_id`),
  KEY `AppWeb_orderitem_order_id_dd38b9ce_fk_AppWeb_order_id` (`order_id`),
  CONSTRAINT `AppWeb_orderitem_equipment_id_254f74cf_fk_AppWeb_equipment_id` FOREIGN KEY (`equipment_id`) REFERENCES `AppWeb_equipment` (`id`),
  CONSTRAINT `AppWeb_orderitem_order_id_dd38b9ce_fk_AppWeb_order_id` FOREIGN KEY (`order_id`) REFERENCES `AppWeb_order` (`id`),
  CONSTRAINT `AppWeb_orderitem_chk_1` CHECK ((`quantity` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table yala_surf.AppWeb_orderitem : ~5 rows (environ)
INSERT INTO `AppWeb_orderitem` (`id`, `quantity`, `equipment_id`, `order_id`) VALUES
	(9, 4, 12, 8),
	(10, 3, 16, 8),
	(11, 3, 52, 9),
	(12, 1, 46, 10),
	(13, 2, 16, 11);

-- Listage de la structure de table yala_surf. AppWeb_photo
CREATE TABLE IF NOT EXISTS `AppWeb_photo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image` varchar(100) DEFAULT NULL,
  `equipment_id` bigint DEFAULT NULL,
  `surf_spot_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `AppWeb_photo_equipment_id_6cc8780e_fk_AppWeb_equipment_id` (`equipment_id`),
  KEY `AppWeb_photo_surf_spot_id_ccdb52fe_fk_AppWeb_surfspot_id` (`surf_spot_id`),
  CONSTRAINT `AppWeb_photo_equipment_id_6cc8780e_fk_AppWeb_equipment_id` FOREIGN KEY (`equipment_id`) REFERENCES `AppWeb_equipment` (`id`),
  CONSTRAINT `AppWeb_photo_surf_spot_id_ccdb52fe_fk_AppWeb_surfspot_id` FOREIGN KEY (`surf_spot_id`) REFERENCES `AppWeb_surfspot` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=221 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table yala_surf.AppWeb_photo : ~194 rows (environ)
INSERT INTO `AppWeb_photo` (`id`, `image`, `equipment_id`, `surf_spot_id`) VALUES
	(27, 'uploads/taghazout2.webp', NULL, 4),
	(28, 'uploads/taghazout1.jpg', NULL, 4),
	(29, 'uploads/taghazout3.jpg', NULL, 4),
	(30, 'uploads/bouznika1.jpg', NULL, 6),
	(31, 'uploads/bouznika2.jpg', NULL, 6),
	(32, 'uploads/bouznika3.jpg', NULL, 6),
	(33, 'uploads/banana1.jpg', NULL, 8),
	(34, 'uploads/banana2.png', NULL, 8),
	(35, 'uploads/banana3.jpg', NULL, 8),
	(36, 'uploads/killer1.jpg', NULL, 9),
	(37, 'uploads/killer2.jpg', NULL, 9),
	(38, 'uploads/oudaya.jpg', NULL, 7),
	(39, 'uploads/oudaya2.jpg', NULL, 7),
	(40, 'uploads/anza3.jpg', NULL, 5),
	(41, 'uploads/anza1_o8EDhkM.webp', NULL, 5),
	(42, 'uploads/planche1.png', 12, NULL),
	(43, 'uploads/planche3.png', 12, NULL),
	(44, 'uploads/planche2.png', 12, NULL),
	(45, 'uploads/planche4.jpg', 14, NULL),
	(46, 'uploads/planche6.jpg', 14, NULL),
	(47, 'uploads/planche5.jpg', 14, NULL),
	(48, 'uploads/5040_A00_2_PACK_680x_crop_center.webp', 15, NULL),
	(49, 'uploads/5040_A00_1_PACK_680x_crop_center.webp', 15, NULL),
	(50, 'uploads/combinaison_location.jpg', 21, NULL),
	(51, 'uploads/combine_loc.webp', 21, NULL),
	(52, 'uploads/combinaison_buy.png', 20, NULL),
	(53, 'uploads/combine_b.webp', 20, NULL),
	(54, 'uploads/palcnhe_loc.jpg', 17, NULL),
	(55, 'uploads/planche_location.jpg', 17, NULL),
	(56, 'uploads/buy_planche.jpg', 16, NULL),
	(57, 'uploads/buy_planchee.jpg', 16, NULL),
	(58, 'uploads/fcs-ii-performer-neo-glass-ecoblend-extra-small-tri.jpg', 18, NULL),
	(59, 'uploads/ion-leash-de-surf-core-petrol-turquoise.jpg', 19, NULL),
	(60, 'uploads/buy_planche_gyxwZgw.jpg', 22, NULL),
	(61, 'uploads/buy_planchee_wyWT2Tv.jpg', 22, NULL),
	(62, 'uploads/planche_location_ZFgUhFt.jpg', 23, NULL),
	(63, 'uploads/palcnhe_loc_egRzkfi.jpg', 23, NULL),
	(64, 'uploads/fcs-ii-performer-neo-glass-ecoblend-extra-small-tri_7i88cdh.jpg', 24, NULL),
	(65, 'uploads/ion-leash-de-surf-core-petrol-turquoise_QClavP2.jpg', 25, NULL),
	(66, 'uploads/combine_b_fPtJdQG.webp', 26, NULL),
	(67, 'uploads/combinaison_buy_nLqgOWX.png', 26, NULL),
	(68, 'uploads/combinaison_location_kWdWhaq.jpg', 27, NULL),
	(69, 'uploads/combine_loc_YXhosOU.webp', 27, NULL),
	(70, 'uploads/buy_planche_fSHMJOh.jpg', 28, NULL),
	(71, 'uploads/buy_planchee_nGxr9jJ.jpg', 28, NULL),
	(72, 'uploads/planche_location_1gGUst2.jpg', 29, NULL),
	(73, 'uploads/palcnhe_loc_Nyaops8.jpg', 29, NULL),
	(74, 'uploads/ion-leash-de-surf-core-petrol-turquoise_HLStO8N.jpg', 30, NULL),
	(75, 'uploads/ion-leash-de-surf-core-petrol-turquoise_zTBBsMZ.jpg', 31, NULL),
	(76, 'uploads/combine_b_A7ceHXl.webp', 32, NULL),
	(77, 'uploads/combinaison_buy_XUDfMi8.png', 32, NULL),
	(78, 'uploads/combinaison_location_clHDJrP.jpg', 33, NULL),
	(79, 'uploads/combine_loc_0aJfEXV.webp', 33, NULL),
	(80, 'uploads/planche_location_dogirl1.jpg', 34, NULL),
	(81, 'uploads/palcnhe_loc_S3z3yFC.jpg', 34, NULL),
	(82, 'uploads/buy_planche_TNxC9qH.jpg', 35, NULL),
	(83, 'uploads/buy_planchee_JqABhsK.jpg', 35, NULL),
	(84, 'uploads/ion-leash-de-surf-core-petrol-turquoise_66SG7Lt.jpg', 36, NULL),
	(85, 'uploads/fcs-ii-performer-neo-glass-ecoblend-extra-small-tri_A8bqFW1.jpg', 37, NULL),
	(86, 'uploads/combinaison_location_3WIQlZY.jpg', 38, NULL),
	(87, 'uploads/combine_loc_wfXeNZo.webp', 38, NULL),
	(88, 'uploads/combine_b_zYTt0ms.webp', 39, NULL),
	(89, 'uploads/combinaison_buy_kfBphtJ.png', 39, NULL),
	(90, 'uploads/buy_planchee_Nzt95aO.jpg', 40, NULL),
	(91, 'uploads/buy_planche_whv1C8l.jpg', 40, NULL),
	(92, 'uploads/planche_location_BmDzGL7.jpg', 41, NULL),
	(93, 'uploads/palcnhe_loc_kUM7I3Z.jpg', 41, NULL),
	(94, 'uploads/ion-leash-de-surf-core-petrol-turquoise_cwUhiSa.jpg', 42, NULL),
	(95, 'uploads/combinaison_location_eTbKFtS.jpg', 44, NULL),
	(96, 'uploads/combine_loc_gC9ND3F.webp', 44, NULL),
	(97, 'uploads/combine_b_Xp81rTl.webp', 45, NULL),
	(98, 'uploads/combinaison_buy_ofhijGl.png', 45, NULL),
	(99, 'uploads/buy_planchee_FtkPSfU.jpg', 46, NULL),
	(100, 'uploads/buy_planche_SFtv2fx.jpg', 46, NULL),
	(101, 'uploads/palcnhe_loc_NYZf4n8.jpg', 47, NULL),
	(102, 'uploads/planche_location_lMKwmnL.jpg', 47, NULL),
	(103, 'uploads/ion-leash-de-surf-core-petrol-turquoise_QqKTWe7.jpg', 48, NULL),
	(104, 'uploads/leash.webp', 49, NULL),
	(105, 'uploads/combinaison_buy_sCLnoON.png', 50, NULL),
	(106, 'uploads/combine_b_ru9zRRk.webp', 50, NULL),
	(107, 'uploads/combinaison_location_jHEvSeO.jpg', 51, NULL),
	(108, 'uploads/combine_loc_rED3FUf.webp', 51, NULL),
	(109, 'uploads/buy_planchee_qZTRNTQ.jpg', 52, NULL),
	(110, 'uploads/buy_planche_AHJCmWs.jpg', 52, NULL),
	(111, 'uploads/planche_location_liTUF1m.jpg', 53, NULL),
	(112, 'uploads/palcnhe_loc_H2p05h6.jpg', 53, NULL),
	(113, 'uploads/ion-leash-de-surf-core-petrol-turquoise_i6o39ye.jpg', 54, NULL),
	(114, 'uploads/leash_CgtNhHv.webp', 55, NULL),
	(115, 'uploads/combine_b_vTbMTye.webp', 56, NULL),
	(116, 'uploads/combinaison_buy_0bvx8ZH.png', 56, NULL),
	(117, 'uploads/combinaison_location_QyHV97y.jpg', 57, NULL),
	(118, 'uploads/combine_loc_0YVAhGG.webp', 57, NULL),
	(119, 'uploads/buy_planchee_UKsOtTG.jpg', 64, NULL),
	(120, 'uploads/buy_planche_GjwCaEn.jpg', 64, NULL),
	(121, 'uploads/palcnhe_loc_ZIJ03yp.jpg', 65, NULL),
	(122, 'uploads/planche_location_THVLFdg.jpg', 65, NULL),
	(123, 'uploads/ion-leash-de-surf-core-petrol-turquoise_WZK79QL.jpg', 66, NULL),
	(124, 'uploads/leash_lF5iWeZ.webp', 67, NULL),
	(125, 'uploads/combinaison_location_RFR7y8i.jpg', 68, NULL),
	(126, 'uploads/combine_loc_E62EKmj.webp', 68, NULL),
	(127, 'uploads/combine_b_W85BbDA.webp', 69, NULL),
	(128, 'uploads/combinaison_buy_rP9CTsA.png', 69, NULL),
	(129, 'uploads/buy_planchee_x2vhOHy.jpg', 70, NULL),
	(130, 'uploads/buy_planche_XxpabKp.jpg', 70, NULL),
	(131, 'uploads/planche_location_9jiIv8P.jpg', 71, NULL),
	(132, 'uploads/palcnhe_loc_Z7H6jJJ.jpg', 71, NULL),
	(133, 'uploads/ion-leash-de-surf-core-petrol-turquoise_gNynTEm.jpg', 72, NULL),
	(134, 'uploads/leash_ZuglOEP.webp', 73, NULL),
	(135, 'uploads/combine_b_lhv0XPb.webp', 74, NULL),
	(136, 'uploads/combinaison_buy_dygkpTE.png', 74, NULL),
	(137, 'uploads/combinaison_location_odWhXcv.jpg', 75, NULL),
	(138, 'uploads/combine_loc_59NSiio.webp', 75, NULL),
	(139, 'uploads/buy_planchee_vN6VRBW.jpg', 76, NULL),
	(140, 'uploads/buy_planche_vKXuc5j.jpg', 76, NULL),
	(141, 'uploads/planche_location_vGWfaUr.jpg', 77, NULL),
	(142, 'uploads/palcnhe_loc_t9lvD4C.jpg', 77, NULL),
	(143, 'uploads/leash_pa2eN7n.webp', 78, NULL),
	(144, 'uploads/ion-leash-de-surf-core-petrol-turquoise_uT6v08s.jpg', 79, NULL),
	(145, 'uploads/combine_b_QE1IXdf.webp', 80, NULL),
	(146, 'uploads/combinaison_buy_GBDcpTT.png', 80, NULL),
	(147, 'uploads/combinaison_location_dmeDsl0.jpg', 81, NULL),
	(148, 'uploads/combine_loc_61Bx0x7.webp', 81, NULL),
	(149, 'uploads/buy_planchee_5ML23MI.jpg', 82, NULL),
	(150, 'uploads/buy_planche_JPomos8.jpg', 82, NULL),
	(151, 'uploads/planche_location_wnaOtV2.jpg', 83, NULL),
	(152, 'uploads/palcnhe_loc_w8Jn1uC.jpg', 83, NULL),
	(153, 'uploads/leash_SISEi88.webp', 85, NULL),
	(154, 'uploads/ion-leash-de-surf-core-petrol-turquoise_2TuTQpo.jpg', 84, NULL),
	(155, 'uploads/combinaison_location_jRYPUhf.jpg', 86, NULL),
	(156, 'uploads/combine_loc_2DPBmK3.webp', 86, NULL),
	(157, 'uploads/combine_b_B9yB275.webp', 87, NULL),
	(158, 'uploads/combinaison_buy_iquk2dE.png', 87, NULL),
	(159, 'uploads/buy_planchee_0DVkedF.jpg', 88, NULL),
	(160, 'uploads/buy_planche_Q96BDiF.jpg', 88, NULL),
	(161, 'uploads/planche_location_K6wJ6MZ.jpg', 89, NULL),
	(162, 'uploads/palcnhe_loc_a5T8sGP.jpg', 89, NULL),
	(163, 'uploads/leash_zNWqrtT.webp', 90, NULL),
	(164, 'uploads/ion-leash-de-surf-core-petrol-turquoise_7NQmjYu.jpg', 91, NULL),
	(165, 'uploads/combine_b_wZ5vIbT.webp', 92, NULL),
	(166, 'uploads/combinaison_buy_xuS5r58.png', 92, NULL),
	(167, 'uploads/combinaison_location_bLOeZ3t.jpg', 93, NULL),
	(168, 'uploads/combine_loc_PFhJZdu.webp', 93, NULL),
	(169, 'uploads/buy_planchee_yjfNpYT.jpg', 94, NULL),
	(170, 'uploads/buy_planche_AOa5WXn.jpg', 94, NULL),
	(171, 'uploads/planche_location_rn698rZ.jpg', 95, NULL),
	(172, 'uploads/palcnhe_loc_sXTesPu.jpg', 95, NULL),
	(173, 'uploads/leash_uCBCuHi.webp', 96, NULL),
	(174, 'uploads/ion-leash-de-surf-core-petrol-turquoise_rJBWzGN.jpg', 97, NULL),
	(175, 'uploads/combinaison_buy_WPmdciq.png', 98, NULL),
	(176, 'uploads/combinaison_location_BTqO4cx.jpg', 99, NULL),
	(177, 'uploads/combine_loc_k4M7Or6.webp', 99, NULL),
	(178, 'uploads/buy_planchee_pZ0IGqS.jpg', 100, NULL),
	(179, 'uploads/buy_planche_kWoXe0g.jpg', 100, NULL),
	(180, 'uploads/planche_location_yuAuLXd.jpg', 101, NULL),
	(181, 'uploads/leash_gwF5vfW.webp', 102, NULL),
	(182, 'uploads/ion-leash-de-surf-core-petrol-turquoise_lZq6e0f.jpg', 103, NULL),
	(183, 'uploads/combine_b_2PObges.webp', 104, NULL),
	(184, 'uploads/combinaison_buy_4Z8RSTK.png', 104, NULL),
	(185, 'uploads/combinaison_location_xHiNMZz.jpg', 105, NULL),
	(186, 'uploads/combine_loc_nVwjs8r.webp', 105, NULL),
	(187, 'uploads/buy_planchee_edjwXCS.jpg', 106, NULL),
	(188, 'uploads/buy_planche_k7BUBtC.jpg', 106, NULL),
	(189, 'uploads/palcnhe_loc_ddv9xxZ.jpg', 107, NULL),
	(190, 'uploads/leash_kpz3uiF.webp', 108, NULL),
	(191, 'uploads/ion-leash-de-surf-core-petrol-turquoise_ZzeXX4e.jpg', 109, NULL),
	(192, 'uploads/combinaison_buy_XVd0nnb.png', 110, NULL),
	(193, 'uploads/combinaison_location_KXbODGM.jpg', 110, NULL),
	(194, 'uploads/combine_b_zYVFS10.webp', 117, NULL),
	(195, 'uploads/combinaison_buy_oJkXm1A.png', 117, NULL),
	(196, 'uploads/combine_loc_037hMR1.webp', 112, NULL),
	(197, 'uploads/ion-leash-de-surf-core-petrol-turquoise_98U6lFe.jpg', 114, NULL),
	(198, 'uploads/buy_planchee_QzOsBJV.jpg', 118, NULL),
	(199, 'uploads/buy_planche_yOoKSoB.jpg', 118, NULL),
	(200, 'uploads/planche_location_Nhgpwk5.jpg', 119, NULL),
	(201, 'uploads/palcnhe_loc_b4PR7d9.jpg', 119, NULL),
	(202, 'uploads/leash_bIQ6ZL5.webp', 120, NULL),
	(203, 'uploads/ion-leash-de-surf-core-petrol-turquoise_AnDDckK.jpg', 121, NULL),
	(204, 'uploads/combine_b_J3hBDlQ.webp', 122, NULL),
	(205, 'uploads/combinaison_buy_QqGT9lA.png', 122, NULL),
	(206, 'uploads/combine_loc_efbTCas.webp', 123, NULL),
	(207, 'uploads/combinaison_location_W0kE5LY.jpg', 123, NULL),
	(208, 'uploads/palcnhe_loc_w8TmPGF.jpg', 124, NULL),
	(209, 'uploads/buy_planchee_TTj8oob.jpg', 125, NULL),
	(210, 'uploads/ion-leash-de-surf-core-petrol-turquoise_gACUGmn.jpg', 126, NULL),
	(211, 'uploads/leash_9cQDTCt.webp', 127, NULL),
	(212, 'uploads/planche_location_FmZNusq.jpg', 128, NULL),
	(213, 'uploads/planche_location_ED0XM63.jpg', 130, NULL),
	(214, 'uploads/buy_planche_zrMtODL.jpg', 131, NULL),
	(215, 'uploads/leash_oDLyM5i.webp', 132, NULL),
	(216, 'uploads/ion-leash-de-surf-core-petrol-turquoise_JJL9khk.jpg', 133, NULL),
	(217, 'uploads/combine_b_VRttsNx.webp', 135, NULL),
	(218, 'uploads/combinaison_buy_HOlzbXL.png', 135, NULL),
	(219, 'uploads/combinaison_location_BgCcjDm.jpg', 134, NULL),
	(220, 'uploads/combine_loc_3JYt4dx.webp', 134, NULL);

-- Listage de la structure de table yala_surf. AppWeb_surfclub
CREATE TABLE IF NOT EXISTS `AppWeb_surfclub` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `logo` varchar(100) DEFAULT NULL,
  `surf_spot_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `AppWeb_surfclub_surf_spot_id_3de9033c_fk_AppWeb_surfspot_id` (`surf_spot_id`),
  CONSTRAINT `AppWeb_surfclub_surf_spot_id_3de9033c_fk_AppWeb_surfspot_id` FOREIGN KEY (`surf_spot_id`) REFERENCES `AppWeb_surfspot` (`id`),
  CONSTRAINT `AppWeb_surfclub_user_id_5f4f401e_fk_AppWeb_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `AppWeb_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table yala_surf.AppWeb_surfclub : ~21 rows (environ)
INSERT INTO `AppWeb_surfclub` (`id`, `name`, `logo`, `surf_spot_id`, `user_id`) VALUES
	(5, 'Anchor Riders Club', 'uploads/anchor_poinr.webp', 4, 20),
	(6, 'Wave Masters', 'uploads/anchor2.webp', 4, 21),
	(7, 'Taghazout Surf School', 'uploads/anchor3.webp', 4, 22),
	(8, 'Point Break Surf Club', 'uploads/9664abea-5c73-427e-8965-9ffa963a72c2.webp', 4, 23),
	(9, 'Anza Waves', 'uploads/anza1.webp', 5, 24),
	(10, 'Big Wave Riders', 'uploads/anza2.webp', 5, 25),
	(11, 'Ocean Spirit Surf Club', 'uploads/anza3.webp', 5, 26),
	(12, 'Surf Anza Pro', 'uploads/anza4.webp', 5, 27),
	(13, 'Crique Riders', 'uploads/crique1.webp', 6, 28),
	(14, 'Crique Surf School', 'uploads/crique2.webp', 6, 29),
	(15, 'Wave Breakers', 'uploads/crique3.webp', 6, 30),
	(16, 'Ocean Masters', 'uploads/crique4.webp', 6, 31),
	(17, 'Oudayas Surf Club', 'uploads/oudaya1.webp', 7, 32),
	(18, 'Rabat Surf Riders', 'uploads/oudaya2.webp', 7, 33),
	(19, 'Kasbah Surf School', 'uploads/oudaya3.webp', 7, 35),
	(20, 'Banana Riders', 'uploads/banana1.webp', 8, 36),
	(21, 'Banana Surf School', 'uploads/banana2.webp', 8, 37),
	(22, 'Ocean Banana', 'uploads/banana3.webp', 8, 38),
	(23, 'Killer Waves Surf Club', 'uploads/killer1.webp', 9, 39),
	(24, 'Point Breakers', 'uploads/killer2.webp', 9, 40),
	(25, 'Killer Point Surf Academy', 'uploads/killer3.webp', 9, 41);

-- Listage de la structure de table yala_surf. AppWeb_surfer
CREATE TABLE IF NOT EXISTS `AppWeb_surfer` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `firstname` varchar(255) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `birthday` date NOT NULL,
  `level` varchar(50) NOT NULL,
  `photo` varchar(100) DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `AppWeb_surfer_user_id_a82142b3_fk_AppWeb_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `AppWeb_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table yala_surf.AppWeb_surfer : ~3 rows (environ)
INSERT INTO `AppWeb_surfer` (`id`, `firstname`, `lastname`, `birthday`, `level`, `photo`, `user_id`) VALUES
	(12, 'Salah Eddine', 'OR', '2003-02-13', 'advanced', 'uploads/WhatsApp_Image_2024-09-07_à_01.04.23_9c02826c.jpg', 34),
	(13, 'Seline', 'Hadil', '2003-08-27', 'beginner', 'uploads/woman-with-surfboard-beach_uCWgayQ.jpg', 42),
	(14, 'Ahmed', 'Likane', '2002-05-16', 'intermediate', 'uploads/ga1_HOW7Q9a.jpg', 43);

-- Listage de la structure de table yala_surf. AppWeb_surflesson
CREATE TABLE IF NOT EXISTS `AppWeb_surflesson` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `surfer_id` bigint NOT NULL,
  `surf_session_id` bigint NOT NULL,
  `total_price` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `AppWeb_surflesson_surf_session_id_4c72dfe7_fk_AppWeb_su` (`surf_session_id`),
  KEY `AppWeb_surflesson_surfer_id_f480a762_fk_AppWeb_surfer_id` (`surfer_id`),
  CONSTRAINT `AppWeb_surflesson_surf_session_id_4c72dfe7_fk_AppWeb_su` FOREIGN KEY (`surf_session_id`) REFERENCES `AppWeb_surfsession` (`id`),
  CONSTRAINT `AppWeb_surflesson_surfer_id_f480a762_fk_AppWeb_surfer_id` FOREIGN KEY (`surfer_id`) REFERENCES `AppWeb_surfer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table yala_surf.AppWeb_surflesson : ~5 rows (environ)
INSERT INTO `AppWeb_surflesson` (`id`, `surfer_id`, `surf_session_id`, `total_price`) VALUES
	(9, 12, 84, 58.00),
	(10, 12, 92, 34.00),
	(12, 12, 89, 20.00),
	(13, 12, 76, 38.00),
	(14, 13, 79, 34.00);

-- Listage de la structure de table yala_surf. AppWeb_surfsession
CREATE TABLE IF NOT EXISTS `AppWeb_surfsession` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `lesson_schedule_id` bigint NOT NULL,
  `monitor_id` bigint NOT NULL,
  `surf_club_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `AppWeb_surfsession_lesson_schedule_id_196d0ea4_fk_AppWeb_le` (`lesson_schedule_id`),
  KEY `AppWeb_surfsession_monitor_id_0f1a8e64_fk_AppWeb_monitor_id` (`monitor_id`),
  KEY `AppWeb_surfsession_surf_club_id_bd4b6262_fk_AppWeb_surfclub_id` (`surf_club_id`),
  CONSTRAINT `AppWeb_surfsession_lesson_schedule_id_196d0ea4_fk_AppWeb_le` FOREIGN KEY (`lesson_schedule_id`) REFERENCES `AppWeb_lessonschedule` (`id`),
  CONSTRAINT `AppWeb_surfsession_monitor_id_0f1a8e64_fk_AppWeb_monitor_id` FOREIGN KEY (`monitor_id`) REFERENCES `AppWeb_monitor` (`id`),
  CONSTRAINT `AppWeb_surfsession_surf_club_id_bd4b6262_fk_AppWeb_surfclub_id` FOREIGN KEY (`surf_club_id`) REFERENCES `AppWeb_surfclub` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=122 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table yala_surf.AppWeb_surfsession : ~44 rows (environ)
INSERT INTO `AppWeb_surfsession` (`id`, `lesson_schedule_id`, `monitor_id`, `surf_club_id`) VALUES
	(76, 1, 7, 5),
	(77, 4, 8, 5),
	(79, 6, 14, 5),
	(80, 7, 15, 6),
	(81, 8, 16, 6),
	(82, 10, 18, 7),
	(83, 11, 20, 7),
	(84, 13, 22, 8),
	(85, 15, 24, 8),
	(86, 15, 21, 8),
	(87, 16, 25, 9),
	(88, 17, 26, 9),
	(89, 19, 28, 10),
	(90, 23, 33, 11),
	(91, 22, 32, 11),
	(92, 25, 34, 12),
	(93, 26, 36, 12),
	(94, 28, 37, 13),
	(95, 30, 39, 13),
	(96, 29, 38, 13),
	(97, 31, 40, 14),
	(98, 32, 42, 14),
	(99, 34, 44, 15),
	(100, 35, 45, 15),
	(101, 37, 46, 16),
	(102, 39, 48, 16),
	(103, 40, 49, 17),
	(104, 42, 51, 17),
	(105, 43, 52, 18),
	(106, 44, 53, 18),
	(107, 46, 55, 19),
	(108, 47, 56, 19),
	(109, 49, 58, 20),
	(110, 51, 60, 20),
	(111, 52, 62, 21),
	(112, 53, 63, 21),
	(113, 57, 65, 22),
	(114, 55, 66, 22),
	(115, 58, 68, 23),
	(116, 60, 69, 23),
	(117, 62, 71, 24),
	(118, 63, 72, 24),
	(119, 64, 74, 25),
	(120, 65, 75, 25);

-- Listage de la structure de table yala_surf. AppWeb_surfspot
CREATE TABLE IF NOT EXISTS `AppWeb_surfspot` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `zip_code` varchar(20) NOT NULL,
  `address` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table yala_surf.AppWeb_surfspot : ~6 rows (environ)
INSERT INTO `AppWeb_surfspot` (`id`, `name`, `zip_code`, `address`, `description`, `latitude`, `longitude`) VALUES
	(4, 'Anchor Point', '99556', 'Taghazout, Morocco', 'Anchor Point is a legendary surf spot located near Taghazout, Morocco. Known for its long, right-hand point break, it offers world-class waves that can peel for hundreds of meters, providing thrilling rides for experienced surfers. The spot works best with a solid swell and is most famous during the winter months when the waves are at their best', 30.545224, -9.661369),
	(5, 'Anza', '80000', 'Agadir Morocco', 'Anza is a popular surf spot located just north of Agadir, Morocco. Known for its consistent waves, it attracts surfers of all levels throughout the year. The beach offers both left and right-hand breaks, making it a versatile spot for practicing different surf techniques. With a laid-back atmosphere and stunning views of the Atlantic Ocean, Anza is a favorite destination for both local and visiting surfers.', 30.449581, -9.661369),
	(6, 'La crique', '13100', 'Bouznika Morocco', 'La Crique in Bouznika, Morocco, is a hidden gem for surfers. Nestled between rocky cliffs, this surf spot offers clean, consistent waves that appeal to both beginners and experienced surfers. The secluded beach creates an intimate atmosphere, making it a perfect escape from the more crowded spots. With its beautiful natural surroundings and reliable surf, La Crique is a must-visit for those seeking an authentic Moroccan surf experience.', 33.8236, -7.15001),
	(7, 'Les Oudayas', '10030', 'Rabat Morocco', 'Les Oudayas in Rabat, Morocco, is a unique surf spot set against the backdrop of the historic Kasbah of the Udayas. The waves here are steady, making it a great spot for surfers of all levels. Beyond the surf, the location offers stunning views of the Atlantic Ocean and the city’s ancient fortifications. The blend of rich history and the thrill of surfing makes Les Oudayas a special destination for both surfers and travelers looking to experience Morocco\'s cultural and coastal charm.', 34.033414, -6.83993),
	(8, 'Banana', '80000', 'Taghazout Agadir Morocco', 'Banana Point in Taghazout, Agadir, Morocco, is a popular surf spot known for its long, peeling right-hand waves, making it ideal for surfers of all levels. The spot is named after the nearby banana plantations and offers a laid-back vibe with consistent surf, especially during the winter months. It\'s a great place for both beginners looking to improve and experienced surfers seeking fun, manageable waves in a picturesque setting.', 30.49962, -9.678873),
	(9, 'Killer Point', '80000', 'Taghazout Agadir Morocco', 'Killer Point in Taghazout, Agadir, Morocco, is a world-renowned surf spot famous for its powerful, long right-hand waves. The spot gets its name from the occasional sighting of killer whales offshore. Known for its fast and hollow waves, Killer Point is a favorite among advanced surfers looking for a thrilling ride. The break works best during mid to high tide, offering challenging but rewarding surf in a stunning coastal setting.', 30.551298, -9.961369);

-- Listage de la structure de table yala_surf. auth_group
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table yala_surf.auth_group : ~0 rows (environ)

-- Listage de la structure de table yala_surf. auth_group_permissions
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table yala_surf.auth_group_permissions : ~0 rows (environ)

-- Listage de la structure de table yala_surf. auth_permission
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table yala_surf.auth_permission : ~88 rows (environ)
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
	(1, 'Can add log entry', 1, 'add_logentry'),
	(2, 'Can change log entry', 1, 'change_logentry'),
	(3, 'Can delete log entry', 1, 'delete_logentry'),
	(4, 'Can view log entry', 1, 'view_logentry'),
	(5, 'Can add permission', 2, 'add_permission'),
	(6, 'Can change permission', 2, 'change_permission'),
	(7, 'Can delete permission', 2, 'delete_permission'),
	(8, 'Can view permission', 2, 'view_permission'),
	(9, 'Can add group', 3, 'add_group'),
	(10, 'Can change group', 3, 'change_group'),
	(11, 'Can delete group', 3, 'delete_group'),
	(12, 'Can view group', 3, 'view_group'),
	(13, 'Can add content type', 4, 'add_contenttype'),
	(14, 'Can change content type', 4, 'change_contenttype'),
	(15, 'Can delete content type', 4, 'delete_contenttype'),
	(16, 'Can view content type', 4, 'view_contenttype'),
	(17, 'Can add session', 5, 'add_session'),
	(18, 'Can change session', 5, 'change_session'),
	(19, 'Can delete session', 5, 'delete_session'),
	(20, 'Can view session', 5, 'view_session'),
	(21, 'Can add equipment', 6, 'add_equipment'),
	(22, 'Can change equipment', 6, 'change_equipment'),
	(23, 'Can delete equipment', 6, 'delete_equipment'),
	(24, 'Can view equipment', 6, 'view_equipment'),
	(25, 'Can add equipment type', 7, 'add_equipmenttype'),
	(26, 'Can change equipment type', 7, 'change_equipmenttype'),
	(27, 'Can delete equipment type', 7, 'delete_equipmenttype'),
	(28, 'Can view equipment type', 7, 'view_equipmenttype'),
	(29, 'Can add forum', 8, 'add_forum'),
	(30, 'Can change forum', 8, 'change_forum'),
	(31, 'Can delete forum', 8, 'delete_forum'),
	(32, 'Can view forum', 8, 'view_forum'),
	(33, 'Can add order', 9, 'add_order'),
	(34, 'Can change order', 9, 'change_order'),
	(35, 'Can delete order', 9, 'delete_order'),
	(36, 'Can view order', 9, 'view_order'),
	(37, 'Can add surf club', 10, 'add_surfclub'),
	(38, 'Can change surf club', 10, 'change_surfclub'),
	(39, 'Can delete surf club', 10, 'delete_surfclub'),
	(40, 'Can view surf club', 10, 'view_surfclub'),
	(41, 'Can add surfer', 11, 'add_surfer'),
	(42, 'Can change surfer', 11, 'change_surfer'),
	(43, 'Can delete surfer', 11, 'delete_surfer'),
	(44, 'Can view surfer', 11, 'view_surfer'),
	(45, 'Can add surf spot', 12, 'add_surfspot'),
	(46, 'Can change surf spot', 12, 'change_surfspot'),
	(47, 'Can delete surf spot', 12, 'delete_surfspot'),
	(48, 'Can view surf spot', 12, 'view_surfspot'),
	(49, 'Can add equipment selection', 13, 'add_equipmentselection'),
	(50, 'Can change equipment selection', 13, 'change_equipmentselection'),
	(51, 'Can delete equipment selection', 13, 'delete_equipmentselection'),
	(52, 'Can view equipment selection', 13, 'view_equipmentselection'),
	(53, 'Can add order item', 14, 'add_orderitem'),
	(54, 'Can change order item', 14, 'change_orderitem'),
	(55, 'Can delete order item', 14, 'delete_orderitem'),
	(56, 'Can view order item', 14, 'view_orderitem'),
	(57, 'Can add monitor', 15, 'add_monitor'),
	(58, 'Can change monitor', 15, 'change_monitor'),
	(59, 'Can delete monitor', 15, 'delete_monitor'),
	(60, 'Can view monitor', 15, 'view_monitor'),
	(61, 'Can add lesson schedule', 16, 'add_lessonschedule'),
	(62, 'Can change lesson schedule', 16, 'change_lessonschedule'),
	(63, 'Can delete lesson schedule', 16, 'delete_lessonschedule'),
	(64, 'Can view lesson schedule', 16, 'view_lessonschedule'),
	(65, 'Can add message', 17, 'add_message'),
	(66, 'Can change message', 17, 'change_message'),
	(67, 'Can delete message', 17, 'delete_message'),
	(68, 'Can view message', 17, 'view_message'),
	(69, 'Can add surf lesson', 18, 'add_surflesson'),
	(70, 'Can change surf lesson', 18, 'change_surflesson'),
	(71, 'Can delete surf lesson', 18, 'delete_surflesson'),
	(72, 'Can view surf lesson', 18, 'view_surflesson'),
	(73, 'Can add surf session', 19, 'add_surfsession'),
	(74, 'Can change surf session', 19, 'change_surfsession'),
	(75, 'Can delete surf session', 19, 'delete_surfsession'),
	(76, 'Can view surf session', 19, 'view_surfsession'),
	(77, 'Can add photo', 20, 'add_photo'),
	(78, 'Can change photo', 20, 'change_photo'),
	(79, 'Can delete photo', 20, 'delete_photo'),
	(80, 'Can view photo', 20, 'view_photo'),
	(81, 'Can add custom user', 21, 'add_customuser'),
	(82, 'Can change custom user', 21, 'change_customuser'),
	(83, 'Can delete custom user', 21, 'delete_customuser'),
	(84, 'Can view custom user', 21, 'view_customuser'),
	(85, 'Can add contact', 22, 'add_contact'),
	(86, 'Can change contact', 22, 'change_contact'),
	(87, 'Can delete contact', 22, 'delete_contact'),
	(88, 'Can view contact', 22, 'view_contact');

-- Listage de la structure de table yala_surf. django_admin_log
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_AppWeb_customuser_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_AppWeb_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `AppWeb_customuser` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table yala_surf.django_admin_log : ~66 rows (environ)
INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
	(1, '2024-08-30 11:47:42.068088', '1', 'SurfSpot object (1)', 1, '[{"added": {}}]', 12, 1),
	(2, '2024-08-30 11:48:04.841565', '1', 'Photo of Anza', 1, '[{"added": {}}]', 20, 1),
	(3, '2024-08-30 11:48:13.052844', '2', 'Photo of Anza', 1, '[{"added": {}}]', 20, 1),
	(4, '2024-08-30 11:56:52.706362', '1', 'EquipmentType object (1)', 1, '[{"added": {}}]', 7, 1),
	(5, '2024-08-30 11:56:56.835006', '2', 'EquipmentType object (2)', 1, '[{"added": {}}]', 7, 1),
	(6, '2024-08-30 11:57:00.870614', '3', 'EquipmentType object (3)', 1, '[{"added": {}}]', 7, 1),
	(7, '2024-08-30 12:15:47.154919', '1', 'Forum for Anza', 1, '[{"added": {}}]', 8, 1),
	(8, '2024-08-30 18:01:37.730282', '3', 'surfer@gmail.com', 2, '[{"changed": {"fields": ["Password"]}}]', 21, 1),
	(9, '2024-08-30 18:01:51.714710', '3', 'surfer@gmail.com', 2, '[]', 21, 1),
	(10, '2024-08-31 01:05:36.686864', '9', 'Photo of derive FS', 1, '[{"added": {}}]', 20, 1),
	(11, '2024-08-31 12:51:17.920483', '2', 'SurfSpot object (2)', 1, '[{"added": {}}]', 12, 1),
	(12, '2024-08-31 12:56:03.148047', '2', 'Photo of Anza', 3, '', 20, 1),
	(13, '2024-08-31 12:56:07.004434', '1', 'Photo of Anza', 3, '', 20, 1),
	(14, '2024-08-31 12:57:26.868433', '13', 'Photo of Anza', 1, '[{"added": {}}]', 20, 1),
	(15, '2024-08-31 13:19:20.895601', '14', 'Photo of Anza', 1, '[{"added": {}}]', 20, 1),
	(16, '2024-08-31 13:52:28.612653', '3', 'SurfSpot object (3)', 1, '[{"added": {}}]', 12, 1),
	(17, '2024-08-31 13:52:48.987625', '15', 'Photo of Taghazout', 1, '[{"added": {}}]', 20, 1),
	(18, '2024-08-31 15:01:34.072469', '11', 'Photo of derive FS', 2, '[{"changed": {"fields": ["Image"]}}]', 20, 1),
	(19, '2024-08-31 15:40:20.579873', '12', 'Photo of test', 3, '', 20, 1),
	(20, '2024-08-31 15:40:30.238994', '16', 'Photo of test', 1, '[{"added": {}}]', 20, 1),
	(21, '2024-08-31 15:58:42.923284', '5', 'Photo of combine', 2, '[{"changed": {"fields": ["Image"]}}]', 20, 1),
	(22, '2024-08-31 15:58:50.913399', '8', 'Photo of planche de surf', 2, '[{"changed": {"fields": ["Image"]}}]', 20, 1),
	(23, '2024-08-31 22:55:15.346283', '17', 'Photo of Bouznika', 1, '[{"added": {}}]', 20, 1),
	(24, '2024-09-02 23:59:06.080186', '18', 'Photo of test', 1, '[{"added": {}}]', 20, 1),
	(25, '2024-09-05 02:14:34.812654', '25', 'Photo of derive', 1, '[{"added": {}}]', 20, 1),
	(26, '2024-09-05 02:14:42.882657', '26', 'Photo of planche', 1, '[{"added": {}}]', 20, 1),
	(27, '2024-09-09 21:10:34.608069', '4', 'SurfSpot object (4)', 1, '[{"added": {}}]', 12, 1),
	(28, '2024-09-09 21:15:13.769017', '5', 'SurfSpot object (5)', 1, '[{"added": {}}]', 12, 1),
	(29, '2024-09-09 21:18:50.373903', '6', 'SurfSpot object (6)', 1, '[{"added": {}}]', 12, 1),
	(30, '2024-09-09 21:26:43.134875', '7', 'SurfSpot object (7)', 1, '[{"added": {}}]', 12, 1),
	(31, '2024-09-09 21:29:22.605361', '8', 'SurfSpot object (8)', 1, '[{"added": {}}]', 12, 1),
	(32, '2024-09-09 21:32:44.968506', '9', 'SurfSpot object (9)', 1, '[{"added": {}}]', 12, 1),
	(33, '2024-09-09 21:33:27.298441', '7', 'SurfSpot object (7)', 2, '[{"changed": {"fields": ["Address"]}}]', 12, 1),
	(34, '2024-09-09 21:33:30.134230', '7', 'SurfSpot object (7)', 2, '[]', 12, 1),
	(35, '2024-09-09 21:33:39.475673', '6', 'SurfSpot object (6)', 2, '[{"changed": {"fields": ["Address"]}}]', 12, 1),
	(36, '2024-09-09 21:34:01.442352', '5', 'SurfSpot object (5)', 2, '[{"changed": {"fields": ["Address"]}}]', 12, 1),
	(37, '2024-09-09 21:34:11.276130', '4', 'SurfSpot object (4)', 2, '[{"changed": {"fields": ["Address"]}}]', 12, 1),
	(38, '2024-09-09 22:52:13.983008', '8', 'SurfSpot object (8)', 2, '[{"changed": {"fields": ["Longitude"]}}]', 12, 1),
	(39, '2024-09-09 22:52:19.486673', '9', 'SurfSpot object (9)', 2, '[{"changed": {"fields": ["Longitude"]}}]', 12, 1),
	(40, '2024-09-09 22:52:28.763101', '4', 'SurfSpot object (4)', 2, '[{"changed": {"fields": ["Longitude"]}}]', 12, 1),
	(41, '2024-09-09 22:52:33.611520', '5', 'SurfSpot object (5)', 2, '[]', 12, 1),
	(42, '2024-09-09 23:25:42.104095', '27', 'Photo of Anchor Point', 1, '[{"added": {}}]', 20, 1),
	(43, '2024-09-09 23:25:51.149202', '28', 'Photo of Anchor Point', 1, '[{"added": {}}]', 20, 1),
	(44, '2024-09-09 23:25:59.667935', '29', 'Photo of Anchor Point', 1, '[{"added": {}}]', 20, 1),
	(45, '2024-09-09 23:26:09.947522', '30', 'Photo of La crique', 1, '[{"added": {}}]', 20, 1),
	(46, '2024-09-09 23:26:18.103753', '31', 'Photo of La crique', 1, '[{"added": {}}]', 20, 1),
	(47, '2024-09-09 23:26:25.946926', '32', 'Photo of La crique', 1, '[{"added": {}}]', 20, 1),
	(48, '2024-09-09 23:26:34.823125', '33', 'Photo of Banana', 1, '[{"added": {}}]', 20, 1),
	(49, '2024-09-09 23:26:43.102701', '34', 'Photo of Banana', 1, '[{"added": {}}]', 20, 1),
	(50, '2024-09-09 23:26:50.962817', '35', 'Photo of Banana', 1, '[{"added": {}}]', 20, 1),
	(51, '2024-09-09 23:27:04.120188', '36', 'Photo of Killer Point', 1, '[{"added": {}}]', 20, 1),
	(52, '2024-09-09 23:27:11.154595', '37', 'Photo of Killer Point', 1, '[{"added": {}}]', 20, 1),
	(53, '2024-09-09 23:27:20.959666', '38', 'Photo of Les Oudayas', 1, '[{"added": {}}]', 20, 1),
	(54, '2024-09-09 23:27:29.913170', '39', 'Photo of Les Oudayas', 1, '[{"added": {}}]', 20, 1),
	(55, '2024-09-09 23:28:52.742165', '40', 'Photo of Anza', 1, '[{"added": {}}]', 20, 1),
	(56, '2024-09-09 23:29:01.457800', '41', 'Photo of Anza', 1, '[{"added": {}}]', 20, 1),
	(57, '2024-09-09 23:31:40.723797', '40', 'Photo of Anza', 2, '[{"changed": {"fields": ["Image"]}}]', 20, 1),
	(58, '2024-09-09 23:33:29.290706', '38', 'Photo of Les Oudayas', 2, '[{"changed": {"fields": ["Image"]}}]', 20, 1),
	(59, '2024-09-10 10:48:40.996249', '9', 'Killer Point', 2, '[{"changed": {"fields": ["Longitude"]}}]', 12, 1),
	(60, '2024-09-10 10:49:07.821083', '9', 'Killer Point', 2, '[{"changed": {"fields": ["Longitude"]}}]', 12, 1),
	(61, '2024-09-10 10:49:34.642678', '8', 'Banana', 2, '[{"changed": {"fields": ["Longitude"]}}]', 12, 1),
	(62, '2024-09-10 10:50:36.486766', '8', 'Banana', 2, '[{"changed": {"fields": ["Longitude"]}}]', 12, 1),
	(63, '2024-09-10 10:51:13.622459', '7', 'Les Oudayas', 2, '[]', 12, 1),
	(64, '2024-09-10 10:52:00.470031', '7', 'Les Oudayas', 2, '[{"changed": {"fields": ["Latitude", "Longitude"]}}]', 12, 1),
	(65, '2024-09-10 10:52:57.332392', '6', 'La crique', 2, '[{"changed": {"fields": ["Longitude"]}}]', 12, 1),
	(66, '2024-09-10 10:53:12.442906', '6', 'La crique', 2, '[{"changed": {"fields": ["Latitude"]}}]', 12, 1);

-- Listage de la structure de table yala_surf. django_content_type
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table yala_surf.django_content_type : ~22 rows (environ)
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
	(1, 'admin', 'logentry'),
	(22, 'AppWeb', 'contact'),
	(21, 'AppWeb', 'customuser'),
	(6, 'AppWeb', 'equipment'),
	(13, 'AppWeb', 'equipmentselection'),
	(7, 'AppWeb', 'equipmenttype'),
	(8, 'AppWeb', 'forum'),
	(16, 'AppWeb', 'lessonschedule'),
	(17, 'AppWeb', 'message'),
	(15, 'AppWeb', 'monitor'),
	(9, 'AppWeb', 'order'),
	(14, 'AppWeb', 'orderitem'),
	(20, 'AppWeb', 'photo'),
	(10, 'AppWeb', 'surfclub'),
	(11, 'AppWeb', 'surfer'),
	(18, 'AppWeb', 'surflesson'),
	(19, 'AppWeb', 'surfsession'),
	(12, 'AppWeb', 'surfspot'),
	(3, 'auth', 'group'),
	(2, 'auth', 'permission'),
	(4, 'contenttypes', 'contenttype'),
	(5, 'sessions', 'session');

-- Listage de la structure de table yala_surf. django_migrations
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table yala_surf.django_migrations : ~23 rows (environ)
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
	(1, 'contenttypes', '0001_initial', '2024-08-30 11:30:37.391783'),
	(2, 'contenttypes', '0002_remove_content_type_name', '2024-08-30 11:30:37.454518'),
	(3, 'auth', '0001_initial', '2024-08-30 11:30:37.674138'),
	(4, 'auth', '0002_alter_permission_name_max_length', '2024-08-30 11:30:37.737145'),
	(5, 'auth', '0003_alter_user_email_max_length', '2024-08-30 11:30:37.737145'),
	(6, 'auth', '0004_alter_user_username_opts', '2024-08-30 11:30:37.737145'),
	(7, 'auth', '0005_alter_user_last_login_null', '2024-08-30 11:30:37.752783'),
	(8, 'auth', '0006_require_contenttypes_0002', '2024-08-30 11:30:37.752783'),
	(9, 'auth', '0007_alter_validators_add_error_messages', '2024-08-30 11:30:37.752783'),
	(10, 'auth', '0008_alter_user_username_max_length', '2024-08-30 11:30:37.752783'),
	(11, 'auth', '0009_alter_user_last_name_max_length', '2024-08-30 11:30:37.769238'),
	(12, 'auth', '0010_alter_group_name_max_length', '2024-08-30 11:30:37.784283'),
	(13, 'auth', '0011_update_proxy_permissions', '2024-08-30 11:30:37.784283'),
	(14, 'auth', '0012_alter_user_first_name_max_length', '2024-08-30 11:30:37.799948'),
	(15, 'AppWeb', '0001_initial', '2024-08-30 11:30:39.771439'),
	(16, 'admin', '0001_initial', '2024-08-30 11:30:39.919231'),
	(17, 'admin', '0002_logentry_remove_auto_add', '2024-08-30 11:30:39.930241'),
	(18, 'admin', '0003_logentry_add_action_flag_choices', '2024-08-30 11:30:39.947180'),
	(19, 'sessions', '0001_initial', '2024-08-30 11:30:39.993759'),
	(20, 'AppWeb', '0002_equipment_quantity', '2024-09-03 02:07:55.912553'),
	(21, 'AppWeb', '0003_remove_equipment_is_rent_remove_equipment_is_sell', '2024-09-03 02:16:49.122989'),
	(22, 'AppWeb', '0004_surflesson_total_price', '2024-09-03 02:52:34.746170'),
	(23, 'AppWeb', '0005_contact', '2024-09-04 12:47:23.750364');

-- Listage de la structure de table yala_surf. django_session
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table yala_surf.django_session : ~4 rows (environ)
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
	('sx9vuidwhtj58nnvkeehxt6ft2te6pd0', '.eJxVjEsOwjAMBe-SNYr6sR3Mkn3PEDm1QwqolfpZIe4OlbqA7ZuZ93JRtrXEbbE5Duournan3y1J_7BxB3qX8Tb5fhrXeUh-V_xBF99Nas_r4f4dFFnKt0YiocAhcdWqgeZaqwRNw2cDaSkgcq9MwrWFijIDtQiIhJm1AQP3_gDFvDbd:1sm20R:FMkMmFlEF8Mad2XMxZou51dd3k7fmyuw7kdJ1r2YaZA', '2024-09-19 02:13:55.509306'),
	('tx9yntbbkzgwm5z8b3k0kv0741p8fq1t', '.eJxVjEsOwjAMBe-SNYr6sR3Mkn3PEDm1QwqolfpZIe4OlbqA7ZuZ93JRtrXEbbE5Duournan3y1J_7BxB3qX8Tb5fhrXeUh-V_xBF99Nas_r4f4dFFnKt0YiocAhcdWqgeZaqwRNw2cDaSkgcq9MwrWFijIDtQiIhJm1AQP3_gDFvDbd:1skwrX:kq7-jWdQ3g_VYfz1gSBlCjfbPrtsw72Z1FrCq-k91wU', '2024-09-16 02:32:15.286250'),
	('wj8bc862r2a11fjpbi326zux7x3m6i91', '.eJxVjEsOwjAMBe-SNYr6sR3Mkn3PEDm1QwqolfpZIe4OlbqA7ZuZ93JRtrXEbbE5Duournan3y1J_7BxB3qX8Tb5fhrXeUh-V_xBF99Nas_r4f4dFFnKt0YiocAhcdWqgeZaqwRNw2cDaSkgcq9MwrWFijIDtQiIhJm1AQP3_gDFvDbd:1snnE5:onVt7PrUYuN1tEWKoWEo2tZ2Rm5jmRSdJ6UmZQ593W4', '2024-09-23 22:51:17.250866'),
	('zmygkx14scg3h2xnp3nni51197pzm1o1', '.eJxVjEsOwjAMBe-SNYr6sR3Mkn3PEDm1QwqolfpZIe4OlbqA7ZuZ93JRtrXEbbE5Duournan3y1J_7BxB3qX8Tb5fhrXeUh-V_xBF99Nas_r4f4dFFnKt0YiocAhcdWqgeZaqwRNw2cDaSkgcq9MwrWFijIDtQiIhJm1AQP3_gDFvDbd:1sknZn:vQjtikvChY5hbtAtdQ1yiMWOtuHuX7RDe56t9z21Xak', '2024-09-15 16:37:19.358038');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
