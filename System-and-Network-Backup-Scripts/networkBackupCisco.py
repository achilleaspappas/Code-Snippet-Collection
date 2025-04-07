from netmiko import ConnectHandler  # Import ConnectHandler for network device connection
from datetime import datetime       # Import datetime to get the current date
import json                         # Import json to parse device configuration file

# Get the current date and format it as "day_month_year"
now = datetime.now()
date = now.strftime("%d_%m_%Y")

# Load JSON file containing Cisco device configurations
with open('/home/administrator/Documents/Scripts/networkBackupCisco.json') as f:
    data_file = f.read()

# Parse JSON data to retrieve device details
data = json.loads(data_file)
devices = data["devices"]

# Iterate over each device in the configuration file
for device in devices:
    try:
        # Connect to the device using its properties from the JSON file
        net_connect = ConnectHandler(**device["properties"])
        net_connect.enable()  # Enter enable mode on the device

        # Send the command to retrieve the running configuration
        result = net_connect.send_command('show run')

        # Disconnect from the device after retrieving the configuration
        net_connect.disconnect()

        # Define the path to save the configuration backup file
        path = '/path/to/destination/Cisco/' + device["device_name"] + '_' + date + '.txt'

        # Save the retrieved configuration to a file
        with open(path, 'w') as f:
            for line in result:
                f.write(line)
                
    except:
        # Print error message if the connection or command fails
        print("error")
