create or replace PROCEDURE ENABLE_ALL_CONSTRAINT
IS
BEGIN
-- Enable all constraint except foreign key
for i IN (select table_name, constraint_name
from user_constraints
where status = 'DISABLED'
and constraint_type!='R')
loop
EXECUTE IMMEDIATE 'alter table'||i.table_name||'enable novalidate constraint'||i.constraint_name;
end loop i;

-- Enable foreign key constraint
for i IN (select table_name, constraint_name
from user_constraints
where constraint_type ='R'
and status = 'DISABLED')
loop
EXECUTE IMMEDIATE 'alter table'||i.table_name||' enable novalidate constraint'||i.constraint_name;
end loop i;
END;


create or replace PROCEDURE DISABLE_ALL_CONSTRAINT
IS
BEGIN
-- Disable foreign key constraint
for i IN (select table_name, constraint_name
from user_constraints
where constraint_type ='R'
and status = 'ENABLED')
loop
EXECUTE IMMEDIATE 'alter table'||i.table_name||' disable constraint'||i.constraint_name;
end loop i;

-- Disable rest of the constraint
for i IN (select table_name, constraint_name
from user_constraints
where status = 'ENABLED')
loop
EXECUTE IMMEDIATE 'alter table'||i.table_name||' disable constraint'||i.constraint_name;
end loop i;
END;