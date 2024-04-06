import pandas as pd
from tqdm import tqdm 
from sqlalchemy import create_engine, types, dialects
import sys

def csv_to_sql(name_file: str):
    csv_file_path = '/vagrant/store/modulo00/customer/' + name_file
    db_url = 'postgresql+psycopg2://juan-gon:mysecretpassword@localhost:5432/piscineds'
    db = create_engine(db_url)

    try:
        assert db.connect(), "Error: Could not connect to the database"
        chunksize = 10000
        dtype = {'event_time': types.TIMESTAMP,
                 'product_id': dialects.postgresql.INTEGER,
                 'price': dialects.postgresql.FLOAT,
                 'user_id': dialects.postgresql.BIGINT,
                 'user_session': dialects.postgresql.UUID,
                }

        with tqdm(desc="Loading data", unit="chunk", ncols=100) as pbar:
            for chunk in pd.read_csv(csv_file_path, chunksize=chunksize):
                if 'event_time' in chunk.columns:
                    chunk['event_time'] = pd.to_datetime(chunk['event_time'])
                chunk.to_sql(name_file[:-4], db, index=False, if_exists='append', dtype=dtype)
                pbar.update(1)
    except AssertionError as e:
        print(f"AssertionError: {e}")
        return None

def main():
    csv_to_sql("data_2022_oct.csv")

if __name__ == "__main__":
    main()
    
