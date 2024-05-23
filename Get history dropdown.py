import mysql.connector
from mysql.connector import Error
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from matplotlib.ticker import FuncFormatter
from ipywidgets import interact, Dropdown

try:
    # Establish a database connection
    db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="val094256",
    database="albion"
)

    if db.is_connected():
        print("Connected to MySQL database")

        # Create a cursor object
        cursor = db.cursor()

        # Define the query
        query = """
        SELECT 
            item_id, city, quality, sell_price_min, sell_price_min_date, 
            sell_price_max, sell_price_max_date, buy_price_min, buy_price_min_date, 
            buy_price_max, buy_price_max_date, updated_date 
        FROM 
            current_data

        where item_id = 'T4_SKILLBOOK_GATHER_HIDE' or item_id = 'T4_SKILLBOOK_GATHER_ORE'
        and city != 'Caerleon' AND city != '0'
            
        """

        # Execute the query
        cursor.execute(query)

        # Fetch all rows from the executed query
        result = cursor.fetchall()

        # Convert the result to a pandas DataFrame
        df = pd.DataFrame(result, columns=[
            'item_id', 'city', 'quality', 'sell_price_min', 'sell_price_min_date', 
            'sell_price_max', 'sell_price_max_date', 'buy_price_min', 'buy_price_min_date', 
            'buy_price_max', 'buy_price_max_date', 'updated_date'
        ])

        def thousands_separator(x, pos):
            return '{:,.0f}'.format(x)
        
        # Convert date columns to datetime with error handling
        df['sell_price_min_date'] = pd.to_datetime(df['sell_price_min_date'], errors='coerce')

        # Filter out values above the upper limit
        #upper_limit = 200000
        #df = df[df['sell_price_min'] <= upper_limit]

        # Plot data for each item_id
        item_ids = df['item_id'].unique()
        for item_id in item_ids:
            item_data = df[df['item_id'] == item_id]
            cities = item_data['city'].unique()
            plt.figure(figsize=(10, 5))

            for city in cities:
                city_data = item_data[item_data['city'] == city]
                if city == 'Thetford':
                    color = 'purple'
                elif city == 'Fort Sterling':
                    color = 'lightblue'
                elif city == 'Lymhurst':
                    color = 'green'
                elif city == 'Bridgewatch':
                    color = 'orange'
                elif city == 'Martlock':
                    color = 'blue'
                elif city == 'Caerleon':
                    color = 'red'
                else:
                    color = 'black'  # default color
                plt.plot(city_data['sell_price_min_date'], city_data['sell_price_min'], label=city, marker='o', color=color)


            plt.xlabel('Date (DD-MM HH)')
            plt.ylabel('Sell Price Min')
            plt.title(f'Sell Price Min Trends for Item ID: {item_id}')
            plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m %H'))
            plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
            plt.gca().yaxis.set_major_formatter(FuncFormatter(thousands_separator))  # Format y-axis label with thousands separator
            plt.gcf().autofmt_xdate()  # Rotation of x-axis labels for better readability

            plt.grid(True)
            plt.show()

except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    if db.is_connected():
        cursor.close()
        db.close()
        print("MySQL connection is closed")

# Get unique item ids
unique_item_ids = df['item_id'].unique()

# Create dropdown menu
dropdown = Dropdown(options=unique_item_ids, description='Item ID:')

# Define function to update plot when dropdown value changes
def update_plot(item_id):
    query_data(item_id)

# Register function to be called when dropdown value changes
interact(update_plot, item_id=dropdown)