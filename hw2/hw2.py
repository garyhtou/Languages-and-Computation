"""
Gary Tou
CPSC 3400, HW 2
1/19/2022
https://seattleu.instructure.com/courses/1602042/assignments/6989792
"""

import sys
import os

# Constants
AM = 'AM'
PM = 'PM'
VALID_MERIDIEMS = [AM, PM]


class ImproperTimeError(Exception):
    """Raised when a time is improperly formatted"""
    pass


class EmtpyFileError(Exception):
    """Raised when an input file is empty (size in bytes == 0)"""
    pass


def create_time_list(filename):
    """
    Reads a file (the name of the file is stored in the parameter, `filename`)
    consisting of times and returns a list of time tuples. Each line in the file
    represents a single time and the order of the items in the list must match
    the order in the file.

    Args:
        filename (string): Name of the input file

    Raises:
        EmtpyFileError: The input file is empty (size in bytes == 0)
        ImproperTimeError: The input file contains a time that is improperly
            formatted
        FileNotFoundError: The input filename/path does not exist


    Returns:
        list of (int, int, string): A list of time tuples. Each time tuple has three
            elements in this order: (hours, minutes, AM/PM).

    >>> # This doctest requires the instructor-provided 'sample1.txt' input file
    ... try:
    ...     create_time_list("sample1.txt")
    ... except FileNotFoundError:
    ...     ("This doctest failed because the instructor-provided "
    ...      "'sample1.txt' input file was not present.")
    [(4, 12, 'PM'), (8, 23, 'PM'), (4, 3, 'AM'), (1, 34, 'AM'), (12, 48, 'PM'), (4, 13, 'AM'), (11, 9, 'AM'), (3, 12, 'PM'), (4, 10, 'PM')]
    """
    times = []

    # Check if file is empty
    if os.stat(filename).st_size == 0:
        raise EmtpyFileError

    # This will raise a `FileNotFoundError` if the file doesn't exist
    with open(filename) as file:
        while (line := file.readline().strip()):
            # Skips empty lines
            if len(line) == 0:
                continue

            try:
                rawHours, rawMinutes, meridiem = line.split(' ')

                # validate and convert inputs
                hours = int(rawHours)
                minutes = int(rawMinutes)

                validations = [
                    meridiem in VALID_MERIDIEMS,
                    hours >= 1 and hours <= 12,
                    minutes >= 0 and minutes <= 59,
                    # must have 2 digits (padded with leading 0)
                    len(rawMinutes) == 2,
                ]
                # If any of the validations fail, raise an error
                if not all(validations):
                    raise ImproperTimeError

                times.append((hours, minutes, meridiem))

            except ValueError:
                # catch and reraise error for these following cases:
                #   - non-integer values for hours and minutes
                #   - incorrect number of fields
                raise ImproperTimeError

    return times


def time_compare_gen(time_list, target):
    """
    The yielded tuples will contain two integers in this order: (hours,
    minutes).

    Args:
        time_list (list of (int, int, string)): list of time tuples from
            create_time_list
        target ((int, int, string)): a single time tuple

    >>> [t for t in time_compare_gen([(4, 13, 'PM')], (4, 12, 'PM'))]
    [(0, 1)]
    >>> [t for t in time_compare_gen([(6, 20, 'PM')], (4, 12, 'PM'))]
    [(2, 8)]
    >>> [t for t in time_compare_gen([(4, 12, 'AM')], (4, 12, 'PM'))]
    [(12, 0)]
    >>> [t for t in time_compare_gen([(4, 11, 'PM')], (4, 12, 'PM'))]
    [(23, 59)]
    >>> [t for t in time_compare_gen([(4, 12, 'PM')], (4, 12, 'PM'))]
    [(0, 0)]
    >>> [t for t in time_compare_gen([(4, 12, 'PM')], (4, 12, 'AM'))]
    [(12, 0)]
    >>> [t for t in time_compare_gen([(12, 0, 'AM')], (4, 12, 'AM'))]
    [(19, 48)]
    >>> [t for t in time_compare_gen([(12, 0, 'PM')], (4, 12, 'PM'))]
    [(19, 48)]
    """

    if target is None:
        return

    # Get minutes since midnight for target
    target_total_minutes = minutes_since_midnight(target)

    for time in time_list:
        # Get minutes since midnight for time
        time_total_minutes = minutes_since_midnight(time)

        # Calculate difference
        diff_total_minutes = time_total_minutes - target_total_minutes

        # Wrap around
        if diff_total_minutes < 0:
            diff_total_minutes += 24 * 60

        # Convert total minutes to hours and minutes
        hours = diff_total_minutes // 60
        minutes = diff_total_minutes % 60

        # Yield the difference
        yield (hours, minutes)


