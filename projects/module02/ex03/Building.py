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
		print(filtered_df.head(10))
		plt.figure(figsize=(10,10))

		plt.bar([str(x.left) + '-' + str(x.right) for x in filtered_df['frequency_group']], filtered_df['number_of_users'])
		plt.xlabel('Frecuency')
		plt.ylabel('Customers')

		plt.xticks(rotation=0)
		
		plt.tight_layout()
		plt.savefig("test.png")
		plt.close()
			
	except Exception as e:
		print(f"Error: {e}")
		return None

def main():
    frequency('orders')

if __name__ == '__main__':
    main()