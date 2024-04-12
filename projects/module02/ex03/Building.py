import pandas as pd
import time
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import seaborn as sns



def connect():
    db_url = 'postgresql+psycopg2://juan-gon:mysecretpassword@localhost:5432/piscineds'
    engine = create_engine(db_url)
    return engine

try:
    engine = connect()
except SQLAlchemyError as e:
    print(f"Error: {e}")
    
    
def frequency(table: str)-> None:
	try:
		start_time = time.time()
		sql_command = f"""
            SELECT
			user_id,
			SUM(price) AS total_spent
			FROM
			customers
			WHERE
			event_type = 'purchase'
			GROUP BY
			user_id
			ORDER BY
			total_spent;
					"""
		with engine.connect() as conn:
			df = pd.read_sql(sql_command, conn)
		end_time = time.time()
		print(f"Elapsed time: {end_time - start_time:.2f} seconds\n")

		plt.figure(figsize=(10,6))
		df['total_spent'].hist(bins=10, color='blue', alpha=0.7)
		plt.xlabel('Frecuency')
		plt.ylabel('Customers')
		plt.savefig("test.png")
		plt.close()
			
	except Exception as e:
		print(f"Error: {e}")
		return None
    
def main():
    frequency('orders')

if __name__ == '__main__':
    main()