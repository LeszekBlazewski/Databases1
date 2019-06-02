load data 
CHARACTERSET UTF8
infile '../databaseData/StaffData.csv' 
append
into table STAFF
fields terminated by ','
TRAILING NULLCOLS
(ID_S,NAME,SURNAME,SALARY,JOB,SUPERVISOR)
