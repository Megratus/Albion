import pip._vendor.requests

import mysql.connector
import json

def get_request(url, params=None):
    try:
        response = pip._vendor.requests.get(url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()  # Assuming the response is in JSON format
    except pip._vendor.requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

# Example usage
url = 'https://europe.albion-online-data.com/api/v2/stats/history/T4_SKILLBOOK_GATHER_HIDE?time-scale=24'
params = {'key1': 'value1', 'key2': 'value2'}  # Optional parameters

json_data = get_request(url, params)


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
INSERT IGNORE INTO historic_data (location, item_id, quality, item_count, avg_price, timestamp)
VALUES (%s, %s, %s, %s, %s, %s)
"""

try:
    for item in json_data:
        location = item['location']
        item_id = item['item_id']
        quality = item['quality']
        
        for record in item['data']:
            values = (
                location,
                item_id,
                quality,
                record['item_count'],
                record['avg_price'],
                record['timestamp']
            )
            cursor.execute(insert_query, values)
        # Execute the insert query
        print(values)
        #cursor.execute(insert_query, values)
    
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
