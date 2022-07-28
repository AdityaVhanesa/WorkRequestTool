from datetime import datetime


class dateTime:
    def __init__(self, dateTimeObject):
        self.__weekDays = ["Monday",
                           "Tuesday",
                           "Wednesday",
                           "Thursday",
                           "Friday",
                           "Saturday",
                           "Sunday"]
        self.year = "None"
        self.day = "None"
        self.weekday = "None"

        if dateTimeObject is not None:
            self.year = dateTimeObject.year
            self.month = dateTimeObject.month
            self.day = dateTimeObject.day
            self.hour = dateTimeObject.hour
            self.minute = dateTimeObject.minute
            self.second = dateTimeObject.second
            self.weekday = self.__weekDays[dateTimeObject.weekday()]

    def __str__(self):
        if self.weekday == "None":
            return ""
        return f"{self.weekday} {self.day}, {self.year}"
