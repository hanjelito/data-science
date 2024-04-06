#!/bin/bash
sudo -u postgres psql -c "CREATE USER \"juan-gon\" WITH SUPERUSER PASSWORD 'mysecretpassword';"
sudo -u postgres psql -c "CREATE DATABASE piscineds OWNER \"juan-gon\";"

echo "Usuario y base de datos de PostgreSQL configurados."

# head -n 3 '/vagrant/store/modulo00/customer/data_2022_dec.csv'
    

# TRUNCATE TABLE nombre_tabla;
# DROP TABLE tabla1, tabla2, tabla3;
# DROP DATABASE nombre_base_datos;


# psql -U juan-gon -d piscineds -h localhost -W

# delete DB
# sudo -u postgres psql -c "DROP DATABASE IF EXISTS piscineds;"
# delete tabla:
# sudo -u postgres psql -c "DROP USER \"juan-gon\";"