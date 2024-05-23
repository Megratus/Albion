import pip._vendor.requests
import datetime

import mysql.connector
import json

from collections import defaultdict

import matplotlib.pyplot as plt

import time
import threading


def get_request(item):
    
    url = 'https://europe.albion-online-data.com/api/v2/stats/prices/%s.json?locations=Thetford, Fort Sterling, Lymhurst, Martlock, Bridgewatch, Caerleon&qualities=0' %(item)
    params = {'key1': 'value1', 'key2': 'value2'}  # Optional parameters
    
    try:
        response = pip._vendor.requests.get(url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()  # Assuming the response is in JSON format
    except pip._vendor.requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

#items_config = ('QUESTITEM_TOKEN_ROYAL_T5','T5_FARM_COUGAR_BABY','T4_FIBER_LEVEL2@2','T4_FIBER_LEVEL1@1','T5_FARM_CABBAGE_SEED','T5_FARM_GOOSE_BABY','T5_FARM_GOOSE_GROWN','T4_SKILLBOOK_GATHER_HIDE', 'T4_SKILLBOOK_GATHER_ORE', 'T6_MAIN_RAPIER_MORGANA@2','T4_ARMOR_LEATHER_HELL@2','T4_LEATHER_LEVEL2@2', 'T4_ARTEFACT_ARMOR_LEATHER_HELL')

# Read contents of the file
with open('items_config.txt', 'r') as file:
    file_contents = file.read()

# Split the content into individual items
items_config_list = file_contents.split(',')

# Remove leading and trailing whitespace from each item
items_config_list = [item.strip() for item in items_config_list]

# Convert the list to a tuple
items_config = tuple(items_config_list)

def main():

    updated_date = datetime.datetime.now().replace(microsecond=0).isoformat()
    json_data = []

    for item in items_config:
        data = get_request(item)
        if data:
            json_data += data

    # Database connection
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="val094256",
        database="albion"
    )

    cursor = db.cursor()

    # Insert query
    insert_query = """
    INSERT IGNORE INTO current_data (
        item_id, city, quality, sell_price_min, sell_price_min_date, 
        sell_price_max, sell_price_max_date, buy_price_min, buy_price_min_date, 
        buy_price_max, buy_price_max_date, updated_date
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    try:
        # List to hold all the values to be inserted
        all_values = []
        
        # Extract values from JSON data
        for item in json_data:
            
            if item["sell_price_min"] == 0 and item["sell_price_max"] == 0 and item["buy_price_max"] == 0 :
                    continue
            
            values = (
                item["item_id"],
                item["city"],
                item["quality"],
                item["sell_price_min"],
                item["sell_price_min_date"],
                item["sell_price_max"],
                item["sell_price_max_date"],
                item["buy_price_min"],
                item["buy_price_min_date"],
                item["buy_price_max"],
                item["buy_price_max_date"],
                updated_date
            )
            all_values.append(values)
        
        # Execute the insert query with IGNORE for each record
        cursor.executemany(insert_query, all_values)        
        
        # Commit the transaction
        db.commit()
        
        print(f"Data inserted successfully at: ", updated_date)
        
    except mysql.connector.Error as err:
        # Rollback in case of an error
        db.rollback()
        print(f"Error: {err}")
    finally:
        # Close the cursor and connection
        cursor.close()
        db.close()

main()

# #Define a flag to control the stopping of the loop
# stop_event = threading.Event()

# def my_function():
#     main()
#     print("Function is running")

# def run_periodically(interval, func, stop_event):
#     while not stop_event.is_set():
#         func()
#         time.sleep(interval)

# # Function to start the periodic function
# def start_periodic_function():
#     # Set the interval to 30 minutes (1800 seconds)
#     interval = 3600  # seconds
#     thread = threading.Thread(target=run_periodically, args=(interval, my_function, stop_event))
#     thread.start()
#     return thread

# # Function to stop the periodic function
# def stop_periodic_function():
#     stop_event.set()

# # Example usage:
# # Start the function
# thread = start_periodic_function()

# The function will run every 60 minutes until you call stop_periodic_function()
# To stop it:
# stop_periodic_function()