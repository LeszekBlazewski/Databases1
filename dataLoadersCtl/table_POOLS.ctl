load data 
CHARACTERSET UTF8
infile '/databaseData/PoolData.csv' 
append
into table POOLS
fields terminated by ','
(ID,NUMBEROFPLACES,REQUIREDSKILL,SPOTPRICE)