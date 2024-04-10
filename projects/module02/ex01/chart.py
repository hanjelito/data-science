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
    

def columnes_count(table_name: str, start_date: str, end_date: str, event_type_filter: str) -> any:
    try:
        start_time = time.time()
        assert engine.connect(), "Error: Could not connect to the database"
        with engine.connect() as conn:
            sql_command = f"""
            SELECT DATE(event_time) AS event_day, COUNT(*) AS event_count
			FROM {table_name}
			WHERE event_time >= :start_date AND event_time < :end_date
			AND event_type = :event_type_filter
			GROUP BY event_day;
            """
            result = conn.execute(text(sql_command), {'start_date': start_date, 'end_date': end_date, 'event_type_filter': event_type_filter})

            print(f"Generated {result.rowcount} rows")
        end_time = time.time()
        print(f"Elapsed time: {end_time - start_time:.2f} seconds")
        return result.fetchall()

    except AssertionError as e:
        print(f"Error: {e}")

def generate_time_series_chart(data):
    df = pd.DataFrame(data, columns=['event_time', 'event_count'])
    df['event_time'] = pd.to_datetime(df['event_time'])
    df.set_index('event_time', inplace=True)

    df.resample('D').sum().plot()
    plt.ylabel('Number of costumers')
    plt.xlabel('month')
    plt.legend().remove()
    plt.tight_layout()
    plt.savefig('number_of_costumers.png')
    plt.close()
    
def generate_monthly_sales_chart(data):
    # Asegúrate de que los datos están en el formato correcto:
    # [(date1, count1), (date2, count2), ...]
    
    df = pd.DataFrame(data, columns=['event_day', 'event_count'])
    
    # Convertimos 'event_day' a datetime si no lo es ya
    df['event_day'] = pd.to_datetime(df['event_day'])
    
    # Truncamos las fechas al primer día de cada mes y agrupamos por esta nueva columna
    df['month'] = df['event_day'].dt.to_period('M')
    monthly_data = df.groupby('month')['event_count'].sum().reset_index()
    
    # Convertimos 'month' a cadena para que sea más legible
    monthly_data['month'] = monthly_data['month'].dt.strftime('%b %Y')
    
    # Creamos el gráfico
    ax = monthly_data.plot(kind='bar', x='month', y='event_count', legend=False, color='skyblue')
    ax.set_title('Total Sales per Month')
    ax.set_xlabel('Month')
    ax.set_ylabel('Total Sales')
    
    # Formateamos los ticks del eje y para que sean legibles
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    
    # Asegúrate de que las etiquetas del eje x sean legibles
    ax.set_xticklabels(monthly_data['month'], rotation=45)
    
    plt.tight_layout()
    plt.savefig('monthly_sales_chart.png')
    plt.close()



def main():
	result = columnes_count('customers', '2022-10-01', '2023-03-01', 'purchase')
	generate_time_series_chart(result)
	generate_monthly_sales_chart(result)
 

if __name__ == "__main__":
    main()
  
  
  
#   WHERE event_time >= '2022-10-01' AND event_time < '2023-02-01'
