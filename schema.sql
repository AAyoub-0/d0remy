CREATE DATABASE IF NOT EXISTS `ytb_music` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `ytb_music`;

CREATE TABLE IF NOT EXISTS `songs` (
  `video_id` VARCHAR(32) NOT NULL,
  `title` TEXT,
  `artist` TEXT,
  `uploader` TEXT,
  `duration` INT,
  `upload_date` VARCHAR(16),
  `description` TEXT,
  `url` TEXT,
  `thumbnail` TEXT,
  `size_bytes` BIGINT,
  `size_mb` DECIMAL(12,2),
  `downloaded` TINYINT(1) NOT NULL DEFAULT 0,
  `metadata_created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`video_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `playlists` (
  `playlist_id` VARCHAR(64) NOT NULL,
  `title` TEXT,
  `uploader` TEXT,
  `uploader_id` TEXT,
  `webpage_url` TEXT,
  `description` TEXT,
  `entry_count` INT,
  `total_size_mb` DECIMAL(12,2),
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`playlist_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `playlist_songs` (
  `playlist_id` VARCHAR(64) NOT NULL,
  `video_id` VARCHAR(32) NOT NULL,
  `position` INT NOT NULL,
  PRIMARY KEY (`playlist_id`, `video_id`),
  KEY `idx_playlist_position` (`playlist_id`, `position`),
  CONSTRAINT `fk_playlist_songs_playlist` FOREIGN KEY (`playlist_id`) REFERENCES `playlists` (`playlist_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_playlist_songs_song` FOREIGN KEY (`video_id`) REFERENCES `songs` (`video_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
