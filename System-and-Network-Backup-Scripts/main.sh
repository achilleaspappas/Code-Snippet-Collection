#!/bin/bash

# Backup databases at the 30th minute of every hour
if [ $(date +%M) == "30" ]; then
    /home/administrator/Documents/Scripts/systemBackupDatabases.sh "trn"
fi

# Backup user files daily at 06:00 AM
if [ $(date +%H:%M) == "06:00" ]; then
    /home/administrator/Documents/Scripts/systemBackupFiles.sh
fi

# Empty specific folders daily at 07:30 AM
if [ $(date +%H:%M) == "07:30" ]; then
    /home/administrator/Documents/Scripts/systemEmptyFolders.sh
fi

# Perform a full database backup daily at 07:35 AM
if [ $(date +%H:%M) == "07:35" ]; then
    /home/administrator/Documents/Scripts/systemBackupDatabases.sh "day"
fi

# Perform a nightly database backup daily at 05:00 PM
if [ $(date +%H:%M) == "17:00" ]; then
    /home/administrator/Documents/Scripts/systemBackupDatabases.sh "night"
fi

# Backup FortiGate and Cisco device configurations on the 5th, 15th, and 25th of each month at 10:00 AM
if ([ $(date +%d) == "5" ] || [ $(date +%d) == "15" ] || [ $(date +%d) == "25" ]) && [ $(date +%H:%M) == "10:00" ]; then
    /home/administrator/Documents/Scripts/networkBackup.sh
fi
