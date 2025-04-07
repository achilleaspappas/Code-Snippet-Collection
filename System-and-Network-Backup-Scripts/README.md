# Backup Scripts

This project automates various backup and maintenance tasks, including:
- Copying databases from the cloud to network storage.
- Backing up user files.
- Cleaning up folders.
- Performing regular backups of network devices.

All tasks are scheduled via a cron job, which runs every minute. The `main.sh` script handles scheduling within specific time windows.

## Prerequisites
  - [Python 3](https://www.python.org/downloads/) 
  - SMB/CIFS share access on your network for storing backup files
  - Logging paths correctly set up according to your environment

## Getting Started
To get started with this project, follow these steps:
1. Clone this repository to your local machine.
  ```
 git clone https://github.com/achilleaspappas/Code-Snippet-Collection.git
  ```
2. Setup cron job.

## How It Works
### main.sh
* **Location**: /home/administrator/Documents/Scripts/main.sh
* **Purpose**: Schedules and executes different backup operations based on the time of day and date. It calls separate scripts to handle specific operations.
* **Parameters**: None; it schedules tasks based on the system clock.
* **Scheduling**: This script is executed every minute using the following cron job ``` * * * * * /home/administrator/Documents/Scripts/main.sh ```
* **Tasks**:
  * Database Backup: Calls systemBackupDatabases.sh with flags (trn, day, night) to back up various databases.
  * User File Backup: Runs systemBackupFiles.sh to sync user files between two NAS systems.
  * Folder Cleanup: Invokes systemEmptyFolders.sh to clear recycle bin files.
  * Network Device Backup: Executes networkBackup.sh to back up FortiGate and Cisco device configurations.
* **Logging**: Logs is not happening in this step.

### systemBackupDatabases.sh
* **Location**: /home/administrator/Documents/Scripts/systemBackupDatabases.sh
* **Purpose**: Handles copying databases from cloud storage to the designated NAS backup directory. It’s called with flags (trn, day, night) to specify which databases to back up.
* **Parameters**:
  * ```$1``` - flag: Indicates the type of backup to perform (day, night, or trn), which determines which specific folders will be backed up.
  * ```$src```: Source directory path for each backup task, set within the script for various folders.
  * ```$dst```: Destination directory path for each backup task, set within the script for various folders.
  * ```$name```: A label for the backup task, used for logging.
  * ```$log```: Path to the log file for recording the backup operation details.
  * ```$fileExtention```: The file extension of backup files to find and copy (e.g., bak or trn).
  * ```$timeCopy```: Modification time filter for files to copy (e.g., -1 for files modified within the last day).
  * ```$timeDelete```: Modification time filter for files to delete from the destination (e.g., +2 to delete files older than 2 days).
* **Scheduling**: Invoked by main.sh at specific times based on the backup type, ensuring backups occur regularly throughout the day.
* **Tasks**:
  * Validates the existence of source and destination directories for each backup operation.
  * Copies new or modified files from the source to the destination directory based on the specified flag.
  * Deletes outdated backup files from the destination directory as needed.
  * Logs each backup operation’s status (Success, Failed, or Warning) and records details of the outcome.
* **Logging**: Logs each backup operation with start and end times, backup type, and result status.

### systemBackupFiles.sh
* **Location**: /home/administrator/Documents/Scripts/systemBackupFiles.sh
* **Purpose**: This script synchronizes specified directories from a NAS to a backup NAS location, ensuring that files are copied and updated while also removing obsolete files.
* **Parameters**:
  * ```$1``` - src: Source directory path.
  * ```$2``` - dst: Destination directory path.
  * ```$3``` - name: The name associated with each user for logging purposes.
  * ```$4``` - log: Path for the log file where the script records operation details.
* **Scheduling**: Executed by main.sh as part of the scheduled job to perform user filed synchronization at specified intervals.
* **Tasks**:
  * Defines source and destination directories for each user.
  * Checks if source and destination directories exist before attempting synchronization.
  * Uses rsync for synchronazation.
  * Writes each operation’s start and end time, user name, and status (Success or Failure) to a log file for tracking and troubleshooting.
* **Logging**: Logs each sync operation with start and end timestamps, user name, status, and a description indicating success or the reason for failure.

### systemEmptyFolders.sh
* **Location**: /home/administrator/Documents/Scripts/systemEmptyFolders.sh
* **Purpose**: Periodically cleans up specified directories by deleting all files within them.
* **Parameters**: none
* **Scheduling**: Executed by main.sh as part of the scheduled job to perform cleanup at specified intervals.
* **Tasks**:
  * Defines target directories for cleanup and iterates through each directory.
  * Deletes all files within each specified directory using rm -rf.
  * Logs the start and end times of each cleanup operation to provide a timestamped record of when each directory was cleared.
* **Logging**: Logs each cleanup operation with start and end times, along with the description of the directory being cleared.

### networkBackup.sh
* **Location**: /home/administrator/Documents/Scripts/systemBackupDatabases.sh
* **Purpose**:  This shell script initiates the backup process for Fortinet and Cisco network devices by executing the respective Python scripts. It verifies destination paths, manages logging, and removes outdated files as part of the backup maintenance routine.
* **Parameters**:
  * ```$src```: Path to the Python script to execute for the backup (e.g., networkBackupFortinet.py or networkBackupCisco.py).
  * ```$dst```: Destination directory path where backup files will be saved.
  * ```$name```: A label for the backup task, used for logging (e.g., "Fortinet" or "Cisco").
  * ```$log```: Path to the log file for recording the backup operation details.
  * ```$timeDelete```: Modification time filter for files to delete from the destination (set to delete files older than one day in this script).
* **Scheduling**: This script is executed by main.sh as part of a scheduled job, handling the timing and conditions for network device backups.
* **Tasks**:
  * Executes the specified Python script to connect to network devices and retrieve configuration data.
  * Checks if the specified destination folder (dst) exists; if not, it creates the directory.
  * Logs the start and end of each backup operation, including success or failure status, for each device.
  * Deletes any backup files in the destination folder that are older than 24 hours to manage storage space.
* **Logging**: Logs each device’s backup operation, recording start time, end time, device name, and operation status (Success or Failed) in a structured format within the log file (log).

### networkBackupCisco.py
* **Location**: /home/administrator/Documents/Scripts/networkBackupCisco.py
* **Purpose**: This Python script connects to each Cisco device, retrieves the running configuration, and saves it to the specified destination.
* **Parameters**: none
* **Scheduling**: This script is triggered by networkBackup.sh.
* **Tasks**:
  * Reads device data from networkBackupCisco.json.
  * Connects via SSH to each device and enters privileged mode.
  * Executes the show run command to retrieve the configuration.
  * Saves the output to a .txt file in the destination folder with the format <device_name>_<date>.txt.
* **Logging**: Logs each device connection attempt, configuration retrieval status, and file save operation, noting success or failure for each step.

### networkBackupCisco.json
* **Location**: /home/administrator/Documents/Scripts/networkBackupCisco.json
* **Purpose**: This JSON file contains the list of Cisco devices to be backed up, along with credentials and connection details required for each device.
* **Parameters**:
  * ```device_name```: Name identifier for each device.
  * ```device_type```: Specifies the device type (e.g., "cisco_ios").
  * ```ip```: Device IP address.
  * ```username```: SSH username for login.
  * ```password```: SSH password for login.
  * ```secret```: Privileged mode password.
* **Scheduling**: Not applicable; this file is read by networkBackupCisco.py during execution.
* **Tasks**:
  * Stores structured device information required for SSH connections.
  * Ensures each device’s credentials and IP address are accurately configured for access.
* **Logging**: No direct logging; this file’s contents are referenced by networkBackupCisco.py which logs connection statuses.

### networkBackupFortinet.py
* **Location**: /home/administrator/Documents/Scripts/networkBackupFortinet.py
* **Purpose**: This Python script connects to each Fortinet device, retrieves the configuration backup, and saves it to the specified network destination.
* **Parameters**: None
* **Scheduling**: This script is triggered by networkBackup.sh.
* **Tasks**:
  * Constructs an HTTPS URL to access the configuration backup endpoint using the device’s IP and API token.
  * Sends an HTTPS GET request to retrieve the backup configuration.
  * Saves the backup data to a network location as a .txt file using the format <device_name>_<date>.txt.
* **Logging**: Logs each HTTPS connection attempt, data retrieval status, and file save operation, noting success or failure for each step. 

### networkBackupFortinet.json
* **Location**: /home/administrator/Documents/Scripts/networkBackupFortinet.json
* **Purpose**: This JSON file contains the list of Fortinet devices to be backed up, with connection details and authentication tokens.
* **Parameters**:
  * ```device_name```: Name identifier for each device.
  * ```device_ip```: Device IP address.
  * ```device_token```: API token for authenticating HTTPS requests.
* **Scheduling**: Not applicable; this file is read by networkBackupFortinet.py during execution.
* **Tasks**:
  * Stores structured device information required for HTTPS connections.
  * Ensures each device’s IP and token are properly configured for access.
* **Logging**: No direct logging; this file’s contents are referenced by networkBackupFortinet.py, which logs connection and retrieval statuses.

## Authors
[Achilleas Pappas] - Created the scripts

## License
This project is provided as-is for personal use and development.

## Acknowledgments
This project was developed as part of my work and experience.