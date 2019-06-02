load data 
CHARACTERSET UTF8
infile '../databaseData/ReservationData.csv' 
append
into table RESERVATIONS
fields terminated by ','
(ID_CLIENT,ID_POOL,RESERVATIONDATE,STARTTIME,ENDTIME,PRICE)