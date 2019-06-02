#!/bin/bash
sqlldr control='./table_CLIENTS.ctl' userid=Beard/Test1@XE
sqlldr control='./table_POOLS.ctl' userid=Beard/Test1@XE
sqlldr control='./table_RESERVATIONS.ctl' userid=Beard/Test1@XE
sqlldr control='./table_SCHEDULES.ctl' userid=Beard/Test1@XE
sqlldr control='./table_STAFF.ctl' userid=Beard/Test1@XE