USE `ytb_music`;

-- Migration goals:
-- 1) Rename songs.video_id -> songs.song_id
-- 2) Rename playlist_songs.video_id -> playlist_songs.song_id
-- 3) Create/align ytb_metadata table with song_id and FK to songs(song_id)

SET @db := DATABASE();

-- Drop dependent FKs when they exist (safe to re-add later).
SELECT COUNT(*) INTO @has_fk_playlist_song
FROM information_schema.TABLE_CONSTRAINTS
WHERE CONSTRAINT_SCHEMA = @db
  AND TABLE_NAME = 'playlist_songs'
  AND CONSTRAINT_NAME = 'fk_playlist_songs_song'
  AND CONSTRAINT_TYPE = 'FOREIGN KEY';

SET @sql := IF(
  @has_fk_playlist_song > 0,
  'ALTER TABLE `playlist_songs` DROP FOREIGN KEY `fk_playlist_songs_song`',
  'SELECT 1'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SELECT COUNT(*) INTO @has_fk_ytb_song
FROM information_schema.TABLE_CONSTRAINTS
WHERE CONSTRAINT_SCHEMA = @db
  AND TABLE_NAME = 'ytb_metadata'
  AND CONSTRAINT_NAME = 'fk_ytb_metadata_song'
  AND CONSTRAINT_TYPE = 'FOREIGN KEY';

SET @sql := IF(
  @has_fk_ytb_song > 0,
  'ALTER TABLE `ytb_metadata` DROP FOREIGN KEY `fk_ytb_metadata_song`',
  'SELECT 1'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Ensure ytb_metadata exists (new structure).
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
  PRIMARY KEY (`song_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ytb_metadata: remove downloaded column if it exists.
SELECT COUNT(*) INTO @ytb_metadata_has_downloaded
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = @db
  AND TABLE_NAME = 'ytb_metadata'
  AND COLUMN_NAME = 'downloaded';

SET @sql := IF(
  @ytb_metadata_has_downloaded > 0,
  'ALTER TABLE `ytb_metadata` DROP COLUMN `downloaded`',
  'SELECT 1'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- ytb_metadata: remove visualizer_data column if it exists.
SELECT COUNT(*) INTO @ytb_metadata_has_visualizer_data
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = @db
  AND TABLE_NAME = 'ytb_metadata'
  AND COLUMN_NAME = 'visualizer_data';

SET @sql := IF(
  @ytb_metadata_has_visualizer_data > 0,
  'ALTER TABLE `ytb_metadata` DROP COLUMN `visualizer_data`',
  'SELECT 1'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- songs: rename video_id -> song_id when needed.
SELECT COUNT(*) INTO @songs_has_video_id
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = @db
  AND TABLE_NAME = 'songs'
  AND COLUMN_NAME = 'video_id';

SELECT COUNT(*) INTO @songs_has_song_id
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = @db
  AND TABLE_NAME = 'songs'
  AND COLUMN_NAME = 'song_id';

SET @sql := IF(
  @songs_has_video_id > 0 AND @songs_has_song_id = 0,
  'ALTER TABLE `songs` CHANGE COLUMN `video_id` `song_id` VARCHAR(32) NOT NULL',
  'SELECT 1'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- playlist_songs: rename video_id -> song_id when needed.
SELECT COUNT(*) INTO @playlist_songs_has_video_id
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = @db
  AND TABLE_NAME = 'playlist_songs'
  AND COLUMN_NAME = 'video_id';

SELECT COUNT(*) INTO @playlist_songs_has_song_id
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = @db
  AND TABLE_NAME = 'playlist_songs'
  AND COLUMN_NAME = 'song_id';

SET @sql := IF(
  @playlist_songs_has_video_id > 0 AND @playlist_songs_has_song_id = 0,
  'ALTER TABLE `playlist_songs` CHANGE COLUMN `video_id` `song_id` VARCHAR(32) NOT NULL',
  'SELECT 1'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- ytb_metadata: rename video_id -> song_id when needed.
SELECT COUNT(*) INTO @ytb_metadata_has_video_id
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = @db
  AND TABLE_NAME = 'ytb_metadata'
  AND COLUMN_NAME = 'video_id';

SELECT COUNT(*) INTO @ytb_metadata_has_song_id
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = @db
  AND TABLE_NAME = 'ytb_metadata'
  AND COLUMN_NAME = 'song_id';

SET @sql := IF(
  @ytb_metadata_has_video_id > 0 AND @ytb_metadata_has_song_id = 0,
  'ALTER TABLE `ytb_metadata` CHANGE COLUMN `video_id` `song_id` VARCHAR(32) NOT NULL',
  'SELECT 1'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Recreate expected FKs if missing.
SELECT COUNT(*) INTO @has_fk_playlist_song
FROM information_schema.TABLE_CONSTRAINTS
WHERE CONSTRAINT_SCHEMA = @db
  AND TABLE_NAME = 'playlist_songs'
  AND CONSTRAINT_NAME = 'fk_playlist_songs_song'
  AND CONSTRAINT_TYPE = 'FOREIGN KEY';

SET @sql := IF(
  @has_fk_playlist_song = 0,
  'ALTER TABLE `playlist_songs` ADD CONSTRAINT `fk_playlist_songs_song` FOREIGN KEY (`song_id`) REFERENCES `songs` (`song_id`) ON DELETE CASCADE',
  'SELECT 1'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SELECT COUNT(*) INTO @has_fk_ytb_song
FROM information_schema.TABLE_CONSTRAINTS
WHERE CONSTRAINT_SCHEMA = @db
  AND TABLE_NAME = 'ytb_metadata'
  AND CONSTRAINT_NAME = 'fk_ytb_metadata_song'
  AND CONSTRAINT_TYPE = 'FOREIGN KEY';

SET @sql := IF(
  @has_fk_ytb_song = 0,
  'ALTER TABLE `ytb_metadata` ADD CONSTRAINT `fk_ytb_metadata_song` FOREIGN KEY (`song_id`) REFERENCES `songs` (`song_id`) ON DELETE CASCADE',
  'SELECT 1'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
