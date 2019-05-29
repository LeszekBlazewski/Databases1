load data 
CHARACTERSET UTF8
infile '/databaseData/ScheduleData.csv' 
append
into table SCHEDULES
fields terminated by ','
(STAFFID,POOLID,STARTTIME,ENDTIME,DAYOFWEEK)