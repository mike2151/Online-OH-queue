from django.db import models
from questions.models import Question
import datetime
from django.conf import settings
import pytz
from django.utils.timezone import activate

# Create your models here.
class OHQueue(models.Model):
    name = models.CharField(max_length=256, unique=True)
    questions = models.ManyToManyField(Question, blank=True)
    times_open = models.CharField(max_length=1024)
    is_open_extended = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    is_in_time = models.BooleanField(default=False)
    # average wait time fields
    average_wait_time = models.FloatField(default=0.0)
    num_questions_answered = models.IntegerField(default=0)
    last_answer_time = models.DateField(default=datetime.date.today)

    def question_contents(self):
        question_content = []
        for question in self.questions.order_by('ask_date'):
            question_dict = {
                "first_name": question.author_first_name, 
                "last_name": question.author_last_name,
                "email": question.author_email,
                "question_content": question.description,
                "id": question.id,
            }
            question_content.append(question_dict)
        return question_content

    def __str__(self):
        return self.name

    def updateTime(self):
        s = str(self.times_open)
        curr_time_zone = pytz.timezone(settings.QUEUE_TIME_ZONE)
        today = datetime.datetime.now(curr_time_zone)        
        current_weekday = today.weekday()
        if current_weekday == 0:
            # get string between "Monday" and "Tuesday"
            s = s[s.index("Monday"):]
            s = s[:s.index(" Tuesday")]
        elif current_weekday == 1:
            # get string between "Tuesday" and "Wednesday"
            s = s[s.index("Tuesday"):]
            s = s[:s.index(" Wednesday")]
        elif current_weekday == 2:
            # get string between "Wednesday" and "Thursday"
            s = s[s.index("Wednesday"):]
            s = s[:s.index(" Thursday")]
        elif current_weekday == 3:
            # get string between "Thursday" and "Friday"
            s = s[s.index("Thursday"):]
            s = s[:s.index(" Friday")]
        elif current_weekday == 4:
            # get string between "Friday" and "Saturday"
            s = s[s.index("Friday"):]
            s = s[:s.index(" Saturday")]
        elif current_weekday == 5:
            # get string between "Saturday" and "Sunday"
            s = s[s.index("Saturday"):]
            s = s[:s.index(" Sunday")]
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
            if (current_hour > start_time_int_hour and current_hour < end_time_int_hour):
                isValidTime = True
                break
            else:
                if current_hour == start_time_int_hour:
                    if current_minute >= start_time_int_minute:
                        isValidTime = True
                        break
                elif current_hour == end_time_int_hour:
                    if (current_minute <= end_time_int_minute):
                        isValidTime = True
                        break
        if self.is_in_time != isValidTime:
            self.is_in_time = isValidTime
            self.save()
        return True

    # takes in the current time and the times specified by the OHqueue and sees if it is active 
    def isQueueActive(self):

        if self.is_open_extended: 
            return True
        
        if self.is_closed:
            return False

        s = str(self.times_open)
        curr_time_zone = pytz.timezone(settings.QUEUE_TIME_ZONE)
        today = datetime.datetime.now(curr_time_zone)        
        current_weekday = today.weekday()
        if current_weekday == 0:
            # get string between "Monday" and "Tuesday"
            s = s[s.index("Monday"):]
            s = s[:s.index(" Tuesday")]
        elif current_weekday == 1:
            # get string between "Tuesday" and "Wednesday"
            s = s[s.index("Tuesday"):]
            s = s[:s.index(" Wednesday")]
        elif current_weekday == 2:
            # get string between "Wednesday" and "Thursday"
            s = s[s.index("Wednesday"):]
            s = s[:s.index(" Thursday")]
        elif current_weekday == 3:
            # get string between "Thursday" and "Friday"
            s = s[s.index("Thursday"):]
            s = s[:s.index(" Friday")]
        elif current_weekday == 4:
            # get string between "Friday" and "Saturday"
            s = s[s.index("Friday"):]
            s = s[:s.index(" Saturday")]
        elif current_weekday == 5:
            # get string between "Saturday" and "Sunday"
            s = s[s.index("Saturday"):]
            s = s[:s.index(" Sunday")]
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
            if "-" in time_slot:
                start_time = time_slot.split("-")[0]
                end_time = time_slot.split("-")[1]
                start_time_int_hour = int((datetime.datetime.strptime(start_time, '%I:%M%p')).strftime("%H"))
                end_time_int_hour = int((datetime.datetime.strptime(end_time, '%I:%M%p')).strftime("%H"))
                start_time_int_minute = int((datetime.datetime.strptime(start_time, '%I:%M%p')).strftime("%M"))
                end_time_int_minute = int((datetime.datetime.strptime(end_time, '%I:%M%p')).strftime("%M"))
                if (current_hour > start_time_int_hour and current_hour < end_time_int_hour):
                    isValidTime = True
                    break
                else:
                    if current_hour == start_time_int_hour:
                        if current_minute >= start_time_int_minute:
                            isValidTime = True
                            break
                    elif current_hour == end_time_int_hour:
                        if (current_minute <= end_time_int_minute):
                            isValidTime = True
                            break
        if self.is_in_time != isValidTime:
            self.is_in_time = isValidTime
            self.save()
        return isValidTime
