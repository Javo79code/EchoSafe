USE scam_voice_db;
DESCRIBE scammers;

ALTER TABLE scammers
DROP COLUMN audio_file_path;

ALTER TABLE scammers
ADD COLUMN audio_file_path VARCHAR(500);

ALTER TABLE scammers
