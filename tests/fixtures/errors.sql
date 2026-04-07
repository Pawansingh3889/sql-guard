-- Test fixture: all error rules should trigger

-- E001: DELETE without WHERE
DELETE FROM orders;

-- E002: DROP without IF EXISTS
DROP TABLE users;

-- E003: GRANT in application code
GRANT SELECT ON users TO public;

-- E004: String concatenation in WHERE
SELECT * FROM users WHERE name = '' + @input + '';

-- E005: INSERT without column list
INSERT INTO orders VALUES (1, 'test', 100);
