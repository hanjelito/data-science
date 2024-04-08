import pandas as pd
import datetime
import time
from sqlalchemy import create_engine, text

def connect():
    db_url = 'postgresql+psycopg2://juan-gon:mysecretpassword@localhost:5432/piscineds'
    engine = create_engine(db_url)
    return engine
engine = connect()
    
def create_new_table(table_name):
    start_time = time.time()

    with engine.connect() as conn:
        # sql_command = f"""
        # DROP TABLE IF EXISTS {table_name};
        # CREATE TABLE tester AS
        # SELECT DISTINCT ON (event_type, product_id, price, user_id, user_session)
        # event_time, event_type, product_id, price, user_id, user_session
        # FROM customers
        # ORDER BY event_type, product_id, price, user_id, user_session, event_time;
        # """
        sql_command = f"""
        DROP TABLE IF EXISTS {table_name};
        CREATE TABLE {table_name} AS
        WITH RankedEvents AS (
            SELECT 
                event_time, 
                event_type, 
                product_id, 
                price, 
                user_id, 
                user_session,
                ROW_NUMBER() OVER (
                    PARTITION BY 
                        event_type, 
                        product_id, 
                        user_id, 
                        user_session, 
                        DATE_TRUNC('minute', event_time)
                ) AS rn
            FROM 
                customers
        )
        SELECT 
            event_time, 
            event_type, 
            product_id, 
            price, 
            user_id, 
            user_session
        FROM 
            RankedEvents
        WHERE 
            rn = 1;
        """
        result = conn.execute(text(sql_command))
        conn.commit()

        print(f"Generated {result.rowcount} rows")
    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time:.2f} seconds") 

def rename_table():
    """
    Renames the table 'tester' to 'customers'
    """
    start_time = time.time()
    
    with engine.connect() as conn:
        sql_command = f"""
        DROP TABLE IF EXISTS customers;
        ALTER TABLE tester RENAME TO customers;
        """
        result = conn.execute(text(sql_command))
        conn.commit()
        print(f"Generated {result.rowcount} rows")
    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time:.2f} seconds")

def main():
    create_new_table("tester")
    rename_table()


if __name__ == "__main__":
    main()
    
# -- select * from tester c where user_session = '49e8d843-adf3-428b-a2c3-fe8bc6a307c9'
# -- select * from tester c where user_session = '49e8d843-adf3-428b-a2c3-fe8bc6a307c9' and product_id = 5779403
# -- select * from customers c where user_session = '49e8d843-adf3-428b-a2c3-fe8bc6a307c9' and product_id = 5779403
# -- select * from customers c where event_time = '2022-10-01 00:00:32'
