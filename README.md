# DataBases1

## Introduction

This repository contains work done for the Databases class at Wrocław University of Science and Technology.

## Main target

We were supposed to design and implement a simple database which would help SwimmingPools with data maintenance and information flow.

## What can I find here ?

Repository contains full database dump which can be used with ORACLE DATA PUMP tool to create your own instance.

I have also included implemented data generators written during the process of implementation.

The last thing you can find here are some fancy triggers and PL/SQL procedures which were used to meet given project specification.

## Used technologies & Tools

- Oracle database 11G express edition

- docker

- Python - Faker, Numpy, Pandas

## Full project documentation

If you are a **polish** reader I highly recommend checking the full project documentation which was submitted to the lecturer.

## How can I check it out ?

### Requirements

First you need to make sure that you possess all of the required dependencies and plugins.

#### 1. Install docker if you don't possess this awesome tool.

#### 2. Install the required dependencies.

```bash
pip install -r requirements.txt
```

#### 3.Download official Oracle database 11G express edition docker image from Oracle.

#### 4.Spin up your container by running following command.

```docker
docker run --name oracleDb \
--shm-size=1g \
-p 1521:1521 -p 8080:8080 \
-e ORACLE_PWD=Test \
-v ~/docker/oracle-xe:/u01/app/oracle/oradata \
oracle/database:11.2.0.2-xe
```

#### 5.Start your oracle container

```docker
docker start oracleDb
```

#### 6. Get hands on your container

```bash
docker exec -it oracleDb bash
```

#### 7. Now you can use SQL PLUS to interact with the database

```bash
sqlplus username/password@SID
```

### Create duplicate of database implemented in project

#### 1. Go to the container && make directory for dump

```docker
docker exec -it oracleDb bash
mkdir export && chmod a+rwx ./export
```

#### 2. Copy dump file to the container from DataLoadersCtl on your host

```docker
docker cp ./full_dump.dmp oracleDb:/export/full_dump.dmp
```

#### 3. Get back to container and create directory for export in oracle system database

```sql
sqlplus / as sysdba
CREATE DIRECTORY export AS '/export/';
GRANT read, write ON DIRECTORY export TO username;
```

#### 4. Use ORACLE DATA PUMP TO GENERATE YOUR DATABASE

```docker
impdp username DUMPFILE=export:full_dump.dmp FULL=YES LOGFILE=export:full_imp.log
```

#### 5. Enjoy the database

### Importing data to already created database

#### 1. In order to generate data move to the DataLoaders directory and execute

```bash
python CSVCreator.py
```

#### 2. Move to the dataLoadersCtl folder and copy the data and ctls folder into your container

```bash
docker cp databaseData/. oracleDb:/databaseData
docker cp Ctls/. oracleDb:/Ctls
```

#### 3. Get hands on your container

```bash
docker exec -it oracleDb bash
```

#### 4. Move to the correct directory and run your script

```bash
cd ./Ctls && chmod +x ./loadData.sh && ./loadData.sh
```

## Generators

DataLoaders folder contains all of the generators which are able to create given number of rows for each table in database.

### Format of data

Data is returned as CSV files which are then loaded using the SQL*Loader tool provided by oracle. This solution ensures maximal speed and optimization.

### Used libraries in scripts

Most of the data is pulled from faker library which posses language specific data sets. Some of the easier concepts are simply generated from math functions or calculated. Pandas was used to easily convert python lists into data frames and then write to csv files. Numpy was used to generate random float data used in currency fields and time.

## PL/SQL, Triggers, Procedures

SQL folder inside dataLoadersCtl folder includes some of the triggers and procedures which are responsible for ensuring data integrity in the database.
