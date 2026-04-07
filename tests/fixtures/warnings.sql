-- Test fixture: warning rules should trigger

-- W001: SELECT *
SELECT * FROM users;

-- W003: Function on column in WHERE
SELECT id FROM orders WHERE YEAR(created_at) = 2024;

-- W007: Hardcoded values
SELECT id FROM orders WHERE amount > 10000;

-- W010: Commented-out code
-- SELECT * FROM deleted_users;
