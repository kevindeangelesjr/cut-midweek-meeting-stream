#!/usr/bin/env python3

import os
import re
import ffmpeg
import logging

class MeetingPart:

    def __init__(self, name: str, start_time: str, end_time: str, recording_file: str):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.recording_file = recording_file

    def check_timestamps(self) -> bool:
        # Basic validation to check if timestamps are in the correct format (hh:mm:ss)
        pattern = "^[\d:]+$"
        if not re.fullmatch(pattern, self.start_time) or not re.fullmatch(pattern, self.end_time):
            logging.error(f"Invalid timestamp format for part '{self.name}'. Start: {self.start_time}, End: {self.end_time}.")
            raise ValueError("Invalid timestamp format. Please enter timestamps in the format hh:mm:ss.")
        return True

    def timestamps_sequence_valid(self) -> bool:
        # Convert timestamps to seconds for comparison
        def time_to_seconds(t: str) -> int:
            parts = list(map(int, t.split(':')))
            return parts[0] * 3600 + parts[1] * 60 + parts[2]

        start_seconds = time_to_seconds(self.start_time)
        end_seconds = time_to_seconds(self.end_time)

        if start_seconds >= end_seconds:
            logging.error(f"Start time must be less than end time for part '{self.name}'. Start: {self.start_time}, End: {self.end_time}.")
            raise ValueError("Start time must be less than end time.")
        return True

    def cut_part(self, output_path: str, video_format: str) -> None:
        logging.info(f"Cutting part '{self.name}' from {self.recording_file} (start: {self.start_time}, end: {self.end_time}).")
    
        try:
            output_file = os.path.join(output_path, f"{self.name}.{video_format}")
            (
                ffmpeg
                .input(self.recording_file)
                .output(output_file, ss=self.start_time, to=self.end_time, c='copy')
                .run(capture_stdout=True, capture_stderr=True)
            )
            logging.info(f"Successfully cut part '{self.name}' and saved to {output_file}.")
        except ffmpeg.Error as e:
            logging.error(f"FFmpeg error occurred while cutting part '{self.name}': {e.stderr.decode()}")
            raise
        except Exception as e:
            logging.error(f"An error occurred while cutting part '{self.name}': {e}")
            raise