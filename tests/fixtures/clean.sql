-- Test fixture: no issues should be found

SELECT id, name, email
FROM users
WHERE active = true
LIMIT 100;

DELETE FROM sessions
WHERE expired_at < NOW();

INSERT INTO audit_log (user_id, action, created_at)
VALUES (1, 'login', NOW());

DROP TABLE IF EXISTS temp_data;
