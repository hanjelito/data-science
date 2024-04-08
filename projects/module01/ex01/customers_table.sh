#!/bin/bash

DB_HOST="localhost"
DB_USER="juan-gon"
PGPASSWORD='mysecretpassword'
DATABASE="piscineds"
DATA_FIND='data_20'
DATABASE_NEW="customers"

export PGPASSWORD


table=$(psql -h "$DB_HOST" -U "$DB_USER" -d "$DATABASE" -c "\dt" | grep "$DATA_FIND" | awk '{print $3}')

first_table=$(echo $table | cut -d' ' -f1)

psql -h "$DB_HOST" -U "$DB_USER" -q -d "$DATABASE" <<-EOSQL
DO
\$do\$
BEGIN
    IF NOT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '$DATABASE_NEW') THEN
        EXECUTE 'CREATE TABLE $DATABASE_NEW AS SELECT * FROM ' || quote_ident('$first_table') || ' WHERE FALSE';
    END IF;
END
\$do\$
EOSQL

for tabla in $table; do
    echo "Into db $tabla in '$DATABASE_NEW'..."
    psql -h "$DB_HOST" -U "$DB_USER" -q -d "$DATABASE" <<-EOSQL
        INSERT INTO $DATABASE_NEW SELECT * FROM $tabla;
EOSQL
done

echo "Finish process"


# sudo systemctl restart postgresql