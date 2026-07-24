CREATE DATABASE IF NOT EXISTS `ytb_music` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `ytb_music`;

CREATE TABLE IF NOT EXISTS `songs` (
  `song_id` VARCHAR(32) NOT NULL,
  `title` TEXT,
  `artist` TEXT,
  `uploader` TEXT,
  `duration` INT,
  `upload_date` VARCHAR(16),
  `description` TEXT,
  `url` TEXT,
  `thumbnail` TEXT,
  `isrc` VARCHAR(32) DEFAULT NULL,
  `upc` VARCHAR(32) DEFAULT NULL,
  `musicbrainz_recording_id` VARCHAR(64) DEFAULT NULL,
  `musicbrainz_release_id` VARCHAR(64) DEFAULT NULL,
  `musicbrainz_artist_ids` JSON DEFAULT NULL,
  `spotify_id` VARCHAR(128) DEFAULT NULL,
  `deezer_id` VARCHAR(128) DEFAULT NULL,
  `apple_music_id` VARCHAR(128) DEFAULT NULL,
  `youtube_video_id` VARCHAR(32) DEFAULT NULL,
  `spotify` TEXT,
  `deezer` TEXT,
  `apple_music` TEXT,
  `youtube` TEXT,
  `musicbrainz` TEXT,
  `lastfm` TEXT,
  `genius` TEXT,
  `copyright` TEXT,
  `phonographic` TEXT,
  `publisher` TEXT,
  `rating` DECIMAL(3,2) DEFAULT NULL,
  `size_bytes` BIGINT,
  `size_mb` DECIMAL(12,2),
  `downloaded` TINYINT(1) NOT NULL DEFAULT 0,
  `visualizer_data` JSON DEFAULT NULL,
  `metadata_created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`song_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `artists` (
  `artist_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `stage_name` VARCHAR(255) DEFAULT NULL,
  `slug` VARCHAR(255) DEFAULT NULL,
  `channel_id` VARCHAR(128) DEFAULT NULL,
  `spotify_id` VARCHAR(128) DEFAULT NULL,
  `apple_music_id` VARCHAR(128) DEFAULT NULL,
  `soundcloud_id` VARCHAR(128) DEFAULT NULL,
  `youtube_url` TEXT,
  `website_url` TEXT,
  `avatar_url` TEXT,
  `banner_url` TEXT,
  `bio` TEXT,
  `country_code` CHAR(2) DEFAULT NULL,
  `genres` JSON DEFAULT NULL,
  `followers_count` BIGINT UNSIGNED DEFAULT NULL,
  `monthly_listeners` BIGINT UNSIGNED DEFAULT NULL,
  `is_verified` TINYINT(1) NOT NULL DEFAULT 0,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`artist_id`),
  UNIQUE KEY `uq_artists_slug` (`slug`),
  UNIQUE KEY `uq_artists_channel_id` (`channel_id`),
  KEY `idx_artists_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `albums` (
  `album_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `artist_id` BIGINT UNSIGNED DEFAULT NULL,
  `title` VARCHAR(255) NOT NULL,
  `slug` VARCHAR(255) DEFAULT NULL,
  `album_type` VARCHAR(32) DEFAULT NULL,
  `release_date` DATE DEFAULT NULL,
  `cover_url` TEXT,
  `description` TEXT,
  `rating` DECIMAL(3,2) DEFAULT NULL,
  `track_count` INT DEFAULT NULL,
  `total_duration` INT DEFAULT NULL,
  `total_size_mb` DECIMAL(12,2) DEFAULT NULL,
  `is_explicit` TINYINT(1) NOT NULL DEFAULT 0,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`album_id`),
  UNIQUE KEY `uq_albums_slug` (`slug`),
  KEY `idx_albums_title` (`title`),
  KEY `idx_albums_artist_id` (`artist_id`),
  CONSTRAINT `fk_albums_artist`
    FOREIGN KEY (`artist_id`) REFERENCES `artists` (`artist_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `album_artists` (
  `album_id` BIGINT UNSIGNED NOT NULL,
  `artist_id` BIGINT UNSIGNED NOT NULL,
  `role` VARCHAR(64) NOT NULL,
  `credit_order` INT NOT NULL DEFAULT 1,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`album_id`, `artist_id`, `role`),
  KEY `idx_album_artists_artist_id` (`artist_id`),
  KEY `idx_album_artists_role` (`role`),
  CONSTRAINT `fk_album_artists_album`
    FOREIGN KEY (`album_id`) REFERENCES `albums` (`album_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_album_artists_artist`
    FOREIGN KEY (`artist_id`) REFERENCES `artists` (`artist_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `classifications` (
  `classification_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `genre` VARCHAR(128) DEFAULT NULL,
  `subgenres` JSON DEFAULT NULL,
  `moods` JSON DEFAULT NULL,
  `language` VARCHAR(64) DEFAULT NULL,
  `is_explicit` TINYINT(1) NOT NULL DEFAULT 0,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`classification_id`),
  KEY `idx_classifications_genre` (`genre`),
  KEY `idx_classifications_language` (`language`),
  KEY `idx_classifications_is_explicit` (`is_explicit`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `ytb_metadata` (
  `song_id` VARCHAR(32) NOT NULL,
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
  `metadata_created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`song_id`),
  CONSTRAINT `fk_ytb_metadata_song`
    FOREIGN KEY (`song_id`) REFERENCES `songs` (`song_id`) ON DELETE CASCADE
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
  `song_id` VARCHAR(32) NOT NULL,
  `position` INT NOT NULL,
  PRIMARY KEY (`playlist_id`, `song_id`),
  KEY `idx_playlist_position` (`playlist_id`, `position`),
  CONSTRAINT `fk_playlist_songs_playlist` FOREIGN KEY (`playlist_id`) REFERENCES `playlists` (`playlist_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_playlist_songs_song` FOREIGN KEY (`song_id`) REFERENCES `songs` (`song_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
