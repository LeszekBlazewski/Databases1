load data 
CHARACTERSET UTF8
infile '../databaseData/PoolData.csv' 
append
into table POOLS
fields terminated by ','
TRAILING NULLCOLS
(ID_P,NUMBEROFPLACES,REQUIREDSKILL,SPOTPRICE)