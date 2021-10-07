#
# UVic SENG 265, Spring 2021, Assignment #4
#
# Student work is to appear in this module.
#

import datetime

def convert24_to_12(strg):
    ret = ""
    h1 = ord(strg[0]) - ord('0')
    h2 = ord(strg[1]) - ord('0')

    hh = h1 * 10 + h2

    Meridien = ""
    if (hh < 12):

        Meridien = "AM"

    else:

        Meridien = "PM"

    hh %= 12

    if hh == 0:

        ret = "12:"

        for i in range(2, 4):
            ret = ret + strg[i]

    else:

        if len(str(hh)) == 1:
            hh = str(hh)
            hh = " " + hh
        ret = str(hh) + ":"

        for i in range(2, 4):
            ret = ret + strg[i]

    ret = ret + " " + Meridien

    return ret


def date_day(year=0, month=0, day=0):
    x = datetime.datetime(int(year), int(month), int(day))

    return x.strftime("%A")[0:2]


def date_to_day(year=0, month=0, day=0):
    x = datetime.datetime(int(year), int(month), int(day))

    if int(str(day)) < 10 and len(str(day)) == 1:
        day = '0' + str(day)

    return x.strftime("%B") + " " + str(day) + ", " + str(year) + " (" + x.strftime("%A")[0:3] + ")"


def date_component_converter(date):
    date, time = date.split("T")

    return date, time


def input_date_format_converter(date):
    year, month, day = date.split("/")

    if int(day) < 10 and len(day) == 1:
        day = '0' + day

    if int(month) < 10 and len(month) == 1:
        month = '0' + month

    return str(year) + str(month) + str(day)


class ICSout:

    def __init__(self, filename):
        self.hello = "Alive"
        self.filename = filename

    def get_events_for_day(self, dt):
        print("DEBUG " + str(dt))

    ##########################################

        file = open(self.filename, 'r')
        dictionary_info = dict()
        dictionary_info["RRULE"] = None
        dictionary_info["END"] = None
        line = file.readline()
        weekdays = {"SU": 0, "MO": 1, "TU": 2, "WE": 3, "TH": 4, "FR": 5, "SA": 6}
        temporary = ""
        comparedate = input_date_format_converter(dt)


       # startdate = input_date_format_converter(args.start)
       # enddate = input_date_format_converter(args.end)


        flag = False

        while line:

            line = line.split("\n")[0]
            dictionary_info[line.split(":")[0]] = line.split(":")[1]
            line = file.readline()

            if dictionary_info["END"] == "VEVENT":

                if dictionary_info["RRULE"] is None:

                    startdate_temp, starttime_temp = date_component_converter(dictionary_info["DTSTART"])
                    enddate_temp, endtime_temp = date_component_converter(dictionary_info["DTEND"])

                    if startdate <= startdate_temp:

                        year = startdate_temp[0:4]
                        month = startdate_temp[4:6]
                        day = startdate_temp[6:8]

                        firstline = date_to_day(year, month, day)

                        secondline = convert24_to_12(starttime_temp) + " to " + convert24_to_12(endtime_temp) + ": " + \
                                     dictionary_info["SUMMARY"] + " {{" + dictionary_info["LOCATION"] + "}}"

                        if firstline != temporary:

                            if flag:
                                print("")

                            print(firstline)
                            print("-----------------------")
                            print(secondline)
                            temporary = firstline

                        else:

                            print(secondline)

                        # print("")
                        flag = True
                        dictionary_info = dict()
                        dictionary_info["RRULE"] = None
                        dictionary_info["END"] = None

                else:

                    pruleentries = dictionary_info["RRULE"].split(";")
                    byday = pruleentries[-1].split("=")[1]
                    until = pruleentries[-2].split("=")[1].split("T")[0]
                    startdate_temp, starttime_temp = date_component_converter(dictionary_info["DTSTART"])
                    enddate_temp, endtime_temp = date_component_converter(dictionary_info["DTEND"])

                    if startdate_temp <= startdate:

                        daydiff = weekdays[byday] - weekdays[
                            date_day(year=int(startdate[0:4]), month=int(startdate[4:6]), day=int(startdate[6:8])).upper()]

                        if daydiff < 0:
                            daydiff += 7

                        startdate = str(int(startdate) + daydiff)

                        while startdate <= until and startdate <= enddate:

                            year = startdate[0:4]
                            month = startdate[4:6]
                            day = startdate[6:8]

                            if int(day) > 30:
                                month = str(int(month) + 1)
                                day = str(int(day) - 30)

                            if int(month) > 12:
                                year = str(int(year) + 1)
                                month = str(int(month) - 12)

                            firstline = date_to_day(int(year), int(month), int(day))

                            secondline = convert24_to_12(starttime_temp) + " to " + convert24_to_12(endtime_temp) + ": " + \
                                         dictionary_info["SUMMARY"] + " {{" + dictionary_info["LOCATION"] + "}}"

                            if firstline != temporary:

                                if flag:
                                    print("")

                                print(firstline)
                                print("-----------------------")
                                print(secondline)
                                temporary = firstline

                            else:

                                print(secondline)

                            # print("")
                            flag = True
                            startdate = str(int(startdate) + 7)
                            year = startdate[0:4]
                            month = startdate[4:6]
                            day = startdate[6:8]

                            if int(day) > 30:

                                month = str(int(month) + 1)
                                day = str(int(day) - 30)
                                if len(day) == 1:
                                    day = "0" + day

                            if int(month) > 12:

                                year = str(int(year) + 1)
                                month = str(int(month) - 12)
                                if len(month) == 1:
                                    month = "0" + month

                            startdate = str(year) + str(month) + str(day)



