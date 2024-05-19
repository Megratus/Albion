import pip._vendor.requests
import json

import mysql.connector
from mysql.connector import errorcode

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
url = 'https://europe.albion-online-data.com/api/v2/stats/history/T4_SKILLBOOK_GATHER_ORE.json?time-scale=24'
params = {'key1': 'value1', 'key2': 'value2'}  # Optional parameters

response_data = get_request(url, params)

#parsed = json.loads(response_data)
parsed = response_data

if response_data:
    print(json.dumps(parsed, indent=4))

