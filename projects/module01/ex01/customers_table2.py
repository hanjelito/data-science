# from sqlalchemy import create_engine
import pandas as pd
from sqlalchemy import create_engine
from psycopg2.errors import DuplicateDatabase

def connect():
    db_url = 'postgresql+psycopg2://juan-gon:mysecretpassword@localhost:5432/piscineds'
    return create_engine(db_url)


        
def create_database(engine, db_structure, table_name):
    with engine.connect() as conn:
        for _, table_schema in db_structure.items():  # Ignoramos la clave original del diccionario
            columns_sql = ", ".join([
                f"{column} {details['data_type']} {'NOT NULL' if details['is_nullable'] == 'NO' else ''}"
                for column, details in table_schema.items()
            ])

            create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql})"
            try:
                conn.execute(create_table_sql)
                print(f"Table '{table_name}' created successfully.")
            except Exception as e:
                print(f"An error occurred while creating table '{table_name}': {e}")
    
def detect_db(engine):

    query_similar_tables = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema='public' AND table_name LIKE 'data_20%%'
    """
    try:
        tables = pd.read_sql_query(query_similar_tables, engine)['table_name']
        db_structure = struct_db(engine, tables)

        return db_structure;
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def struct_db(engine, tables):
 
	db_structure = {}
	for table in tables:
		query_columns = f"""
		SELECT column_name, data_type, is_nullable
		FROM information_schema.columns
		WHERE table_schema = 'public' AND table_name = '{table}'
		"""
		columns = pd.read_sql_query(query_columns, engine)
		month_data = {row['column_name']: {'data_type': row['data_type'], 'is_nullable': row['is_nullable']} for index, row in columns.iterrows()}

		# Comprobar si la información del mes ya está presente
		if month_data not in db_structure.values():
			db_structure[table] = month_data

	print(db_structure)
	create_database(engine, db_structure, "customers")

def main():
	engine =  connect()
	detect_db(engine)


if __name__ == "__main__":
    main()