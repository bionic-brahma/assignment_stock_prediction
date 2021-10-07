import re
import datetime


class ICSout:

    # this is our constructor
    def __init__(self, filename):
        self.hello = "Alive"
        self.filename = filename

    def get_events_for_day(self, dt):
        formated_date = self.input_date_format_converter(dt)
        dt = datetime.datetime(formated_date[0], formated_date[1], formated_date[2])
        events = self.sort_events()

        # convert dt to the format we want to print out. e.g  June 18, 2019 (Tue)
        # and add the second line dashes the store in a string called header
        line = dt.strftime("%B") + " " + dt.strftime("%d") + ", " + dt.strftime("%Y") + " (" + dt.strftime("%a") + ")"
        header = line + '\n' + ("-" * len(line))

        body = ""
        counter = 0

        # we go though the sorted list. if the the passed date
        # have events on the list. we print out all the events happen in same day

        for event in events:
            if event["DTSTART"].year == dt.year and event["DTSTART"].month == dt.month and event["DTSTART"].day == dt.day:

                # get the value from dictionary
                DT_day = event["DTSTART"].day
                DT_year = event["DTSTART"].year
                DT_hour = event["DTSTART"].hour
                DT_minute = event["DTSTART"].minute

                if DT_minute < 10:
                    DT_minute = "0" + str(DT_minute)

                    # convert time to am or pm
                if DT_hour > 12:
                    DT_hour -= 12
                    format_DThour_min = str(DT_hour) + ":" + str(DT_minute) + " PM"
                elif DT_hour == 12:
                    format_DThour_min = str(DT_hour) + ":" + str(DT_minute) + " PM"
                    format_DThour_min = str(DT_hour) + ":" + str(DT_minute) + " PM"
                elif DT_hour < 12:
                    format_DThour_min = str(DT_hour) + ":" + str(DT_minute) + " AM"

                END_day = event["DTEND"].day
                END_year = event["DTEND"].year
                END_hour = event["DTEND"].hour
                END_minute = event["DTEND"].minute

                if END_minute < 10:
                    END_minute = "0" + str(END_minute)

                if END_hour > 12:
                    END_hour -= 12
                    format_ENDhour_min = str(END_hour) + ":" + str(END_minute) + " PM"
                elif END_hour == 12:
                    format_ENDhour_min = str(END_hour) + ":" + str(END_minute) + " PM"
                elif END_hour < 12:
                    format_ENDhour_min = str(END_hour) + ":" + str(END_minute) + " AM"

                if DT_day < 10:
                    DT_day = "0" + str(DT_day)

                # format output in string body
                body += "\n" + '{:>8} to {:>8}: {} {{{{{}}}}}'.format(format_DThour_min, format_ENDhour_min,
                                                                      event["SUMMARY"],
                                                                      event["LOCATION"])

        # if no events founded return none
        if body == "":
            return None
        # if find any events. then concatnate header and body and return it
        else:
            return header + body

    def input_date_format_converter(self, date):
        year, month, day = date.split("/")
        return int(year), int(month), int(day)

    def extract(self):
        # read all the lines from the file provided with the use of readfile method
        lines = self.readfile()

        # use a list to store all the events , events are dictionary
        events = []

        # for loop go through each line find the value of BEGIN, DTSTART, DTEND,RRULE
        # LOCATION, SUMMARY and store them in a dictionary
        for line in lines:

            # an single event start with "BEGIN:VEVENT"
            if re.match("^BEGIN:VEVENT", line):
                event = {}

            # use regex to get the number value if datetime.
            # when regex matches the rule it will return the values to its corresponding variables
            elif re.match("^DTSTART:", line):
                (year, month, day) = re.match(".*(\d{4})(\d{2})(\d{2})T.*", line).groups()
                (hour, minute, second) = re.match(".*T(\d{2})(\d{2})(\d{2})", line).groups()

                event["DTSTART"] = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute),
                                                     int(second))

            elif re.match("^DTEND:", line):
                (year, month, day) = re.match(".*(\d{4})(\d{2})(\d{2})T.*", line).groups()
                (hour, minute, second) = re.match(".*T(\d{2})(\d{2})(\d{2})", line).groups()
                event["DTEND"] = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

            elif re.match("^RRULE:", line):
                (year, month, day) = re.match(".*(\d{4})(\d{2})(\d{2})T.*", line).groups()
                (hour, minute, second) = re.match(".*T(\d{2})(\d{2})(\d{2})", line).groups()
                event["RRULE"] = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

            # the use of split to get the LOCATION & SUMMARY information. the content after : is in list 1
            elif re.match("^LOCATION:", line):
                event["LOCATION"] = re.split(r":", line)[1]

            elif re.match("^SUMMARY:", line):
                event["SUMMARY"] = re.split(r":", line)[1]

            # an single event end with "END:VEVENT"
            elif re.match("^END:VEVENT", line):
                events.append(event)
        return events

    # This method is to read all the lines from the file provided
    def readfile(self):
        f = open(self.filename, 'r')
        lines = f.readlines()
        # counter variable for lines
        index = 0

        # rstrip() get rid of new line character
        while index <= (len(lines) - 1):
            lines[index] = lines[index].rstrip()
            index += 1
        return lines

    # This method is to check when the RRULE occurred in file
    def extend(self):
        # call method extract
        events = self.extract()

        temp = []
        for e in events:

            # if RRULE seen we increment Starting date by 7
            if "RRULE" in e.keys():
                d_date = e["DTSTART"]
                while d_date <= e["RRULE"]:
                    new_e = {}
                    new_e["DTSTART"] = d_date
                    new_e["DTEND"] = e["DTEND"]
                    new_e["LOCATION"] = e["LOCATION"]
                    new_e["SUMMARY"] = e["SUMMARY"]

                    temp.append(new_e)
                    d_date += datetime.timedelta(7)
            # if not add dictionary to temp and return
            else:
                temp.append(e)
        return temp

    #  sort_ events method is to sort all the events based on the day.abs
    # If there are two events occurs in same date, then compare their summary

    def sort_events(self):
        # call class methond extend
        modifed_events = self.extend()

        # compare dates
        length = len(modifed_events)

        # read through all the dictionary in list and sort each dictionary by insertion sort
        for i in range(length - 1):
            for j in range(i, length):
                if modifed_events[i]["DTSTART"] > modifed_events[j]["DTSTART"]:
                    temp = modifed_events[j]
                    modifed_events[j] = modifed_events[i]
                    modifed_events[i] = temp

        # if two events have same starting and ending time, then we sort it by the value of SUMMARY
        for i in range(len(modifed_events) - 1):
            if modifed_events[i]["DTSTART"] == modifed_events[i + 1]["DTSTART"] and modifed_events[i]["SUMMARY"].startswith(modifed_events[i + 1]["SUMMARY"]):
                temp = modifed_events[i + 1]
                modifed_events[i + 1] = modifed_events[i]
                modifed_events[i] = temp
        return modifed_events


def main():

    # Testing
    eventgetter = ICSout("one.ics")
    print(eventgetter.get_events_for_day("2021/2/14"))


if __name__ == "__main__":
    main()
