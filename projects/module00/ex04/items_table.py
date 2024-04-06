import subprocess
import time
import pandas as pd
from tqdm import tqdm 
from sqlalchemy import create_engine, types, dialects


def connect():
    db_url = 'postgresql+psycopg2://juan-gon:mysecretpassword@localhost:5432/piscineds'
    return create_engine(db_url)

def list_files(directory):
    db = connect()
    try:
        process = subprocess.Popen(['ls', directory], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        files = stdout.decode()
        assert db, "Error: Could not connect to the database"
        dtype = {
                 'product_id': dialects.postgresql.INTEGER,
                 'category_id': dialects.postgresql.BIGINT,
                 'brand': dialects.postgresql.VARCHAR,
                }
        for file in files.split('\n'):
            if file != '':
                print(file)
                time.sleep(1)
                df = pd.read_csv(directory + file, nrows=0)
                df.to_sql(file[:-4], db, index=False, if_exists='append', dtype=dtype)
                # df.to_sql(file[:-4], db, index=False, if_exists='append')
                csv_to_sql_bash(directory + file, file[:-4])
            else:
                break
    except AssertionError as e:
        print(f"AssertionError: {e}")
        return None

def csv_to_sql_bash(name_file: str, table_name: str):
    engine = connect()
    connection = engine.raw_connection()
    cursor = connection.cursor()
    try:
        with open(name_file, 'r') as f:
            cursor.copy_expert(f"COPY {table_name} FROM STDIN WITH CSV HEADER", f)
        connection.commit()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()


def main():
    list_files('/vagrant/store/modulo00/item/')
    

if __name__ == "__main__":
    main()
