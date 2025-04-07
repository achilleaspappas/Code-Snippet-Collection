import json
import os

# Initialize varibles
currentFolder = "Huawei\Switch_Initial_Config"
#os.makedirs(currentFolder, exist_ok=True)
jsonFile = os.path.join(currentFolder, "networkDevicesHuawei.json")
configTemplate = os.path.join(currentFolder, "config_current_template.txt")

# Load JSON data from the file
with open(jsonFile, "r") as f:
    data = json.load(f)
f.close()

# Load template for the configuration file
with open(configTemplate, "r") as f:
    template = f.read()
f.close()

# Loop through each device and generate the configuration
for device in data["devices"]:
    # Replace placeholders in the template with device-specific values
    config = template.replace("{{sysname}}", device["sysname"])
    config = config.replace("{{managementIP}}", device["managementIP"])
    config = config.replace("{{subnetMask}}", device["subnetMask"])
    config = config.replace("{{gatewayIP}}", device["gatewayIP"])
    config = config.replace("{{locationSNMP}}", device["locationSNMP"])
    
    # Generate configuration files for each serial number
    for slot in ["slot0ESN", "slot1ESN"]:
        serial_number = device[slot] # Get ESN from json file
        configurationsFolder = os.path.join(currentFolder, "Configurations")
        output_file = os.path.join(configurationsFolder, f"{serial_number}.txt") # Create file named ESN to write the config
        with open(output_file, "w") as f: # Save the configuration to the file
            f.write(config)
        f.close()
        stackStatusFile = os.path.join(currentFolder, "config_stack_status.txt") # Find stack_status file
        with open(stackStatusFile, "a") as f: # Append record
            if "0" in slot:
                f.write(serial_number + ":0\n")
            elif "1" in slot:
                f.write(serial_number + ":1\n")
        f.close()
        print(f"Generated configuration for {serial_number} at {output_file}")

print("All configuration files have been generated!")
