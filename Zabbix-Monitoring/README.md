# Zabbix Host Bulk Creation via Excel

This Python script automates the process of creating multiple hosts in Zabbix using its JSON-RPC API. Host information such as hostname, IP, group, SNMP version, and template are extracted from an Excel file (`input.xlsx`), making it easy to manage and provision monitoring targets in bulk.

## Prerequisites
Before running the script, make sure you have:
- [Python 3](https://www.python.org/downloads/) 
- Zabbix API access and a valid API key.
- Install required Python libraries:
  ```
  pip install pyserial netmiko paramiko scp
  ````
- A properly formatted Excel file (`input.xlsx`) with host details.
- Existing host groups and templates already created in Zabbix.

## Getting Started
To get started with this project, follow these steps:
1. Clone this repository to your local machine.
    ```
   git clone https://github.com/achilleaspappas/Code-Snippet-Collection.git
    ```
2. Input data to the excel file.
3. Run the script.

## How It Works
- **Reads Excel input** from `input.xlsx` containing host details:
   - Hostname
   - IP address
   - Host group
   - Template
   - SNMP version (2 or 3)
   - Proxy (currently unused)
- **Authenticates** to the Zabbix API using your provided `api_key`.
- **Fetches Group and Template IDs** from Zabbix via the API using the provided names.
- **Creates hosts** with the given configuration:
   - SNMPv2: uses community string
   - SNMPv3: uses username and password authentication
- **Logs results** to the console:
   - Success: displays created host ID
   - Failure: shows the error message from Zabbix

## Excel Input Format (`input.xlsx`)

| Hostname     | IP Address   | Group Name | Template Name       | SNMP Version | Proxy Name |
|--------------|--------------|------------|----------------------|--------------|-------------|
| switch-01    | 192.168.1.10 | Switches   | Template SNMPv2     | 2            | ZabbixProxy |
| firewall-01  | 192.168.1.1  | Firewalls  | Template SNMPv3     | 3            | ZabbixProxy |

> All fields are required for each row. Missing values will cause the script to skip that entry.

---

## Authors
[Achilleas Pappas] - Created the scripts

## License
This project is provided as-is for personal use and development.

## Acknowledgments
This project was developed as part of my work and experience.

