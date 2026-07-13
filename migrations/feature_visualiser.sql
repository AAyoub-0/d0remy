-- Migration SQL - feature_visualiser
-- Date: 2026-07-13
-- Objectif: ajouter les données de visualisation au stockage des chansons

-- Ajouter la colonne JSON pour stocker l'objet de visualiseur sur chaque chanson
ALTER TABLE `songs`
ADD COLUMN `visualizer_data` JSON DEFAULT NULL;

-- Exemple de mise à jour future si vous voulez préremplir un objet vide
-- UPDATE `songs`
-- SET `visualizer_data` = JSON_OBJECT(
--   'bars', JSON_ARRAY(),
--   'bar_count', 32,
--   'energy', NULL,
--   'peak', NULL,
--   'rms', NULL,
--   'frequencies', JSON_ARRAY()
-- )
-- WHERE `visualizer_data` IS NULL;
