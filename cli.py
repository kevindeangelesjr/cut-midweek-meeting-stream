#!/usr/bin/env python3

# Imports
import logging
import os
from src.cut_meeting import path_exists, delete_old_recordings, get_latest_recording_file, get_part

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Variables
video_format="mp4"
purge_recordings = True
current_user = os.getlogin()
recording_path = os.path.normpath('c:/Users/' + current_user + '/JWSTREAM')
output_path = recording_path

# Main
if __name__ == "__main__":

    # Delete all old recordings in the recording path
    if path_exists(recording_path):
        if purge_recordings:
            delete_old_recordings(recording_path, 1, video_format)
    
    # Get the recording file
    recording_file = get_latest_recording_file(recording_path, video_format)

    # Prompt user for part timestamps
    done = False
    parts = []
    print()
    while not done:
        part = get_part(recording_file)
        parts.append(part)
        cont = input("Do you want to add another part? (y/n): ")
        if cont.lower() != 'y':
            done = True
    print()

    # Cut the parts from the recording file
    for part in parts:
        logging.info(f"Processing part '{part.name}' with start time {part.start_time} and end time {part.end_time}.")
        if part.timestamps_sequence_valid():
            part.cut_part(output_path, video_format)
    
    logging.info("All parts have been cut successfully.")