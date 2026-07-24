USE `ytb_music`;

SET @db := DATABASE();

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