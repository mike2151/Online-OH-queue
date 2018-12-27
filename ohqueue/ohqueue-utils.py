import datetime
# takes in the current time and the times specified by the OHqueue and sees if it is active 
def isQueueActive(times_open):
    s = times_open
    today = datetime.datetime.now()
    current_weekday = today.weekday()
    if current_weekday == 0:
        # get string between "Monday" and "Tuesday"
        s = s[s.index("Monday"):]
        s = s[:s.index("Tuesday")]
    elif current_weekday == 1:
        # get string between "Tuesday" and "Wednesday"
        s = s[s.index("Tuesday"):]
        s = s[:s.index("Wednesday")]
    elif current_weekday == 2:
        # get string between "Wednesday" and "Thursday"
        s = s[s.index("Wednesday"):]
        s = s[:s.index("Thursday")]
    elif current_weekday == 3:
        # get string between "Thursday" and "Friday"
        s = s[s.index("Thursday"):]
        s = s[:s.index("Friday")]
    elif current_weekday == 4:
        # get string between "Friday" and "Saturday"
        s = s[s.index("Friday"):]
        s = s[:s.index("Saturday")]
    elif current_weekday == 5:
        # get string between "Saturday" and "Sunday"
        s = s[s.index("Saturday"):]
        s = s[:s.index("Sunday")]
    elif current_weekday == 6:
        # get string between "Sunday" and end
        s = s[s.index("Sunday"):]
    s = s[s.index(":")+1:]
    # split using deliminator ;
    day_times = s.split(";")
    isValidTime = False
    current_hour = today.hour
    current_minute = today.minute
    for time_slot in day_times:
        start_time = time_slot.split("-")[0]
        end_time = time_slot.split("-")[1]
        start_time_int_hour = int((datetime.datetime.strptime(start_time, '%I:%M%p')).strftime("%H"))
        end_time_int_hour = int((datetime.datetime.strptime(end_time, '%I:%M%p')).strftime("%H"))
        start_time_int_minute = int((datetime.datetime.strptime(start_time, '%I:%M%p')).strftime("%M"))
        end_time_int_minute = int((datetime.datetime.strptime(end_time, '%I:%M%p')).strftime("%M"))
        if (current_hour >= start_time_int_hour and current_hour <= end_time_int_hour
        and current_minute >= start_time_int_minute and current_minute <= end_time_int_minute):
            isValidTime = True
            break
    return isValidTime

