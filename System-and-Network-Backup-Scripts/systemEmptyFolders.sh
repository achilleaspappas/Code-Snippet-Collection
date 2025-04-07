#!/bin/bash

# Record the start time of clearing the @Recycle folder
local startTime=$(date +"%Y-%m-%d %H:%M")
dir1="/path/to/@Recycle"  # Directory path for the @Recycle folder

# Remove all contents in the @Recycle folder
rm -rf "$dir1"/*

# Record the end time of the operation
local endTime=$(date +"%Y-%m-%d %H:%M")

# Log the start and end time for the @Recycle folder cleanup
echo "$startTime | $endTime | FOLDER Recycle Bin" >> $log

# Repeat the process for the #recycle folder
local startTime=$(date +"%Y-%m-%d %H:%M")
dir2="/path/to/#recycle"
rm -rf "$dir2"/*
local endTime=$(date +"%Y-%m-%d %H:%M")
echo "$startTime | $endTime | FOLDER Recycle Bin" >> $log

# Repeat the process for another instance of the #recycle folder
local startTime=$(date +"%Y-%m-%d %H:%M")
dir3="/path/to/#recycle"
rm -rf "$dir3"/*
local endTime=$(date +"%Y-%m-%d %H:%M")
echo "$startTime | $endTime | FOLDER Recycle Bin" >> $log

# Record start time for clearing the Temp folder
local startTime=$(date +"%Y-%m-%d %H:%M")
dir4="/path/to/Temp"  # Directory path for the Temp folder

# Remove all contents in the Temp folder
rm -rf "$dir4"/*

# Record the end time of the Temp folder cleanup
local endTime=$(date +"%Y-%m-%d %H:%M")

# Log the start and end time for the Temp folder cleanup
echo "$startTime | $endTime | FOLDER Temp" >> $log
