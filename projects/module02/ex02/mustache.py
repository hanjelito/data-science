import pandas as pd
import numpy as np
import datetime
import time
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import matplotlib.dates as mdates
import seaborn as sns


def connect():
    db_url = 'postgresql+psycopg2://juan-gon:mysecretpassword@localhost:5432/piscineds'
    engine = create_engine(db_url)
    return engine

try:
    engine = connect()
except SQLAlchemyError as e:
    print(f"Error: {e}")

def mustache_rider(table: str, start: str, end: str):
	try:
		start_time = time.time()
		with engine.connect() as conn:
			sql_command = f"""
			SELECT
				count(*) as count,
				AVG(price) AS mean,
				STDDEV(price) AS std_dev,
				MIN(price) AS min_price,
				MAX(price) AS max_price,
				percentile_cont(0.25) WITHIN GROUP (ORDER BY price) AS first_quartile,
				percentile_cont(0.50) WITHIN GROUP (ORDER BY price) AS median,
				percentile_cont(0.75) WITHIN GROUP (ORDER BY price) AS third_quartile
			FROM {table}
			where event_type = 'purchase'
			"""
   
			result = conn.execute(text(sql_command))
			print(f"Generated {result.rowcount} rows")
			end_time = time.time()
			print(f"Elapsed time: {end_time - start_time:.2f} seconds\n")
			return result.fetchall()
	except Exception as e:
		print(f"Error: {e}")
		return None

def mustache_rider_day(table: str, start: str, end: str):
    try:
        start_time = time.time()
        with engine.connect() as conn:

            sql_command = f"""
            SELECT
                DATE(event_time) AS date,
                COUNT(*) AS count,
                AVG(price) AS mean,
                STDDEV(price) AS std_dev,
                MIN(price) AS min_price,
                MAX(price) AS max_price,
                PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY price) AS first_quartile,
                PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY price) AS median,
                PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY price) AS third_quartile
            FROM {table}
            WHERE event_type = 'purchase'
            GROUP BY DATE(event_time)
            ORDER BY DATE(event_time);  -- Ensure order by date
            """

            result = conn.execute(text(sql_command))
            print(f"Generated {result.rowcount} rows")
            end_time = time.time()
            print(f"Elapsed time: {end_time - start_time:.2f} seconds\n")
            return result.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        return None

def mustache_data(data):
	df = pd.DataFrame(data)
	max_width = max(
	len(f"{df['count'].iloc[0]:,.6f}"),
	len(f"{df['mean'].iloc[0]:,.6f}"),
	len(f"{df['std_dev'].iloc[0]:,.6f}"),
	len(f"{df['min_price'].iloc[0]:,.6f}"),
	len(f"{df['first_quartile'].iloc[0]:,.6f}"),
	len(f"{df['median'].iloc[0]:,.6f}"),
	len(f"{df['third_quartile'].iloc[0]:,.6f}"),
	len(f"{df['max_price'].iloc[0]:,.6f}")
	)

	print(
		f"count:	{df['count'].iloc[0]:>{max_width}.6f}\n"
		f"mean:	{df['mean'].iloc[0]:>{max_width}.6f}\n"
		f"std:	{df['std_dev'].iloc[0]:>{max_width},.6f}\n"
		f"min:	{df['min_price'].iloc[0]:>{max_width}.6f}\n"
		f"25%:	{df['first_quartile'].iloc[0]:>{max_width}.6f}\n"
		f"50%:	{df['median'].iloc[0]:>{max_width}.6f}\n"
		f"75%:	{df['third_quartile'].iloc[0]:>{max_width}.6f}\n"
		f"max:	{df['max_price'].iloc[0]:>{max_width}.6f}"
	)

def generate_box_plot():
    datos = {
		"count": 1286045.0,
		"mean": 4.932943,
		"std": 8.925811,
		"min": -79.37,
		"25%": 1.59,
		"50%": 3.0,
		"75%": 5.4,
		"max": 327.78
	}

    # Configurar el estilo del gráfico (esto es opcional y puede ser modificado para coincidir con el estilo deseado)
    sns.set(style="whitegrid")
    
    # Crear el gráfico de caja y bigotes con Seaborn, que automáticamente añadirá los puntos atípicos
    ax = sns.boxplot(x=datos, width=0.3)

    # Superponer un stripplot para mostrar todos los puntos de datos
    sns.stripplot(x=datos, color='grey', alpha=0.6, jitter=True)

    # Configurar títulos y etiquetas
    ax.set_title('Gráfico de Caja y Bigotes')
    ax.set_xlabel('Precio')
    
    # Configurar los límites del eje X si es necesario
    ax.set_xlim(-50, 350)

	# Guardar la imagen
    plt.savefig("test.png")

	# Cerrar la ventana del diagrama
    plt.close()
		

def main():
    # result = mustache_rider('customers', '2022-10-01', '2023-03-01')
    # mustache_data(result)
    # result = mustache_rider_day('customers', '2022-10-01', '2023-03-01')
    generate_box_plot()
    
if __name__ == "__main__":
    main()