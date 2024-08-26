## Overview

The Calendar Event Reader is a Python application designed to read and process calendar events from an iCalendar file. It filters events based on specified date ranges or a number of days before the current date and prints the details of accepted events in a specified format.

## Features

- Reads events from an iCalendar file.
- Filters events based on a date range or a number of days before the current date.
- Only includes events where the attendee status is "ACCEPTED".
- Prints event details in a formatted template.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/calendar-event-reader.git
    cd calendar-event-reader
    ```

2. Install the required dependencies:
    ```sh
    poetry shell
    poetry install
    ```

## Usage

Run the script with the following command:

```sh
python script.py <file_path> <days_before>
```

or

```sh
python script.py <file_path> <start_date> <end_date>
```

### Parameters

- `<file_path>`: Path to the iCalendar file.
- `<days_before>`: Number of days before the current date to filter events.
- `<start_date>`: Start date in the format `dd_mm_yyyy`.
- `<end_date>`: End date in the format `dd_mm_yyyy`.

### Examples

1. To read events from the last 7 days:
    ```sh
    python script.py calendar.ics 7
    ```

2. To read events between specific dates:
    ```sh
    python script.py calendar.ics 01_01_2023 31_01_2023
    ```
