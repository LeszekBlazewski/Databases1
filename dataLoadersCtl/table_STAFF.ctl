load data 
CHARACTERSET UTF8
infile '/databaseData/StaffData.csv' 
append
into table STAFF
fields terminated by ','
TRAILING NULLCOLS
(ID,NAME,SURNAME,SALARY,JOB,SUPERVISOR)
