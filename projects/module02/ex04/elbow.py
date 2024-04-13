import pandas as pd
import time
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def connect():
    db_url = 'postgresql+psycopg2://juan-gon:mysecretpassword@localhost:5432/piscineds'
    engine = create_engine(db_url)
    return engine

try:
    engine = connect()
except SQLAlchemyError as e:
    print(f"Error: {e}")


def thousands_formatter(x, pos):
    return f'{int(x)}'

def method_elbow(table: str) -> None:
    """
    Método del codo para determinar el número óptimo de clusters.
    suma de las distancias al cuadrado de cada punto al centroide de su cluster
    """
    try:
        start_time = time.time()

        sql_command = f"""
            SELECT 
                user_id,
                MAX(event_time) AS last_purchase_date,
                SUM(price) AS total_spent
            FROM 
                {table}
            WHERE
                event_type = 'purchase'
            GROUP BY 
                user_id;
        """
        with engine.connect() as conn:
            df = pd.read_sql(sql_command, conn)

        df['last_purchase_date'] = pd.to_datetime(df['last_purchase_date'])
        current_date = df['last_purchase_date'].max()
        df['days_since_last_purchase'] = (current_date - df['last_purchase_date']).dt.days

        # Escalado de datos
        scaler = StandardScaler()
        df_scaled = scaler.fit_transform(df[['total_spent', 'days_since_last_purchase']])

        k_values = range(1, 11)
        inertias = []
        #random_state semilla para la inicialización de los centroides
        for k in k_values:
            kmeans = KMeans(n_clusters=k, random_state=0)
            kmeans.fit(df_scaled)
            inertias.append(kmeans.inertia_)

        formatter = FuncFormatter(thousands_formatter)
        plt.figure(figsize=(10, 7))
        plt.plot(k_values, inertias, '-o')
        plt.gca().yaxis.set_major_formatter(formatter)
        plt.xlabel('Number of clusters')
        plt.title('Elbow Method')
        plt.tight_layout()
        plt.savefig("method_elbow.png")
        plt.close()

        
    except Exception as e:
        print(f"Error: {e}")


def main():
    method_elbow('customers')

if __name__ == '__main__':
    main()