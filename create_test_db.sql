-- Create test database + user if doesn't exist
CREATE DATABASE IF NOT EXISTS ticket_test_db;
CREATE USER IF NOT EXISTS 'ticket_test'@'localhost';
SET PASSWORD FOR 'ticket_test'@'localhost' = 'ticket_test_pwd';
GRANT ALL ON ticket_test_db.* TO 'ticket_test'@'localhost';
GRANT SELECT ON performance_schema.* TO 'ticket_test'@'localhost';
FLUSH PRIVILEGES;
