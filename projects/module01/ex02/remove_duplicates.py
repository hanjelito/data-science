import pandas as pd
import datetime
import time
from sqlalchemy import create_engine, text

def connect():
    db_url = 'postgresql+psycopg2://juan-gon:mysecretpassword@localhost:5432/piscineds'
    engine = create_engine(db_url)
    return engine
engine = connect()

def count_total(table):
    with engine.connect() as conn:
        query = text(f"""
        SELECT COUNT(*)
        FROM {table}
        """)
        result = conn.execute(query)
        return result.scalar()
    
def create_new_table_day(table_name, start_datetime, end_datetime):
    start_time = time.time()

    with engine.connect() as conn:
        # Se debe definir el nombre de la tabla en el SQL directamente ya que los nombres de tabla no pueden ser parámetros
        sql_command = f"""
        CREATE TABLE IF NOT EXISTS {table_name} AS
        SELECT *
        FROM customers c
        WHERE c.event_time >= :start AND c.event_time <= :end
        """
        # Ejecuta la consulta pasando 'start' y 'end' como parámetros para evitar inyección SQL
        result = conn.execute(text(sql_command), {'start': start_datetime, 'end': end_datetime})
        conn.commit()  # Confirma los cambios en la base de datos

        print(f"Generated {result.rowcount} rows")  # Imprime la cantidad de filas generadas

    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time:.2f} seconds") 

def month_date(table_name, start_datetime, end_datetime):
    print(f"Creando tabla para {table_name} desde {start_datetime} hasta {end_datetime}")
    # create_new_table_day("customers", "2022-10-01 00:00:00", "2022-10-01 23:59:59")
    create_new_table_day(table_name, start_datetime, end_datetime)
    # Aquí iría la lógica para crear la tabla

def main():
    # Define el rango de fechas
    fecha_inicio = datetime.datetime(2022, 10, 1)
    fecha_fin = datetime.datetime(2022, 11, 30)

    # Itera sobre cada mes en el rango
    mes_actual = fecha_inicio
    cont = 0
    while mes_actual <= fecha_fin:
        inicio_mes = mes_actual

        año_siguiente = inicio_mes.year + (inicio_mes.month // 12)
        mes_siguiente = inicio_mes.month % 12 + 1
        fin_mes = datetime.datetime(año_siguiente, mes_siguiente, 1) - datetime.timedelta(seconds=1)

        
        inicio_str = inicio_mes.strftime("%Y-%m-%d %H:%M:%S")
        fin_str = fin_mes.strftime("%Y-%m-%d %H:%M:%S")
        
        month_date(f'customers{cont}', inicio_str, fin_str)
        cont += 1

        
        mes_actual = fin_mes + datetime.timedelta(seconds=1)


if __name__ == "__main__":
    main()