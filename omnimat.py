import datetime
import sys
from datetime import timezone
from typing import List

from icalendar import Calendar


class CalendarEvent:
    """Represents a calendar event with summary, start date, and attendee status."""

    def __init__(self, summary: str, start: datetime.datetime, attendee_status: str):
        self._summary = summary
        self._start = start
        self._attendee_status = attendee_status

    @property
    def summary(self) -> str:
        return self._summary

    @property
    def start(self) -> datetime.datetime:
        return self._start

    @property
    def attendee_status(self) -> str:
        return self._attendee_status

    def __str__(self) -> str:
        return f"Summary: {self.summary}\nStart: {self.start}\nAttendee Status: {self.attendee_status}\n"

    def __eq__(self, other):
        if isinstance(other, CalendarEvent):
            return (
                self.summary == other.summary
                and self.start == other.start
                and self.attendee_status == other.attendee_status
            )
        return False

    def __hash__(self):
        return hash((self.summary, self.start, self.attendee_status))


class CalendarReader:
    """Reads and processes calendar events from an iCalendar file."""

    def __init__(
        self,
        file_path: str,
        days_before: int = None,
        start_date: str = None,
        end_date: str = None,
    ):
        self._file_path = file_path
        self._days_before = days_before
        self._start_date = (
            datetime.datetime.strptime(start_date, "%d_%m_%Y").replace(
                tzinfo=timezone.utc
            )
            if start_date
            else None
        )
        self._end_date = (
            datetime.datetime.strptime(end_date, "%d_%m_%Y").replace(
                tzinfo=timezone.utc
            )
            if end_date
            else None
        )

    def read_events(self) -> List[CalendarEvent]:
        """Reads events from the iCalendar file and returns a list of CalendarEvent objects."""
        events = []
        with open(self._file_path, "r") as file:
            gcal = Calendar.from_ical(file.read())
            for component in gcal.walk():
                if component.name == "VEVENT":
                    start = component.get("dtstart").dt
                    if isinstance(start, datetime.date) and not isinstance(
                        start, datetime.datetime
                    ):
                        start = datetime.datetime.combine(
                            start, datetime.time.min, timezone.utc
                        )
                    elif isinstance(start, datetime.datetime) and start.tzinfo is None:
                        start = start.replace(tzinfo=timezone.utc)
                    if self._is_event_in_range(start):
                        attendee_status = self._get_attendee_status(component)
                        if attendee_status == "ACCEPTED":
                            event = CalendarEvent(
                                summary=component.get("summary"),
                                start=start,
                                attendee_status=attendee_status,
                            )
                            events.append(event)
        return sorted(events, key=lambda event: event.start)

    def _is_event_in_range(self, event_start: datetime.datetime) -> bool:
        """Checks if the event's start date is within the specified range."""
        if self._start_date and self._end_date:
            return self._start_date <= event_start <= self._end_date
        elif self._days_before:
            now = datetime.datetime.now(timezone.utc)
            days_ago = now - datetime.timedelta(days=self._days_before)
            return days_ago <= event_start <= now
        return True

    def _get_attendee_status(self, component) -> str:
        """Gets the attendee status for the event."""
        attendees = component.get("attendee")
        if attendees:
            if not isinstance(attendees, list):
                attendees = [attendees]
            for attendee in attendees:
                if (
                    hasattr(attendee, "params")
                    and attendee.params.get("PARTSTAT") == "ACCEPTED"
                ):
                    return "ACCEPTED"
        return "DECLINED"


class CalendarPrinter:
    """Prints calendar events."""

    @staticmethod
    def print_events(events: List[CalendarEvent]) -> None:
        """Prints the details of each event in the list in the specified template format."""
        formatted_events = [
            f"project meeting: {event.summary}_{event.start.strftime('%d.%m.%Y')};"
            for event in events
        ]
        print(" \n".join(formatted_events))


def main(
    file_path: str,
    days_before: int = None,
    start_date: str = None,
    end_date: str = None,
) -> None:
    """Main function to read and print calendar events."""
    reader = CalendarReader(file_path, days_before, start_date, end_date)
    events = reader.read_events()
    CalendarPrinter.print_events(events)


if __name__ == "__main__":
    if len(sys.argv) not in [3, 4]:
        print("Usage: python script.py <file_path> <days_before>")
        print("   or: python script.py <file_path> <start_date> <end_date>")
        sys.exit(1)

    file_path = sys.argv[1]
    if len(sys.argv) == 3:
        try:
            days_before = int(sys.argv[2])
            main(file_path, days_before=days_before)
        except ValueError:
            print("The number of days must be an integer.")
            sys.exit(1)
    else:
        start_date = sys.argv[2]
        end_date = sys.argv[3]
        main(file_path, start_date=start_date, end_date=end_date)
