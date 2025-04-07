#!/bin/bash

# Define a function to sync directories with logging
func() {
    local src=$1      # Source directory
    local dst=$2      # Destination directory
    local name=$3     # Name identifier for the sync task
    local log=$4      # Log file path for recording sync status
    local status="Success"     # Default sync status
    local description="OK"     # Default sync description
    local startTime=$(date +"%Y-%m-%d %H:%M") # Record start time

    # Check if the source folder exists
    if [ ! -d "$src" ]; then
        status="Failed"        # Mark as failed if source is missing
        description="Source Not Found"
    fi

    # Check if the destination folder exists
    if [ ! -d "$dst" ]; then
        status="Failed"        # Mark as failed if destination is missing
        description="Destination Not Found"
    fi

    # If both source and destination are valid, proceed with the sync
    if [ "$status" == "Success" ]; then
        # Use rsync to synchronize folders, excluding certain directories
        rsync -rv --update --delete --exclude "@Recycle" --exclude "System Volume Information" "$src" "$dst" >> $log
    fi

    local endTime=$(date +"%Y-%m-%d %H:%M") # Record end time
    # Log the sync process, including start and end time, status, and description
    echo "$startTime | $endTime | $name | Status: $status | Desc: $description" >> $log
    
    return
}

# Define paths for log file, source, and destination base directories
log="/path/to/log/Sync-"$(date +%Y_%m_%d)".log"
src="/path/to/source/"
dst="/path/to/destination/"

# Define source and destination paths for each user directory
src_user1="$src""user1"
src_user2="$src""user2"
src_user3="$src""user3"
src_user4="$src""user4"
src_user5="$src""user5"
src_user6="$src""user6"
src_user7="$src""user7"
src_user8="$src""user8"
src_user9="$src""user9"
src_user10="$src""user10"
src_user11="$src""user11"

dst_user1="$dst""user1"
dst_user2="$dst""user2"
dst_user3="$dst""user3"
dst_user4="$dst""user4"
dst_user5="$dst""user5"
dst_user6="$dst""user6"
dst_user7="$dst""user7"
dst_user8="$dst""user8"
dst_user9="$dst""user9"
dst_user10="$dst""user10"
dst_user11="$dst""user11"

# Call the sync function for each user directory
# Each sync logs its status to the shared log file
func "$src_user1/" "$dst_user1/" "user1" "$log"
func "$src_user2/" "$dst_user2/" "user2" "$log"
func "$src_user3/" "$dst_user3/" "user3" "$log"
func "$src_user4/" "$dst_user4/" "user4" "$log"
func "$src_user5/" "$dst_user5/" "user5" "$log"
func "$src_user6/" "$dst_user6/" "user6" "$log"
func "$src_user7/" "$dst_user7/" "user7" "$log"
func "$src_user8/" "$dst_user8/" "user8" "$log"
func "$src_user9/" "$dst_user9/" "user9" "$log"
func "$src_user10/" "$dst_user10/" "user10" "$log"
func "$src_user11/" "$dst_user11/" "user11" "$log"
