# Huawei Switch Initial Configuration

This script automates the initial configuration and stack setup of Huawei S5735-L switches.

## Prerequisites
  - [Python 3](https://www.python.org/downloads/) 
  - Install required Python libraries:
    ```
    pip install pyserial netmiko paramiko scp
    ```
  - Connect the switch serial port to computer's USB port.
  - Connect the ethernet cable from switch's port 1 to the computer's NIC.
  - Set static IP address to computer's NIC 172.16.0.2/24

## Getting Started
To get started with this project, follow these steps:
1. Clone this repository to your local machine.
    ```
   git clone https://github.com/achilleaspappas/Code-Snippet-Collection.git
    ```
2. Run the networkGenerateConfigHuawei.py to generate the configurations and define stack members.
3. Run networkPushConfigHuawei.py to configure the switch.

## Files and Structure
```
Huawei/
└── Switch_Initial_Config/
    ├── config_stack_status.txt
    ├── config_current_template.txt
    ├── Configurations/
    │   └── <ESN>.txt
    ├── S5735-L_V200R022C00SPC500.cc
    └── S5735-L-V200R022SPH150.pat
```
- `config_stack_status.txt`: Contains ESNs and their stack roles (e.g., `<ESN>:0` for master, `<ESN>:1` for member).
- `config_current_template.txt`: Contains the template configuration.
- `Configurations`: Folder with configuration files named after the ESNs of the switches.
- `.cc`: Software image file.
- `.pat`: Patch file.

## How It Works
### networkGenerateConfigHuawei.py
  - Loads device information from networkDevicesHuawei.json, which includes system name, IP addresses, subnet mask, gateway, SNMP location, and serial numbers.
  - Loads a configuration template from config_current_template.txt containing placeholders (e.g., {{sysname}}, {{managementIP}}, etc.).
  - For each switch:
    - Replaces placeholders in the template with actual values from the JSON file.
    - Generates two configuration files—one for each ESN (slot0 and slot1).
    - Saves each configuration file in the Configurations/ folder, named as <ESN>.txt.
    - Updates the config_stack_status.txt file with entries in the format <ESN>:0 or <ESN>:1, which is used later by the stack configuration logic.
### networkPushConfigHuawei.py
  - The script connects via serial and performs initial config (password change, VLAN and SSH setup).
  - It connects via SSH and retrieves the ESN.
  - Based on the ESN, it sets the switch’s stack status using config_stack_status.txt.
  - It transfers:
    - Software image (.cc)
    - Patch file (.pat)
    - Configuration file for the switch
  - Sets the transferred files to boot at next startup.
  - Reboots the switch.

## Authors
[Achilleas Pappas] - Created the scripts

## License
This project is provided as-is for personal use and development.

## Acknowledgments
This project was developed as part of my work and experience.
