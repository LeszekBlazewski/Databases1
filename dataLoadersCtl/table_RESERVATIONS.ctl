load data 
CHARACTERSET UTF8
infile '/databaseData/ReservationData.csv' 
append
into table RESERVATIONS
fields terminated by ','
(CLIENTID,POOLID,RESERVATIONDATE,STARTTIME,ENDTIME,PRICE)