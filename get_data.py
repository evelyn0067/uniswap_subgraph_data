import pandas as pd
import requests
from datetime import datetime, timedelta
# Get the current timestamp
current_time = datetime.now()
# Compute the timestamp for 24 hours ago
past_24_hours = current_time - timedelta(hours=24)
current_time_seconds = int(current_time.timestamp())
past_24_hours_seconds = int(past_24_hours.timestamp())
print(str(past_24_hours_seconds))
url = 'https://api.thegraph.com/subgraphs/name/ianlapham/uniswap-v2-dev'

# Initialize an empty list to store the queried data
all_pairs = []

# Set the initial value for the 'createdAtTimestamp_gt' parameter
timestamp_lt = str(current_time_seconds)  # Initial timestamp value


# Loop to query all data
while True:
    # GraphQL query
    query = """
    {
      pairs(
        first: 1000
        orderDirection: desc
        orderBy: createdAtTimestamp
        where: { createdAtTimestamp_lt: "%s" }
      ) {
        createdAtTimestamp
        id
        token0Price
        token1Price
        token0 {
          name
          symbol
        }
        token1 {
          name
          symbol
        }
      }
    }
    """ % timestamp_lt

    # Send the request
    response = requests.post(url, json={"query": query})

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()["data"]
        pairs = data["pairs"]
        
        # If no more pairs are returned, break the loop
        if int(pairs[-1]["createdAtTimestamp"]) < past_24_hours_seconds:
            print('end')
            break
        
        # Update the timestamp_gt value for the next iteration
        timestamp_lt = pairs[-1]["createdAtTimestamp"]
        print(timestamp_lt)
        
        # Append the queried pairs to the all_pairs list
        all_pairs.extend(pairs)
        
    else:
        print("Error:", response.status_code)

# Display the queried data
print(past_24_hours_seconds,timestamp_lt)
print(pairs)
for pair in all_pairs:
    print(pair)
df = pd.DataFrame(pairs)
df['createdAtTimestamp'] = pd.to_datetime(df['createdAtTimestamp'], unit='s')
