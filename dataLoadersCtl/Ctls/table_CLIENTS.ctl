load data 
CHARACTERSET UTF8
infile '../databaseData/ClientData.csv' 
append
into table CLIENTS
fields terminated by ','
(ID_C,NAME,SURNAME,PERSONALIDENTITYNUMBER,PHONENUMBER,SWIMMINGSKILL,AGE)