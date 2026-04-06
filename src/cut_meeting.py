#!/usr/bin/env python3

# Imports
import logging
import os
import glob
import re
from src.MeetingPart import MeetingPart

# Functions
def path_exists(path: str) -> bool:
    if not os.path.exists(path):
        raise FileNotFoundError(f"The path {path} does not exist.")
    return True

def delete_old_recordings(path: str, keep: int, video_format: str) -> None:
    logging.info(f"Checking for old recordings in {path} to delete, keeping the most recent {keep} recording(s).")

    if os.listdir(path) == []:
        raise FileNotFoundError(f"No files found in the path {path}.")

    # Sort files by modification time (oldest to newest)
    files = glob.glob(path + f"/*.{video_format}")
    files.sort(key=os.path.getmtime)
    for file in files[:-keep]:  # Keep the most recent 'keep' files
        os.remove(file)
        logging.info(f"Deleted old recording: {file}")

def get_latest_recording_file(path: str, video_format: str) -> str:
    # Get the most recent .mp4 file
    logging.info(f"Looking for .{video_format} files in {path} to find the most recent recording.")
    files = glob.glob(path + f"/*.{video_format}")
    if not files:
        raise FileNotFoundError(f"No .{video_format} files found in the path {path}.")

    latest_file = max(files, key=os.path.getmtime)
    logging.info(f"Found recording file: {latest_file}")
    return latest_file

def get_part(recording_file: str) -> MeetingPart:
    part_name = input("Enter the name of the part: ")
    start_time = input(f"Please enter the start timestamp for {part_name} (hh:mm:ss): ")
    end_time = input(f"Please enter the end timestamp for {part_name} (hh:mm:ss): ")

    part = MeetingPart(name=part_name, start_time=start_time, end_time=end_time, recording_file=recording_file)
    part.check_timestamps()
    return part