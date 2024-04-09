import pandas as pd
import datetime
import time
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def connect():
    db_url = 'postgresql+psycopg2://juan-gon:mysecretpassword@localhost:5432/piscineds'
    engine = create_engine(db_url)
    return engine

try:
    engine = connect()
except SQLAlchemyError as e:
    print(f"Error: {e}")


def create_new_colums():
	start_time = time.time()

	with engine.connect() as conn:
		sql_command = f"""
		ALTER TABLE customers
		ADD COLUMN category_id BIGINT,
		ADD COLUMN category_code TEXT,
		ADD COLUMN brand TEXT;
		"""
		result = conn.execute(text(sql_command))
		conn.commit()

		print(f"Generated {result.rowcount} rows")
	end_time = time.time()
	print(f"Elapsed time: {end_time - start_time:.2f} seconds")

def remove_colums():
	start_time = time.time()
 
	with engine.connect() as conn:
		sql_command = f"""
		ALTER TABLE customers
		DROP COLUMN category_id,
		DROP COLUMN category_code,
		DROP COLUMN brand;
		"""
		result = conn.execute(text(sql_command))
		conn.commit()
		print(f"Generated {result.rowcount} rows")
	end_time = time.time()
	print(f"Elapsed time: {end_time - start_time:.2f} seconds")
 
def fusion_items():
	start_time = time.time()
 
	with engine.connect() as conn:
		sql_command = f"""
		UPDATE customers c
		SET
			category_id = i.category_id,
			category_code = i.category_code,
			brand = i.brand
		FROM item i
		WHERE c.product_id = i.product_id
			AND i.category_id IS NOT NULL
        	AND i.category_code IS NOT NULL
        	AND i.brand IS NOT NULL;
		"""
		result = conn.execute(text(sql_command))
		conn.commit()
		print(f"Generated {result.rowcount} rows")
	end_time = time.time()
	print(f"Elapsed time: {end_time - start_time:.2f} seconds")


 
def main():
	create_new_colums()
	# remove_colums()
	fusion_items()
  
if __name__ == "__main__":
	main()
 
# select * from customers c where category_id = 1487580005268456192 limit 10;
# select  * from  customers c where category_code = 'furniture.bathroom.bath' limit 10;
# 13647049
