-- Change the master 
-- In MASTER_LOG_FILE and MASTER_LOG_POS write the info obtained from the previous tables
-- in case that the table is new just run without them.
CHANGE MASTER TO
  MASTER_HOST='0.0.0.0',
  MASTER_USER='replication_user',
  MASTER_PASSWORD='bigs3cret',
  MASTER_PORT=3310,
  MASTER_LOG_FILE='master1-bin.000003',
  MASTER_LOG_POS=678,
  MASTER_CONNECT_RETRY=10;
  
 -- It is generally recommended to use (GTIDs)
CHANGE MASTER TO MASTER_USE_GTID = slave_pos

START SLAVE;
SHOW SLAVE STATUS