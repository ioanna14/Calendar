class Calendar:
    def __init__(self, booked, limit):
        self._booked_calendar = booked
        self._range_limit = limit
        self._free_time = self._set_free_time_from_range()
        self._mark_busy()

    """
    Returns the free time.
    """

    def get_available(self):
        return self._free_time

    """
    We generate the time when the person may have meetings.
    :return - a list of integers, representing the minutes of the day  
    """

    def _set_free_time_from_range(self):
        start = self._range_limit[0]
        end = self._range_limit[1]
        start_int = start.tm_min + start.tm_hour * 60
        end_int = end.tm_min + end.tm_hour * 60

        return list(range(start_int, end_int + 1))

    """
    Remove the time in which the person already has meetings, from the free time.
    """

    def _mark_busy(self):
        for busy in self._booked_calendar:
            start = busy[0]
            end = busy[1]

            start_int = start.tm_min + start.tm_hour * 60
            end_int = end.tm_min + end.tm_hour * 60
            # We compute the difference of the sets to find the actual free time in the calendar
            self._free_time = set(self._free_time).difference(set(range(start_int, end_int)))

        # We use sorted for having the the minutes of the day in order
        self._free_time = sorted(self._free_time)

    def __str__(self):
        return "Booked calendar: " + \
               str(self._booked_calendar) + \
               "\n range limits: " + \
               str(self._range_limit) + \
               "\nfreetime:" + str(self._free_time)
