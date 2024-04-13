import pandas as pd
import time
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from matplotlib.ticker import MaxNLocator

def connect():
    db_url = 'postgresql+psycopg2://juan-gon:mysecretpassword@localhost:5432/piscineds'
    engine = create_engine(db_url)
    return engine

try:
    engine = connect()
except SQLAlchemyError as e:
    print(f"Error: {e}")

def clustering_and_segmentation(table: str):
    try:
        start_time = time.time()
        sql_command = f"""
            SELECT 
                user_id,
                MAX(event_time) AS last_purchase_date,
                SUM(price) AS total_spent,
                AVG(price) AS average_price
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
        current_date = pd.to_datetime('now')
        df['days_since_last_purchase'] = (current_date - df['last_purchase_date']).dt.days

        features = df[[ 'days_since_last_purchase','total_spent', 'average_price']]
        scaler = StandardScaler()
        df_scaled = scaler.fit_transform(features)

        # Aplicamos KMeans
        kmeans = KMeans(n_clusters=3, random_state=42)
        df['cluster_label'] = kmeans.fit_predict(df_scaled)

        cluster_labels = {
            0: 'Inactive',
            1: 'New Customers',
            2: 'Loyal Customers'
        }
        colors = [(245/255, 220/255, 183/255), (182/255, 197/255, 216/255), (115/255, 192/255, 167/255)]
        df['cluster_name'] = df['cluster_label'].apply(lambda x: cluster_labels[x])

        # Obtenemos el conteo de los clusters
        cluster_counts = df['cluster_name'].value_counts()

        # Gráfico de barras horizontal de los clusters
        plt.figure(figsize=(10, 6))
        bars = plt.barh(cluster_counts.index, cluster_counts.values, color=colors)
        plt.xlabel('Number of Customers')
        
        # Añadir etiquetas numéricas al final de cada barra
        for bar in bars:
            plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2,
                     f'{int(bar.get_width())}',
                     va='center', ha='left')

        plt.tight_layout()
        plt.savefig("test.png")
        plt.close()

        end_time = time.time()
        print(f"Elapsed time: {end_time - start_time:.2f} seconds")
    except Exception as e:
        print(f"Error: {e}")




def main():
    clustering_and_segmentation('customers')


if __name__ == '__main__':
    main()