USE `ytb_music`;

-- Migration goals:
-- 1) Extend songs with external metadata/provider/editorial/rating fields
-- 2) Create artists, albums, album_artists, classifications tables
-- 3) Align albums with rating field

SET @db := DATABASE();

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
  KEY `idx_albums_artist_id` (`artist_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `album_artists` (
  `album_id` BIGINT UNSIGNED NOT NULL,
  `artist_id` BIGINT UNSIGNED NOT NULL,
  `role` VARCHAR(64) NOT NULL,
  `credit_order` INT NOT NULL DEFAULT 1,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`album_id`, `artist_id`, `role`),
  KEY `idx_album_artists_artist_id` (`artist_id`),
  KEY `idx_album_artists_role` (`role`)
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

-- songs columns added incrementally when missing.
SELECT COUNT(*) INTO @songs_has_isrc
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = @db AND TABLE_NAME = 'songs' AND COLUMN_NAME = 'isrc';
SET @sql := IF(@songs_has_isrc = 0, 'ALTER TABLE `songs` ADD COLUMN `isrc` VARCHAR(32) DEFAULT NULL AFTER `thumbnail`', 'SELECT 1');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SELECT COUNT(*) INTO @songs_has_upc
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = @db AND TABLE_NAME = 'songs' AND COLUMN_NAME = 'upc';
SET @sql := IF(@songs_has_upc = 0, 'ALTER TABLE `songs` ADD COLUMN `upc` VARCHAR(32) DEFAULT NULL AFTER `isrc`', 'SELECT 1');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SELECT COUNT(*) INTO @songs_has_mb_recording
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = @db AND TABLE_NAME = 'songs' AND COLUMN_NAME = 'musicbrainz_recording_id';
SET @sql := IF(@songs_has_mb_recording = 0, 'ALTER TABLE `songs` ADD COLUMN `musicbrainz_recording_id` VARCHAR(64) DEFAULT NULL AFTER `upc`', 'SELECT 1');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SELECT COUNT(*) INTO @songs_has_mb_release
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = @db AND TABLE_NAME = 'songs' AND COLUMN_NAME = 'musicbrainz_release_id';
SET @sql := IF(@songs_has_mb_release = 0, 'ALTER TABLE `songs` ADD COLUMN `musicbrainz_release_id` VARCHAR(64) DEFAULT NULL AFTER `musicbrainz_recording_id`', 'SELECT 1');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SELECT COUNT(*) INTO @songs_has_mb_artists
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = @db AND TABLE_NAME = 'songs' AND COLUMN_NAME = 'musicbrainz_artist_ids';
SET @sql := IF(@songs_has_mb_artists = 0, 'ALTER TABLE `songs` ADD COLUMN `musicbrainz_artist_ids` JSON DEFAULT NULL AFTER `musicbrainz_release_id`', 'SELECT 1');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SELECT COUNT(*) INTO @songs_has_spotify_id
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = @db AND TABLE_NAME = 'songs' AND COLUMN_NAME = 'spotify_id';
SET @sql := IF(@songs_has_spotify_id = 0, 'ALTER TABLE `songs` ADD COLUMN `spotify_id` VARCHAR(128) DEFAULT NULL AFTER `musicbrainz_artist_ids`', 'SELECT 1');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SELECT COUNT(*) INTO @songs_has_deezer_id
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = @db AND TABLE_NAME = 'songs' AND COLUMN_NAME = 'deezer_id';
SET @sql := IF(@songs_has_deezer_id = 0, 'ALTER TABLE `songs` ADD COLUMN `deezer_id` VARCHAR(128) DEFAULT NULL AFTER `spotify_id`', 'SELECT 1');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SELECT COUNT(*) INTO @songs_has_apple_music_id
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = @db AND TABLE_NAME = 'songs' AND COLUMN_NAME = 'apple_music_id';
SET @sql := IF(@songs_has_apple_music_id = 0, 'ALTER TABLE `songs` ADD COLUMN `apple_music_id` VARCHAR(128) DEFAULT NULL AFTER `deezer_id`', 'SELECT 1');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SELECT COUNT(*) INTO @songs_has_youtube_video_id
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = @db AND TABLE_NAME = 'songs' AND COLUMN_NAME = 'youtube_video_id';
SET @sql := IF(@songs_has_youtube_video_id = 0, 'ALTER TABLE `songs` ADD COLUMN `youtube_video_id` VARCHAR(32) DEFAULT NULL AFTER `apple_music_id`', 'SELECT 1');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SELECT COUNT(*) INTO @songs_has_spotify
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = @db AND TABLE_NAME = 'songs' AND COLUMN_NAME = 'spotify';
SET @sql := IF(@songs_has_spotify = 0, 'ALTER TABLE `songs` ADD COLUMN `spotify` TEXT AFTER `youtube_video_id`', 'SELECT 1');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SELECT COUNT(*) INTO @songs_has_deezer
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = @db AND TABLE_NAME = 'songs' AND COLUMN_NAME = 'deezer';
SET @sql := IF(@songs_has_deezer = 0, 'ALTER TABLE `songs` ADD COLUMN `deezer` TEXT AFTER `spotify`', 'SELECT 1');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SELECT COUNT(*) INTO @songs_has_apple_music
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = @db AND TABLE_NAME = 'songs' AND COLUMN_NAME = 'apple_music';
SET @sql := IF(@songs_has_apple_music = 0, 'ALTER TABLE `songs` ADD COLUMN `apple_music` TEXT AFTER `deezer`', 'SELECT 1');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SELECT COUNT(*) INTO @songs_has_youtube
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = @db AND TABLE_NAME = 'songs' AND COLUMN_NAME = 'youtube';
SET @sql := IF(@songs_has_youtube = 0, 'ALTER TABLE `songs` ADD COLUMN `youtube` TEXT AFTER `apple_music`', 'SELECT 1');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SELECT COUNT(*) INTO @songs_has_musicbrainz
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = @db AND TABLE_NAME = 'songs' AND COLUMN_NAME = 'musicbrainz';
SET @sql := IF(@songs_has_musicbrainz = 0, 'ALTER TABLE `songs` ADD COLUMN `musicbrainz` TEXT AFTER `youtube`', 'SELECT 1');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SELECT COUNT(*) INTO @songs_has_lastfm
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = @db AND TABLE_NAME = 'songs' AND COLUMN_NAME = 'lastfm';
SET @sql := IF(@songs_has_lastfm = 0, 'ALTER TABLE `songs` ADD COLUMN `lastfm` TEXT AFTER `musicbrainz`', 'SELECT 1');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SELECT COUNT(*) INTO @songs_has_genius
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = @db AND TABLE_NAME = 'songs' AND COLUMN_NAME = 'genius';
SET @sql := IF(@songs_has_genius = 0, 'ALTER TABLE `songs` ADD COLUMN `genius` TEXT AFTER `lastfm`', 'SELECT 1');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SELECT COUNT(*) INTO @songs_has_copyright
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = @db AND TABLE_NAME = 'songs' AND COLUMN_NAME = 'copyright';
SET @sql := IF(@songs_has_copyright = 0, 'ALTER TABLE `songs` ADD COLUMN `copyright` TEXT AFTER `genius`', 'SELECT 1');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SELECT COUNT(*) INTO @songs_has_phonographic
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = @db AND TABLE_NAME = 'songs' AND COLUMN_NAME = 'phonographic';
SET @sql := IF(@songs_has_phonographic = 0, 'ALTER TABLE `songs` ADD COLUMN `phonographic` TEXT AFTER `copyright`', 'SELECT 1');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SELECT COUNT(*) INTO @songs_has_publisher
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = @db AND TABLE_NAME = 'songs' AND COLUMN_NAME = 'publisher';
SET @sql := IF(@songs_has_publisher = 0, 'ALTER TABLE `songs` ADD COLUMN `publisher` TEXT AFTER `phonographic`', 'SELECT 1');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SELECT COUNT(*) INTO @songs_has_rating
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = @db AND TABLE_NAME = 'songs' AND COLUMN_NAME = 'rating';
SET @sql := IF(@songs_has_rating = 0, 'ALTER TABLE `songs` ADD COLUMN `rating` DECIMAL(3,2) DEFAULT NULL AFTER `publisher`', 'SELECT 1');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- albums.rating may need to be added on an already-created albums table.
SELECT COUNT(*) INTO @albums_has_rating
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = @db AND TABLE_NAME = 'albums' AND COLUMN_NAME = 'rating';
SET @sql := IF(@albums_has_rating = 0, 'ALTER TABLE `albums` ADD COLUMN `rating` DECIMAL(3,2) DEFAULT NULL AFTER `description`', 'SELECT 1');
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- Recreate foreign keys if missing.
SELECT COUNT(*) INTO @has_fk_albums_artist
FROM information_schema.TABLE_CONSTRAINTS
WHERE CONSTRAINT_SCHEMA = @db
  AND TABLE_NAME = 'albums'
  AND CONSTRAINT_NAME = 'fk_albums_artist'
  AND CONSTRAINT_TYPE = 'FOREIGN KEY';
SET @sql := IF(
  @has_fk_albums_artist = 0,
  'ALTER TABLE `albums` ADD CONSTRAINT `fk_albums_artist` FOREIGN KEY (`artist_id`) REFERENCES `artists` (`artist_id`) ON DELETE SET NULL',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SELECT COUNT(*) INTO @has_fk_album_artists_album
FROM information_schema.TABLE_CONSTRAINTS
WHERE CONSTRAINT_SCHEMA = @db
  AND TABLE_NAME = 'album_artists'
  AND CONSTRAINT_NAME = 'fk_album_artists_album'
  AND CONSTRAINT_TYPE = 'FOREIGN KEY';
SET @sql := IF(
  @has_fk_album_artists_album = 0,
  'ALTER TABLE `album_artists` ADD CONSTRAINT `fk_album_artists_album` FOREIGN KEY (`album_id`) REFERENCES `albums` (`album_id`) ON DELETE CASCADE',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

SELECT COUNT(*) INTO @has_fk_album_artists_artist
FROM information_schema.TABLE_CONSTRAINTS
WHERE CONSTRAINT_SCHEMA = @db
  AND TABLE_NAME = 'album_artists'
  AND CONSTRAINT_NAME = 'fk_album_artists_artist'
  AND CONSTRAINT_TYPE = 'FOREIGN KEY';
SET @sql := IF(
  @has_fk_album_artists_artist = 0,
  'ALTER TABLE `album_artists` ADD CONSTRAINT `fk_album_artists_artist` FOREIGN KEY (`artist_id`) REFERENCES `artists` (`artist_id`) ON DELETE CASCADE',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;
