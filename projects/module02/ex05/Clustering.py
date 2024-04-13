import pandas as pd
import time
import matplotlib.pyplot as plt
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

def clustering_and_segmentation(table: str):
    """
    Clustering and segmentation of customers based on their purchase history.
    """
    try:
        start_time = time.time()

        sql_command = f"""
            SELECT 
                user_id,
                MAX(event_time) AS last_purchase_date,
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
        current_date = df['last_purchase_date'].max()
        df['days_since_last_purchase'] = (current_date - df['last_purchase_date']).dt.days

        features = df[['days_since_last_purchase', 'average_price']]
        scaler = StandardScaler()
        df_scaled = scaler.fit_transform(features)

        kmeans = KMeans(n_clusters=3, random_state=42)
        df['cluster_label'] = kmeans.fit_predict(df_scaled)

        cluster_labels = {
            0: 'Inactive',
            1: 'New Customers',
            2: 'Loyal Customers'
        }
        df['cluster_name'] = df['cluster_label'].apply(lambda x: cluster_labels[x])

        # Definir colores específicos para cada cluster
        colors = ['lightblue', 'lightgreen', 'salmon']

        # Mapa de colores basado en las etiquetas
        color_map = {label: color for label, color in zip(cluster_labels.values(), colors)}

        # Gráfico de barras
        plt.figure(figsize=(10, 6))
        cluster_counts = df['cluster_name'].value_counts().reindex(cluster_labels.values(), fill_value=0)
        bars = plt.barh(cluster_counts.index, cluster_counts.values, color=[color_map[name] for name in cluster_counts.index])
        plt.xlabel('Number of Customers')

        # Añadir etiquetas numéricas
        for bar in bars:
            plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2,
                     f'{int(bar.get_width())}',
                     va='center', ha='left')

        plt.tight_layout()
        plt.savefig("customers_active.png")
        plt.show()
        plt.close()

        # Gráfico de dispersión
        centroids = scaler.inverse_transform(kmeans.cluster_centers_)
        plt.figure(figsize=(10, 6))
        scatter = plt.scatter(df['average_price'], df['days_since_last_purchase'], 
                              c=[color_map[name] for name in df['cluster_name']], alpha=0.6, edgecolor='k', s=50)

        plt.scatter(centroids[:, 1], centroids[:, 0], c='yellow', s=200, marker='o')
        plt.title('Customer Clusters')
        plt.xlabel('Total Spent')
        plt.ylabel('Days Since Last Purchase')
        plt.tight_layout()
        plt.savefig("consumers_clusters.png")
        plt.show()
        plt.close()

        end_time = time.time()
        print(f"Elapsed time: {end_time - start_time:.2f} seconds")
    except Exception as e:
        print(f"Error: {e}")


def main():
    clustering_and_segmentation('customers')
    # clustering_and_segmentation2('customers')


if __name__ == '__main__':
    main()