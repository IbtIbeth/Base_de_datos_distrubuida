CREATE USER 'replication_user'@'%' IDENTIFIED BY 'bigs3cret';
GRANT REPLICATION SLAVE ON *.* TO 'replication_user'@'%';

-- LOCK TABLES
FLUSH TABLES WITH READ LOCK;

-- Show the status and record the file and the position
-- You should make an import of the database after consulting this and copy
-- to the slave database
SHOW MASTER STATUS;

-- Unlock the database
UNLOCK TABLES;

