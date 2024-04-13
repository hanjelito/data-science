import pandas as pd
import datetime
import time
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import matplotlib.pyplot as plt

def connect():
    db_url = 'postgresql+psycopg2://juan-gon:mysecretpassword@localhost:5432/piscineds'
    engine = create_engine(db_url)
    return engine

try:
	engine = connect()
except SQLAlchemyError as e:
	print(f"Error: {e}")
    

def columnes_count(table_name :str, start_date :str, end_date :str)->any:
	try:
		start_time = time.time()
		assert engine.connect(), "Error: Could not connect to the database"
		with engine.connect() as conn:
			sql_command = f"""
			SELECT event_type, COUNT(*) AS event_count
			FROM {table_name}
			WHERE
				event_time >= :start_date AND event_time < :end_date
			GROUP BY event_type;
			"""
			result = conn.execute(text(sql_command), {'start_date': start_date, 'end_date': end_date})

			print(f"Generated {result.rowcount} rows")
		end_time = time.time()
		print(f"Elapsed time: {end_time - start_time:.2f} seconds")
		return result;

	except AssertionError as e:
		print(f"Error: {e}")

def generate_pie(result: any):
    df = pd.DataFrame(result.fetchall(), columns=result.keys())
    df = df.sort_values(by='event_count', ascending=False)
    fig, ax = plt.subplots()
    df.plot.pie(y='event_count', labels=df['event_type'], autopct='%1.1f%%', startangle=0, ax=ax)
    ax.legend().remove()
    ax.set_xlabel('')
    ax.set_ylabel('')
    plt.savefig('event_type_distribution.png', bbox_inches='tight')

def main():
	result = columnes_count("customers", "2022-10-01", "2023-02-01")
	generate_pie(result)
 

if __name__ == "__main__":
    main()
  
  
  
#   WHERE event_time >= '2022-10-01' AND event_time < '2023-02-01'
