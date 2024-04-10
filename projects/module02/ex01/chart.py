import pandas as pd
import datetime
import time
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib.dates as mdates


def connect():
    db_url = 'postgresql+psycopg2://juan-gon:mysecretpassword@localhost:5432/piscineds'
    engine = create_engine(db_url)
    return engine

try:
	engine = connect()
except SQLAlchemyError as e:
	print(f"Error: {e}")
    

def create_query_date(table_name: str, new_table: str, start_date: str, end_date: str, event_type_filter: str) -> None:
    try:
        start_time = time.time()
        with engine.connect() as conn:
            sql_command = f"""
            DROP TABLE IF EXISTS {new_table};
            CREATE TABLE {new_table} AS
            SELECT DATE(event_time) AS event_day,
                   SUM(price) AS total_price,
                   COUNT(*) AS event_count,
                   COUNT(DISTINCT user_id) AS unique_users
            FROM {table_name}
            WHERE event_time >= :start_date AND event_time < :end_date
            AND event_type = :event_type_filter
            GROUP BY event_day;
            """
            result = conn.execute(text(sql_command), {'start_date': start_date, 'end_date': end_date, 'event_type_filter': event_type_filter})
            conn.commit()
            print(f"Generated {result.rowcount} rows")
        
        end_time = time.time()
        print(f"Elapsed time: {end_time - start_time:.2f} seconds")
    
    except Exception as e:
        print(f"Error: {e}")

def query_total_sales(table_name:str)-> any:
    try:
        with engine.connect() as conn:
            sql_command = text(f"""
            SELECT * 
            FROM {table_name}
            """)
            result = conn.execute(sql_command)
            return result.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        return None

def generate_time_series_chart(data):
    df = pd.DataFrame(data, columns=['event_day', 'event_count', 'total_price', 'unique_users'])
    df = df[['event_day', 'unique_users']]
    df['event_day'] = pd.to_datetime(df['event_day'])
    df.set_index('event_day', inplace=True)

    df['unique_users'].resample('D').sum().plot(kind='line', color='blue')

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())

    plt.ylabel('Number of costumers')
    plt.xlabel('')
    plt.tight_layout()
    plt.savefig('number_of_costumers.png')
    plt.close()
    
def generate_monthly_sales_chart(data):
    df = pd.DataFrame(data, columns=['event_day', 'event_count', 'total_price', 'unique_users'])
    
    df.drop(columns=['unique_users'], inplace=True)

    df['event_day'] = pd.to_datetime(df['event_day'])
    df['month'] = df['event_day'].dt.to_period('M')
    monthly_data = df.groupby('month')['event_count'].sum().reset_index()
    monthly_data['month'] = monthly_data['month'].dt.strftime('%b')

    monthly_data['event_count'] = monthly_data['event_count'] / 1e6

    ax = monthly_data.plot(kind='bar', x='month', y='event_count', legend=False, color='skyblue')
    ax.set_xlabel('Month')
    ax.set_ylabel('Total Sales Millions of ₳')

    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, loc: "{:,.1f}".format(x)))
    ax.set_xticklabels(monthly_data['month'], rotation=0)
    
    plt.tight_layout()
    plt.savefig('monthly_sales_chart.png')
    plt.close()



def main():
    # create table
    # create_query_date('customers', 'total_sales', '2022-10-01', '2023-03-01', 'purchase')
    result = query_total_sales('total_sales')
    generate_time_series_chart(result)
    generate_monthly_sales_chart(result)
 

if __name__ == "__main__":
    main()
  
  
  
#   WHERE event_time >= '2022-10-01' AND event_time < '2023-02-01'
