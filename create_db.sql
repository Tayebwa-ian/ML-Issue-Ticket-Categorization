-- Create database + user if doesn't exist
CREATE DATABASE IF NOT EXISTS ticket_dev_db;
CREATE USER IF NOT EXISTS 'ticket_dev'@'localhost';
SET PASSWORD FOR 'ticket_dev'@'localhost' = 'ticket_dev_pwd';
GRANT ALL ON ticket_dev_db.* TO 'ticket_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'ticket_dev'@'localhost';
FLUSH PRIVILEGES;
