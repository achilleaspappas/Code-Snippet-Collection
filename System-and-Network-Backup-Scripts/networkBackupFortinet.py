import requests  # Import requests to handle HTTP requests
import json      # Import json to parse device configuration file
from datetime import datetime  # Import datetime to get the current date

# Get the current date and format it as "day_month_year"
now = datetime.now()
date = now.strftime("%d_%m_%Y")

# Load JSON file containing Fortinet device configurations
with open('/home/administrator/Documents/Scripts/networkBackupFortinet.json') as f:
    data_file = f.read()

# Parse JSON data to retrieve device details
data = json.loads(data_file)
devices = data["devices"]

# Iterate over each device in the configuration file
for device in devices:
    try:
        # Construct API URL for device backup, using IP and access token from the JSON file
        api_url = 'https://' + device["device_ip"] + '/api/v2/monitor/system/config/backup?scope=global&access_token=' + device["device_token"]

        # Define the path to save the configuration backup file with the current date
        path = '/path/to/destination/Fortinet/' + device["device_name"] + "_" + date

        # Disable SSL warnings for unverified HTTPS requests
        requests.packages.urllib3.disable_warnings()

        # Send a GET request to the device API to download the backup
        response = requests.get(api_url, verify=False)

        # Save the response (backup data) to a file
        with open(path, 'wb') as f:
            for line in response:
                f.write(line)
                
    except:
        # Print error message if the connection or request fails
        print("error")
