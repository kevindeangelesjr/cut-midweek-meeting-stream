# cut-midweek-meeting-stream

Tool to cut a midweek meeting recording from JW Stream into individual video parts.

## Requirements

- Python 3.13+
- `ffmpeg-python`
- `ffmpeg` installed and available on the system `PATH`

## Installation

1. Install dependencies:
   ```sh
   poetry install
   ```

## Usage

Run the main script:

```sh
python main.py
```

The script will:

- check that the recording directory exists
- optionally delete older recordings while keeping the most recent one
- find the latest `.mp4` recording in the `JWSTREAM` folder
- prompt you for part names and timestamps
- cut each part into a separate `mp4` file

## Project structure

- `main.py` — entry point for the tool
- `src/cut_meeting.py` — helper functions for path/recording discovery and user input
- `src/MeetingPart.py` — meeting part validation and ffmpeg-based cutting logic

## Notes

- The default recording path is `c:/Users/<current_user>/JWSTREAM`
- Output files are saved to the same directory by default
- Timestamp format must be `hh:mm:ss`