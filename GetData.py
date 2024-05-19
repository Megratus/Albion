import pip._vendor.requests
import json
from datetime import datetime

import mysql.connector
from mysql.connector import errorcode

# def get_request(url, params=None):
#     try:
#         response = pip._vendor.requests.get(url, params=params)
#         response.raise_for_status()  # Raise an HTTPError for bad responses
#         return response.json()  # Assuming the response is in JSON format
#     except pip._vendor.requests.exceptions.HTTPError as http_err:
#         print(f'HTTP error occurred: {http_err}')
#     except Exception as err:
#         print(f'Other error occurred: {err}')

# # Example usage
# url = 'https://europe.albion-online-data.com/api/v2/stats/history/T4_SKILLBOOK_GATHER_ORE.json?time-scale=24'
# params = {'key1': 'value1', 'key2': 'value2'}  # Optional parameters

# response_data = get_request(url, params)

# #parsed = json.loads(response_data)
# parsed = response_data

# if response_data:
#     print(json.dumps(parsed, indent=4))


# JSON data to be inserted (example)
# json_data = '''
# [
#     {"location": "Martlock", "timestamp":"2024-04-24T00:00:00", , "item_id": "T4_SKILLBOOK_GATHER_ORE", "item_count": 69, "avg_price":220}
    
# ]
# # '''

json_data = [
    {
        "location": "Brecilien",
        "item_id": "T4_SKILLBOOK_GATHER_HIDE",
        "quality": 1,
        "data": [
            {
                "item_count": 1,
                "avg_price": 18,
                "timestamp": "2024-04-27T00:00:00"
            },
            {
                "item_count": 13,
                "avg_price": 18,
                "timestamp": "2024-04-30T00:00:00"
            },
            # ... (rest of the data)
        ]
    },
    # ... (rest of the items)
]

json_data_test = [
    {
        "location": "Brecilien",
        "item_id": "T4_SKILLBOOK_GATHER_HIDE",
        "quality": 1,        
        "item_count": 1,
        "avg_price": 18,
        "timestamp": "2024-04-27T00:00:00"
    }
]


# Database connection details
db_config = {
    'user': 'root',
    'password': 'val094256',
    'host': 'localhost',
    'database': 'albion'
}

# Function to create a connection to the database
def create_db_connection(config):
    try:
        conn = mysql.connector.connect(**config)
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Incorrect username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: Database does not exist")
        else:
            print(err)

def insert_json_data_test(cursor, data):
    insert_query = """
    INSERT INTO historic_data (location, item_id, quality, item_count, avg_price, timestamp)
    VALUES ('test', '1', '69','testID', '2024-04-27T00:00:00')
    """

    values = ('test', '1', '69','testID', '2024-04-27T00:00:00')

    # for item in data:
    #     location = item["location"]
    #     item_id = item["item_id"]
    #     quality = item["quality"]
    #     item_count = item["item_count"]
    #     avg_price = item["avg_price"]
    #     timestamp = datetime.strptime(item["timestamp"], "%Y-%m-%dT%H:%M:%S")

def insert_json_data(cursor, data):
    insert_query = """
    INSERT INTO historic_data (location, item_id, quality, item_count, avg_price, timestamp)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    for item in data:
        location = item["location"]
        item_id = item["item_id"]
        quality = item["quality"]
        for entry in item["data"]:
            item_count = entry["item_count"]
            avg_price = entry["avg_price"]
            timestamp = datetime.strptime(entry["timestamp"], "%Y-%m-%dT%H:%M:%S")


def main():
    data = json_data
    data_test = json_data_test   

    # Create a database connection
    conn = create_db_connection(db_config)  
    if conn:
        cursor = conn.cursor()       
        
        # Insert JSON data
        insert_json_data(cursor, data)

        # Insert JSON data test
        insert_json_data_test(cursor, data_test)
        
        # Commit the transaction
        conn.commit()
        
        # Close the cursor and connection
        cursor.close()
        conn.close()
        print("Data inserted successfully")

# Execute main function
if __name__ == '__main__':
    main()