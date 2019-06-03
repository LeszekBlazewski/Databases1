-- automatically archives old reservations and updates data related to affected removed rows
create or replace PROCEDURE ARCHIVE_RESERVATIONS AS
currentDate DATE;
currentTime NUMBER;
-- temporary table for storing grouped result of reservations group by
TYPE GROUPED_POOLS_DATA IS RECORD(
    id_pool NUMBER,  -- Stores rows with poll id
    total_number_of_places NUMBER ); -- and total number of outdate reservations for each pool
-- declare the type of table
TYPE archived_reservations_t IS TABLE OF GROUPED_POOLS_DATA;
-- declare the actual table which will store the result
archived_reservations archived_reservations_t; 
BEGIN
  -- get current date without time
  currentDate := TRUNC(CURRENT_DATE);
  -- get current hour with minutes as number
  currentTime := EXTRACT(HOUR from current_timestamp) + EXTRACT(MINUTE from current_timestamp)/60; 
    
  -- Insert into RESERVATIONS_HISTORY table all reservations which date is older
  -- than current date or equal to it and endtime is older than current time
  INSERT INTO reservations_history
  SELECT * FROM RESERVATIONS
  WHERE reservationdate < currentDate OR (reservationdate=currentDate AND endtime <= currenttime);
  
  -- Calculate for each pool the sum of occupied places by reservations which will be deleted
  SELECT id_pool, COUNT(id_pool) BULK COLLECT INTO archived_reservations
  FROM RESERVATIONS
  WHERE reservationdate < currentDate OR (reservationdate=currentDate AND endtime <= currenttime)
  GROUP BY id_pool;
  
  -- Iterate over each row and update the correct pool
  FORALL pool_index IN 1 .. archived_reservations.COUNT SAVE EXCEPTIONS
    UPDATE POOLS
    SET numberofplaces=numberofplaces + archived_reservations(pool_index).total_number_of_places
    WHERE id_p = archived_reservations(pool_index).id_pool;
    
  -- Delete the rows from RESERVATIONS table
  DELETE FROM RESERVATIONS
  WHERE reservationdate < currentDate OR (reservationdate=currentDate AND endtime <= currenttime);
END ARCHIVE_RESERVATIONS;

-- To run it periodically create a suitable job for it
BEGIN
    DBMS_SCHEDULER.CREATE_JOB (
            job_name => 'ARCHIVE_RESERVATIONS_JOB',
            job_type => 'STORED_PROCEDURE',
            job_action => 'ARCHIVE_RESERVATIONS',
            number_of_arguments => 0,
            start_date => NULL,
            repeat_interval => 'FREQ=MINUTELY;INTERVAL=30',
            end_date => NULL,
            enabled => TRUE,
            auto_drop => FALSE,
            comments => 'Removes old rows from reservation table, inserts them into
            reservations_history and updates number of places for required pools');
END;