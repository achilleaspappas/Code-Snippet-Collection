#!/bin/bash

# Accepts a flag parameter to determine which databases to back up
flag=$1

# Function to handle the backup process for each database
func() {
    local src=$1            # Source directory for backup files
    local dst=$2            # Destination directory for backup files
    local name=$3           # Name identifier for logging
    local log=$4            # Log file path
    local fileExtention=$5  # File extension of the backup files
    local timeCopy=$6       # File age condition for copying (mtime filter)
    local timeDelete=$7     # File age condition for deletion (mtime filter)
    local status="Success"  # Initial status
    local description="OK"  # Initial description
    local startTime=$(date +"%Y-%m-%d %H:%M")  # Start time of the backup operation
    
    # Check if the source folder exists; update status if not
    if [ ! -d "$src" ]; then
        status="Failed"
        description="Source Not Found"
    fi

    # Check if the destination folder exists; update status if not
    if [ ! -d "$dst" ]; then
        status="Failed"
        description="Destination Not Found"
    fi

    # If both source and destination directories exist, proceed with backup
    if [ "$status" == "Success" ]; then
        # Check for new backup files in the source directory
        local newBackup=$(find "$src" -name "*.$fileExtention" -type f -mtime "$timeCopy" | wc -l)
        
        # If no new backups are found, update status and description
        if [ "$newBackup" -eq "0" ]; then
            status="Warning"
            description="New Backup Not Found"
        else
            # Copy new backup files to the destination directory
            find "$src" -name "*.$fileExtention" -mtime "$timeCopy" -exec cp --update=none {} "$dst" \;
            # Delete old backup files from the destination directory
            find "$dst" -type f -name "*.$fileExtention" -mtime "$timeDelete" -exec rm -r {} \;
        fi
    fi

    # Calculate the size of the most recent files for logging purposes
    local sizeHeadOne=$(ls "$dst" -t | head -n 1 | wc --bytes)
    local sizeHeadTwo=$(ls "$dst" -t | head -n 2 | tail -n 1 | wc --bytes)
    local sizeHeadThree=$(ls "$dst" -t | head -n 3 | tail -n 1 | wc --bytes)
    local sizeAverage=$(( (sizeHeadTwo + sizeHeadThree) / 2 ))  # Calculate the average size of two recent backups
    
    # Log the backup operation details to the specified log file
    local endTime=$(date +"%Y-%m-%d %H:%M")
    echo "$startTime | $endTime | $name | Status: $status | Desc: $description | Actual: $sizeHeadOne | Expected: $sizeAverage" >> $log
    
    return
}

# Log file path with the current date
log="/path/to/log/Copy-"$(date +%Y_%m_%d)".log"

# Define source directories for different databases
src_src1="/path/to/source1/"
src_db1="$src_src1""db1"
src_db2="$src_src1""db2"
src_db3="$src_src1""db3"
src_db4="$src_src1""db4"
src_db5="$src_src1""db5"
src_db6="$src_src1""db6"
src_db7="$src_src1""db7"

src_src2="/path/to/source2/"
src_db8="$src_src2""db8"
src_db9="$src_src2""db9"
src_db10="$src_src2""db10"
src_db11="$src_src2""db11"
src_db12="$src_src2""db12"

src_src3="/path/to/source3/"
src_db13="$src_src3""db13"

# Define destination directories for backups
dst_dst1="/path/to/destination1/"
dst_db1="$dst_dst1""db1"
dst_db2="$dst_dst1""db2"
dst_db3="$dst_dst1""db3"
dst_db4="$dst_dst1""db4"
dst_db5="$dst_dst1""db5"
dst_db6="$dst_dst1""db6"
dst_db7="$dst_dst1""db7"
dst_db8="$dst_dst1""db8"
dst_db9="$dst_dst1""db9"
dst_db10="$dst_dst1""db10"
dst_db11="$dst_dst1""db11"
dst_db12="$dst_dst1""db12"

dst_dst2="/path/to/destination2/"

# Execute daily backups if the flag is set to "day"
if [ "$flag" == "day" ]; then
    func "$src_db1/" "$dst_db1/" "db1" "$log" "bak" "-1" "+2"
    func "$src_db2/" "$dst_db2/" "db2" "$log" "bak" "-1" "+2"
    func "$src_db4/" "$dst_db4/" "db4" "$log" "bak" "-1" "+2"
    func "$src_db5/" "$dst_db5/" "db5" "$log" "bak" "-1" "+2"
    func "$src_db6/" "$dst_db6/" "db6" "$log" "bak" "-1" "+2"
    func "$src_db7/" "$dst_db7/" "db7" "$log" "bak" "-1" "+2"
    func "$src_db8/" "$dst_db8/" "db8" "$log" "bak" "-1" "+2"
    func "$src_db10/" "$dst_db10/" "db10" "$log" "bak" "-1" "+2"
    func "$src_db11/" "$dst_db11/" "db11" "$log" "bak" "-1" "+2"
    func "$src_db12/" "$dst_db12/" "db12" "$log" "bak" "-1" "+2"

# Execute nightly backups if the flag is set to "night"
elif [ "$flag" == "night" ]; then
    func "$src_db3/" "$dst_db3/" "db3" "$log" "bak" "-1" "+2"
    func "$src_db9/" "$dst_db9/" "db9" "$log" "bak" "-1" "+2"

# Execute training database backups if the flag is set to "trn"
elif [ "$flag" == "trn" ]; then
    func "$src_db13/" "$dst_db13/" "db13" "$log" "trn" "0" "+0"
fi
