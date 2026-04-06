# cut-midweek-meeting-stream

Tool to cut a midweek meeting recording from JW Stream into individual video parts.

## Requirements

- Python 3.13+
- `ffmpeg-python`
- `PyQt6`
- `ffmpeg` installed and available on the system `PATH`

## Installation

1. Install dependencies:
   ```sh
   poetry install
   ```

## Usage

### GUI Application

Run the GUI application:

```sh
python app.py
```

The application provides a user interface to:

- select a recording file
- choose an output directory
- add parts with names and start/end timestamps
- cut each part into a separate `mp4` file

### CLI Application

Run the CLI application:

```sh
python cli.py
```

The script will:

- check that the recording directory exists
- optionally delete older recordings while keeping the most recent one
- find the latest `.mp4` recording in the `JWSTREAM` folder
- prompt you for part names and timestamps
- cut each part into a separate `mp4` file

## Project structure

- `app.py` — PyQt6 GUI application
- `cli.py` — CLI entry point
- `src/cut_meeting.py` — helper functions for path/recording discovery and user input
- `src/MeetingPart.py` — meeting part validation and ffmpeg-based cutting logic

## Notes

- Timestamp format must be `hh:mm:ss`
- Output files are saved to the selected output directory (GUI) or the same directory as the recording (CLI)