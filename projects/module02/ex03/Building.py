import pandas as pd
import time
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import seaborn as sns
import numpy as np



def connect():
    db_url = 'postgresql+psycopg2://juan-gon:mysecretpassword@localhost:5432/piscineds'
    engine = create_engine(db_url)
    return engine

try:
    engine = connect()
except SQLAlchemyError as e:
    print(f"Error: {e}")
    
    
def frequency(table: str) -> None:
	try:
		start_time = time.time()
		sql_command = """
		SELECT
			user_id,
			COUNT(*) AS frequency
		FROM
			customers
		WHERE
			event_type = 'purchase'
		GROUP BY
			user_id;
		""".format(table)
		
		with engine.connect() as conn:
			df = pd.read_sql(sql_command, conn)
		
		# Agrupamos por frecuencia		
		df['frequency_group'] = pd.cut(df['frequency'], bins=range(0, df['frequency'].max() + 10, 10), right=False)
		grouped_df = df.groupby('frequency_group', observed=True).size().reset_index(name='number_of_users')

		mean_frequency = grouped_df['number_of_users'].mean()
		
		# Filtramos para obtener solo las frecuencias mayores o iguales a la media
		filtered_df = grouped_df[grouped_df['number_of_users'] >= mean_frequency]
		end_time = time.time()
		print(f"Elapsed time: {end_time - start_time:.2f} seconds\n")


		plt.figure(figsize=(10,10))
		plt.bar([str(x.left) + '-' + str(x.right) for x in filtered_df['frequency_group']], filtered_df['number_of_users'])
		plt.xlabel('Frecuency')
		plt.ylabel('Customers')

		plt.xticks(rotation=0)
		
		plt.tight_layout()
		plt.savefig("frequency.png")
		plt.close()
			
	except Exception as e:
		print(f"Error: {e}")
		return None

def monetary_value(table: str) -> None:
	try:
		start_time = time.time()
		sql_command = f"""
		SELECT
			user_id,
			SUM(CASE WHEN price > 0 THEN price ELSE 0 END)::NUMERIC AS altairian_dollars_spent
		FROM
			{table}
		WHERE
			event_type = 'purchase'
		GROUP BY
			user_id;
		"""
		
		with engine.connect() as conn:
			df = pd.read_sql(sql_command, conn)
		
		bins = [-24, 24, 74, 124, 174, 224]
		labels = ["0", "50", "100", "150", "200"]
		df['range'] = pd.cut(df['altairian_dollars_spent'], bins=bins, labels=labels, include_lowest=True)

		customer_count = df['range'].value_counts().sort_index().reset_index(name='customers')
		customer_count.columns = ['range', 'customers']

		plt.figure(figsize=(10, 6))
		plt.bar(customer_count['range'], customer_count['customers'], color='skyblue')
		plt.xticks(rotation=0)
		plt.ylim(0, customer_count['customers'].max() * 1.1)
		plt.xlabel('Monetary Value in $')
		plt.ylabel('Customers')
		plt.savefig("monetary_value.png")
		plt.close()
			
	except Exception as e:
		print(f"Error: {e}")
		return None

def main():
    frequency('customers')
    monetary_value('customers')

if __name__ == '__main__':
    main()