# Helper functions
def to_24_hour_time(time):
    """
    Converts a normal time tuple (12-hour) into a 24-hour time tuple.
    Hours ranges from 0 to 23 (not 1 to 24)

    Args:
        time ((int, int, string)): a single time tuple

    Returns:
        (int, int): a 24-hour time tuple

    >>> to_24_hour_time((4, 12, 'PM'))
    (16, 12)
    >>> to_24_hour_time((4, 12, 'AM'))
    (4, 12)
    >>> to_24_hour_time((12, 12, 'AM'))
    (0, 12)
    >>> to_24_hour_time((12, 12, 'PM'))
    (12, 12)
    >>> to_24_hour_time((1, 12, 'PM'))
    (13, 12)
    >>> to_24_hour_time((1, 12, 'AM'))
    (1, 12)
    >>> to_24_hour_time((11, 59, 'PM'))
    (23, 59)
    >>> to_24_hour_time((11, 59, 'AM'))
    (11, 59)
    >>> to_24_hour_time((12, 0, 'AM'))
    (0, 0)
    >>> to_24_hour_time((12, 0, 'PM'))
    (12, 0)
    """
    hours, minutes, meridiem = time

    # Wrap hours
    if(meridiem == AM and hours == 12):
        hours = 0

    offset = 12 if meridiem == PM and hours != 12 else 0
    return (hours + offset, minutes)


def minutes_since_midnight(time):
    """
    Converts a time tuple into a integer representing the number of minutes
    since midnight.

    Args:
        time ((int, int, string)): a single time tuple

    Returns:
        int: the number of minutes since midnight

    >>> minutes_since_midnight((4, 12, 'PM'))
    972
    >>> minutes_since_midnight((4, 12, 'AM'))
    252
    >>> minutes_since_midnight((12, 12, 'AM'))
    12
    >>> minutes_since_midnight((12, 12, 'PM'))
    732
    >>> minutes_since_midnight((1, 12, 'PM'))
    792
    >>> minutes_since_midnight((1, 12, 'AM'))
    72
    >>> minutes_since_midnight((11, 59, 'PM'))
    1439
    >>> minutes_since_midnight((11, 59, 'AM'))
    719
    >>> minutes_since_midnight((12, 0, 'AM'))
    0
    >>> minutes_since_midnight((12, 0, 'PM'))
    720
    """
    hours, minutes = to_24_hour_time(time)
    return hours * 60 + minutes


def main(filename):
    try:
        # Create a list time from the input file
        time_list = create_time_list(filename)

        # Print time list in string format
        print(
            [f'{t[0]}:{t[1]:02d} {t[2]}' for t in time_list]
        )

        # Print the time that occurs latest in the day
        print(
            max(time_list, key=minutes_since_midnight)
        )

        # Print the sorted time list in ascending order
        print(
            sorted(time_list, key=minutes_since_midnight)
        )

        # Create a target (first entry in time list) and print the difference of
        # each time in time list from that target
        target = time_list[0]
        print(
            [d for d in time_compare_gen(time_list, target)]
        )

    # Handle exceptions
    except ImproperTimeError:
        print(("Improper Time Error: The input file contains a time that is "
               "improperly formatted. Please use the following strftime format "
               "'%I %M %p'. eg. '1 00 PM'."))
        sys.exit(1)
    except EmtpyFileError:
        print("Empty File Error: The input file is empty (zero bytes).")
        sys.exit(1)
    except FileNotFoundError:
        print("File Not Found Error: The input file does not exist.")
        sys.exit(1)
    except Exception as e:
        print("HW2: An error has occured.")
        print("    ", e)


if __name__ == '__main__':
    # Get the name of the input file from the command line (using sys.argv)
    try:
        filepath = sys.argv[1]
        main(filepath)
    except IndexError:
        # Exit if no input file is provided
        print("Usage: hw2 <filepath>")
        sys.exit(1)
