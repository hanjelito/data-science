from sqlalchemy import create_engine, text, Table, MetaData

# Función para conectarse a la base de datos
def connect():
    db_url = 'postgresql+psycopg2://juan-gon:mysecretpassword@localhost:5432/piscineds'
    engine = create_engine(db_url)
    table_metadata = MetaData()  # No 'bind' argument here
    return engine, table_metadata

def create_customer_table(engine, table_metadata):
    with engine.connect() as conn:
        table_metadata.bind = engine  # Bind metadata before table creation
        sql_query = """
        CREATE TABLE papita AS
        SELECT * FROM data_2022_dec
            UNION
        SELECT * FROM data_2022_nov;
        """
        try:
            conn.execute(text(sql_query))
            print("Tabla 'customer' creada con éxito")
        except Exception as e:
            print(f"Error al crear la tabla: {e}")


# Conectando a la base de datos
print("Conectando a la base de datos...")
engine, table_metadata = connect()
print("Conexión exitosa")

# Creando tabla 'customer'
print("Creando tabla 'customer'...")
create_customer_table(engine, table_metadata)

