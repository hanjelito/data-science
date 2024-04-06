#!/bin/bash


sudo apt-get install -y postgresql postgresql-contrib

# Configura PostgreSQL para aceptar conexiones de cualquier dirección
POSTGRESQL_CONF=$(sudo -u postgres psql -c "SHOW config_file;" | grep -m 1 '/' | xargs)
PG_HBA_CONF=$(sudo -u postgres psql -c "SHOW hba_file;" | grep -m 1 '/' | xargs)

# Reemplaza listen_addresses y añade reglas a pg_hba.conf
sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" "$POSTGRESQL_CONF"
echo "host    all             all             all                     md5" | sudo tee -a "$PG_HBA_CONF"

# Reinicia PostgreSQL para aplicar los cambios
sudo systemctl restart postgresql

# Configura el usuario de PostgreSQL y la base de datos automáticamente
sudo -u postgres psql -c "CREATE USER \"juan-gon\" WITH SUPERUSER PASSWORD 'mysecretpassword';"
sudo -u postgres psql -c "CREATE DATABASE piscineds OWNER \"juan-gon\";"

echo "Usuario y base de datos de PostgreSQL configurados."