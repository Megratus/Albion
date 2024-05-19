import mysql.connector
import json

# JSON data
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
INSERT INTO historic_data (location, item_id, quality, item_count, avg_price, timestamp)
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
        # Execute the insert query
        cursor.execute(insert_query, values)
    
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
