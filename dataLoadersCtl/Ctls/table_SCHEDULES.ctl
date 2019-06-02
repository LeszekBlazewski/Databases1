load data 
CHARACTERSET UTF8
infile '../databaseData/ScheduleData.csv' 
append
into table SCHEDULES
fields terminated by ','
TRAILING NULLCOLS
(ID_STAFF,ID_POOL,STARTTIME,ENDTIME,DAYOFWEEK)