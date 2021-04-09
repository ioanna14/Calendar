import re
import time
from Calendar import Calendar

"""
We read the input from the file, we use the method find to get the meeting time, 
and a regular expression to find all the intervals of time from the string.
:file_name - the path of the input file as string
:return - calendars (the list of all calendars), meeting_time (the maximum meeting time, integer)
"""


def read_from_file(file_name):
    program = []
    calendars = []
    f = open(file_name, "r")

    content = f.read()

    meeting_time_string = "Meeting Time Minutes:"
    index = content.find(meeting_time_string)
    meeting_time = int(content[index + len(meeting_time_string):].strip())

    lis_of_content = content.split("calendar")

    for element in lis_of_content:
        m = re.findall("\d{1,2}:\d{2}", element)
        if m:
            # We append all the hours found in the string to the program list
            each_program = []
            for timeline in m:
                format_time = time.strptime(timeline, '%H:%M')
                each_program.append(format_time)
            program.append(each_program)

    for j in range(0, len(program), 2):
        booked = []
        range_limit = []

        # We group the booked calendar two by two and the range limit calendar as well
        for i in range(0, len(program[j]), 2):
            booked.append([program[j][i], program[j][i + 1]])
        for k in range(0, len(program[j + 1]), 2):
            range_limit = [program[j + 1][k], program[j + 1][k + 1]]

        # We create a new Calendar and append it to the list of all calendars
        calendars.append(Calendar(booked, range_limit))

    return calendars, meeting_time


"""
Write into the file the result.
:file_name - the path of the input file as string
:output - the string with the available time for meetings
"""


def write_into_file(file_name, output):
    f = open(file_name, "w")
    f.write(str(output))


if __name__ == '__main__':
    calendars, meeting = read_from_file("input.txt")
    # A day will be represented in minutes
    # 0 -> 1440
    lower_limit = 0
    upper_limit = 1440
    all_day = set(range(lower_limit, upper_limit))
    free_time = all_day
    # We will intersect all the calendars.
    for calendar in calendars:
        free_time = sorted(set(free_time).intersection(set(calendar.get_available())))

    # We must find all ranges greater or equal with the meeting time.
    ranges = []
    start = -1
    current = -1
    for i, index in enumerate(free_time):
        # If we are in the beginning
        if current == -1:
            start = index
            current = index
        # Elif the index is part of the range
        elif current + 1 == index:
            current = index
        # Elif the index is part of the next range
        elif current + 1 != index or i + 1 == len(free_time):
            if current - start + 1 >= meeting:
                ranges.append([start, current + 1])
            current = index
            start = index

    output = []
    # We must transform the ranges back to hours and minutes of the day.
    for times in ranges:
        start = ''

        # We have to check if the minute is 0 or 60 for both starting time
        # and ending time and double it, if it is that way
        start_h = times[0] // 60
        if start_h != 0:
            start += str(start_h)
        else:
            start += '00'
        start += ':'
        start_m = times[0] % 60
        if start_m != 0:
            start += str(start_m)
        else:
            start += '00'

        end = ''
        end_h = times[1] // 60
        if end_h != 0:
            end += str(end_h)
        else:
            end += '00'
        end += ':'
        end_m = times[1] % 60
        if end_m != 0:
            end += str(end_m)
        else:
            end += '00'

        output.append([start, end])

    write_into_file("output.txt", output)

"""
I had to make a guess on the example because from the task 
because in the input we had two mistakes (I guess).
1. The second booked calendar, was named booked calendar1,
the same as the first one.
2. The input said that the first person has time for a meeting
between ['10:30','12:00'] and the second one, ['11:30','12:30].
It seems to me that the intersected time for meeting must be
['11:30','12:00'], and not ['11:30','12:30'] as it says in 
the example output.
"""
