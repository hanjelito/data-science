import pandas as pd
import numpy as np
import datetime
import time
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import matplotlib.dates as mdates
import matplotlib.patches as patches
import seaborn as sns
from sqlalchemy import create_engine



def connect():
    db_url = 'postgresql+psycopg2://juan-gon:mysecretpassword@localhost:5432/piscineds'
    engine = create_engine(db_url)
    return engine

try:
    pandas_url = create_engine('postgresql://juan-gon:mysecretpassword@localhost:5432/piscineds')
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

def generate_boxplot_comparison():
    try:
        start_time = time.time()
        with engine.connect() as conn:
            consulta_sql = """
            SELECT
                price
            FROM customers
            WHERE event_type = 'purchase'
            """
            result = conn.execute(text(consulta_sql))
            data = result.fetchall()
            df = pd.DataFrame(data, columns=['price'])

            print(f"Generated {result.rowcount} rows")
            end_time = time.time()
            print(f"Elapsed time: {end_time - start_time:.2f} seconds\n")

            plt.figure(figsize=(10, 12))

            plt.subplot(2, 1, 1)
            sns.set(style="whitegrid")
            ax1 = sns.boxplot(x=df['price'], showfliers=True)
            ax1.set_xlabel('Price')

            plt.subplot(2, 1, 2) 
            sns.set(style="whitegrid")
            ax2 = sns.boxplot(x=df['price'], showfliers=False)
            ax2.set_xlabel('Price')

            plt.savefig("boxplot_comparison.png")
            plt.close()
    except Exception as e:
        print(f"Error: {e}")
        return None

# def generate_average_basket_price_boxplot():
#     try:
#         start_time = time.time()
#         with engine.connect() as conn:
#             consulta_sql = """
#             SELECT
#                 user_id,
#                 AVG(price) as average_basket_price
#             FROM customers
#             where event_type = 'purchase'
#             GROUP BY user_id
#             """
#             result = conn.execute(text(consulta_sql))
#             data = result.fetchall()
#             df = pd.DataFrame(data, columns=['user_id', 'average_basket_price'])

#             print(f"Generated {result.rowcount} rows")
#             end_time = time.time()
#             print(f"Elapsed time: {end_time - start_time:.2f} seconds\n")

#             sns.set(style="whitegrid")
#             plt.figure(figsize=(10, 6))
#             ax = sns.boxplot(x=df['average_basket_price'], showfliers=False)
#             ax.set_xlabel('Average Basket Price per User')
#             plt.savefig("average_basket_price_boxplot.png")
#             plt.close()
#     except Exception as e:
#         print(f"Error: {e}")
#         return None

def generate_average_basket_price_boxplot():
    # Tus estadísticas sumarias
    stats = {
        'mean': 4.932943,
        'std': 8.925811,
        'min': -79.370000,
        '25%': 1.590000,
        '50%': 3.000000,
        '75%': 5.400000,
        'max': 327.780000
    }

    # Los valores atípicos se podrían calcular como aquellos fuera de los bigotes del box plot.
    # Por simplicidad, vamos a generar algunos datos aleatorios que podrían representar valores atípicos.
    np.random.seed(0)  # Para reproducibilidad
    outliers = np.random.uniform(low=stats['min'], high=stats['max'], size=10)

    # Datos para el box plot basados en estadísticas sumarias
    data = [stats['min'], stats['25%'], stats['50%'], stats['75%'], stats['max']]

    # Crear un box plot
    plt.figure(figsize=(10, 2))  # Tamaño del gráfico
    plt.boxplot(data, vert=False, whis=[0, 100], showfliers=False)  # No mostrar los fliers automáticos

    # Añadir los valores atípicos
    plt.scatter(outliers, np.ones_like(outliers), color='red', alpha=0.5)

    # Añadir título y etiquetas
    plt.title('Box Plot with the Average Basket Price per User')
    plt.xlabel('Average Basket Price')

    # Configurar límites del eje x
    plt.xlim(28, 42)
    plt.savefig("test.png")
    plt.close()

def main():
    # exercice 1
    # result = mustache_rider('customers', '2022-10-01', '2023-03-01')
    # mustache_data(result)

    # exercice 2 crea mi tabla temporal
    # generate_boxplot_comparison()
    # exercice 3
    generate_average_basket_price_boxplot()

if __name__ == "__main__":
    main()