import pip._vendor.requests
import datetime

import mysql.connector
import json

def get_request(item):
    
    url = 'https://europe.albion-online-data.com/api/v2/stats/prices/%s.json?locations=Thetford, Fort Sterling, Lymhurst, Matlock, Bridgewatch, Caerleon&qualities=0' %(item)
    params = {'key1': 'value1', 'key2': 'value2'}  # Optional parameters
    
    try:
        response = pip._vendor.requests.get(url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()  # Assuming the response is in JSON format
    except pip._vendor.requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

items_config = ('T4_SKILLBOOK_GATHER_HIDE', 'T4_SKILLBOOK_GATHER_ORE', 'T6_MAIN_RAPIER_MORGANA@2','T4_ARMOR_LEATHER_HELL@2','T4_LEATHER_LEVEL2@2')

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
    
    print(f"Data inserted successfully.")
except mysql.connector.Error as err:
    # Rollback in case of an error
    db.rollback()
    print(f"Error: {err}")
finally:
    # Close the cursor and connection
    cursor.close()
    db.close()
