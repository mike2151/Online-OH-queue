from django.db import models
from questions.models import Question
import datetime
import os
import pytz
from django.utils.timezone import activate
from time import strftime

# Create your models here.
class OHQueue(models.Model):
    name = models.CharField(max_length=32, unique=True)
    questions = models.ManyToManyField(Question, blank=True)
    is_open_extended = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    is_in_time = models.BooleanField(default=False)
    # scheduling
    monday_times = models.CharField(max_length=50, default="", blank=True, null=True)
    tuesday_times = models.CharField(max_length=50, default="", blank=True, null=True)
    wednesday_times = models.CharField(max_length=50, default="", blank=True, null=True)
    thursday_times = models.CharField(max_length=50, default="", blank=True, null=True)
    friday_times = models.CharField(max_length=50, default="", blank=True, null=True)
    saturday_times = models.CharField(max_length=50, default="", blank=True, null=True)
    sunday_times = models.CharField(max_length=50, default="", blank=True, null=True)
    # average wait time fields
    average_wait_time = models.FloatField(default=0.0)
    num_questions_answered = models.IntegerField(default=0)
    last_answer_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Office Hours Queue"
        verbose_name_plural = "Office Hours Queues"

    def student_question_contents(self):
        curr_time_zone = pytz.timezone(os.environ.get('QUEUE_TIME_ZONE','America/New_York'))
        question_content = []
        for question in self.questions.order_by('ask_date'):
            question_dict = {
                "first_name": question.author_first_name, 
                "last_name": question.author_last_name,
                "email": question.author_email,
                "id": question.id,
            }
            question_content.append(question_dict)
        return question_content

    def question_contents(self):
        curr_time_zone = pytz.timezone(os.environ.get('QUEUE_TIME_ZONE','America/New_York'))
        question_content = []
        for question in self.questions.order_by('ask_date'):
            question_dict = {
                "first_name": question.author_first_name, 
                "last_name": question.author_last_name,
                "email": question.author_email,
                "student_id": question.author_email.split("@", 1)[0],
                "question_content": question.description,
                "id": question.id,
                "time_asked": question.ask_date.replace(tzinfo=pytz.utc).astimezone(curr_time_zone).strftime('%I:%M %p')
            }
            question_content.append(question_dict)
        return question_content

    def wait_time(self):
        max_wait_time = os.environ.get('MAX_WAIT_TIME', 60.0)
        wait_time = self.average_wait_time * len(self.questions.all())
        return min(wait_time, max_wait_time)

    def __str__(self):
        return self.name

    def updateTime(self):
        s = ""
        curr_time_zone = pytz.timezone(os.environ.get('QUEUE_TIME_ZONE','America/New_York'))
        today = datetime.datetime.now(curr_time_zone)        
        current_weekday = today.weekday()
        if current_weekday == 0:
            s = self.monday_times
        elif current_weekday == 1:
            s = self.tuesday_times
        elif current_weekday == 2:
            s = self.wednesday_times
        elif current_weekday == 3:
            s = self.thursday_times
        elif current_weekday == 4:
            s = self.friday_times
        elif current_weekday == 5:
            s = self.saturday_times
        elif current_weekday == 6:
            s = self.sunday_times
        s = s.replace(" ", "")
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
    def isQueueActive(self, user):

        if user != None:
            for question in self.questions.all():
                if question.author_email == user.email:
                    return True

        if self.is_open_extended: 
            return True
        
        if self.is_closed:
            return False

        s = ""
        curr_time_zone = pytz.timezone(os.environ.get('QUEUE_TIME_ZONE','America/New_York'))
        today = datetime.datetime.now(curr_time_zone)        
        current_weekday = today.weekday()
        if current_weekday == 0:
            s = self.monday_times
        elif current_weekday == 1:
            s = self.tuesday_times
        elif current_weekday == 2:
            s = self.wednesday_times
        elif current_weekday == 3:
            s = self.thursday_times
        elif current_weekday == 4:
            s = self.friday_times
        elif current_weekday == 5:
            s = self.saturday_times
        elif current_weekday == 6:
            s = self.sunday_times
        s = s.replace(" ", "")
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
