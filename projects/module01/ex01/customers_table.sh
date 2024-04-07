#!/bin/bash

# Conexión a la base de datos PostgreSQL
DATABASE="piscineds"
DATABASE_NEW="customer"
USER="username"
PASSWORD="password"


tablas=$(sudo -u postgres psql -d "$DATABASE" -c "\dt" | grep "data_20" | awk '{print $3}')

# Identificar la estructura de las tablas para determinar los campos
for tabla in $tablas; do
    echo "Estructura de la tabla $tabla:"
    sudo -u postgres psql -d "$DATABASE" -c "\d $tabla"
done

# Crear la tabla 'customer' si no existe con los campos identificados
# Debes definir esta estructura manualmente basada en la salida del paso anterior
sudo -u postgres psql -d "$DATABASE" <<-EOSQL
    CREATE TABLE IF NOT EXISTS customer (
        event_time TIMESTAMP,
        product_id INTEGER,
        price FLOAT,
        user_id BIGINT,
        user_session UUID,
        PRIMARY KEY (event_time, product_id, user_id)  -- Ajusta según la lógica de tus datos
    );
EOSQL
echo "Proceso completado."
