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
                   COUNT(DISTINCT user_id) AS unique_users,
                   COUNT(*) AS event_count,
                   SUM(price) AS total_price,
                   SUM(price) / NULLIF(COUNT(DISTINCT user_id), 0) AS average_spend
            FROM {table_name}
            WHERE event_time >= :start_date AND event_time < :end_date
            AND event_type = :event_type_filter
            and event_type = 'purchase'
            GROUP BY event_day
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
    # Initialize DataFrame with specific columns
    df = pd.DataFrame(data, columns=['event_day', 'event_count', 'total_price', 'unique_users', 'fifth_column'])
    
    # Filter columns and convert 'event_day' to datetime, then set as index
    df = df[['event_day', 'unique_users']]
    df['event_day'] = pd.to_datetime(df['event_day'])
    df.set_index('event_day', inplace=True)
    
    # Resampling data to daily frequency and plotting
    fig, ax = plt.subplots()
    df['unique_users'].resample('D').sum().plot(kind='line', color='blue', ax=ax)
    
    # Setting up date formatting and locator for the x-axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    
    # Labeling axes and adjusting layout
    ax.set_ylabel('Number of Customers')
    ax.set_xlabel('')  # No label needed as the date provides context
    plt.tight_layout()  # Adjust layout to fit everything neatly
    
    # Saving the figure and closing plot
    plt.savefig('number_of_customers.png')
    plt.close()
    
def generate_monthly_sales_chart(data):
    df = pd.DataFrame(data)
    df['event_day'] = pd.to_datetime(df['event_day'])
    df = df[['event_day', 'total_price']]
    
    # Convert event_day to datetime and extract month
    df['event_day'] = pd.to_datetime(df['event_day'])
    df['month'] = df['event_day'].dt.to_period('M')
    
    # Sum event counts by month and format month names
    monthly_data = df.groupby('month')['total_price'].sum().reset_index()
    monthly_data['month'] = monthly_data['month'].dt.strftime('%b')
    monthly_data['total_price'] = (monthly_data['total_price'] / 1e6)  # Scale to millions
    
    # Create a bar plot
    fig, ax = plt.subplots(figsize=(10, 7))
    monthly_data.plot(kind='bar', x='month', y='total_price', legend=False, color='skyblue', ax=ax)
    
    # Set custom formatting for the plot
    ax.set_xlabel('Month')
    ax.set_ylabel('Total Sales Millions of ₳')
    # ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, loc: "{:,.1f}".format(x)))
    ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: "{:,.2f}".format(x)))

    ax.set_xticklabels(monthly_data['month'], rotation=0)
    
    # Improve layout and save the figure
    fig.autofmt_xdate()
    plt.tight_layout(pad=2)
    plt.savefig('monthly_sales_chart.png')
    plt.close()

def generate_average_spend(data):
    df = pd.DataFrame(data)
    df['event_day'] = pd.to_datetime(df['event_day'])
    df = df[['event_day', 'average_spend']]
    
    fig, ax = plt.subplots(figsize=(10,7))
    df.plot(kind='area', x='event_day', y='average_spend', ax=ax, alpha=0.4, color='skyblue')
    df.plot(kind='line', x='event_day', y='average_spend', ax=ax, color='Slateblue', alpha=0.6)
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    
    date_range = pd.date_range(df['event_day'].min(), df['event_day'].max(), freq='MS')
    ax.set_xticks(date_range)
    
    fig.autofmt_xdate()
    plt.tight_layout(pad=2)

    ax.set_ylabel('Average spend/customers in ₳')
    ax.set_xlabel('')
    ax.legend().remove()

    plt.savefig('average_spend.png')
    plt.close()
    

def main():
    # create table
    create_query_date('customers', 'total_sales', '2022-10-01', '2023-03-01', 'purchase')
    result = query_total_sales('total_sales')
    generate_time_series_chart(result)
    generate_monthly_sales_chart(result)
    generate_average_spend(result)


 

if __name__ == "__main__":
    main()
  
  
  
#   WHERE event_time >= '2022-10-01' AND event_time < '2023-02-01'
