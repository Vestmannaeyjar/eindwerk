from django.contrib.postgres.fields import ArrayField
from django.db import models
from contacts.models import Address, ContextContact
from dateutil.relativedelta import relativedelta


class Action(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class Context(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class State(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class TaskType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class MeetingRoom(models.Model):
    name = models.CharField()
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.name}"


class Meeting(models.Model):
    name = models.CharField()
    date = models.DateTimeField()
    contacts = models.ManyToManyField(ContextContact, through='MeetingContextContact')
    meetingroom = models.ForeignKey(MeetingRoom, on_delete=models.CASCADE)
    digital_space = models.URLField()

    def __str__(self):
        return f"{self.date} {self.name} {self.meetingroom}"


class MeetingAcceptance(models.Model):
    name = models.CharField()

    def __str__(self):
        return f"{self.name}"


class MeetingContextContact(models.Model):
    contextcontact = models.ForeignKey(ContextContact, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    status = models.ForeignKey(MeetingAcceptance, on_delete=models.CASCADE)


class Project(models.Model):
    name = models.CharField(max_length=255)
    startdate = models.DateField()
    enddate = models.DateField()
    total_projected_time_internal = models.TimeField(default="00:00.000")
    total_projected_time_external = models.TimeField(default="00:00.000")

    def __str__(self):
        return f"{self.name} {self.startdate} - {self.enddate}"


class Task(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    assignment = models.ForeignKey(ContextContact, on_delete=models.CASCADE, blank=True, null=True)
    action = models.ForeignKey(Action, on_delete=models.CASCADE, blank=True, null=True)

    subject = models.CharField(max_length=255)

    execution_startdate = models.DateField(blank=True, null=True)
    execution_starttime = models.TimeField(blank=True, null=True)
    execution_enddate = models.DateField(blank=True, null=True)
    execution_endtime = models.TimeField(blank=True, null=True)

    full_days = models.BooleanField(blank=True, default=False)
    duration_registered = models.DurationField(blank=True, null=True)
    duration_projected_internal = models.DurationField(blank=True, null=True)
    duration_projected_external = models.DurationField(blank=True, null=True)

    deadline = models.DateTimeField(blank=True, null=True)

    cycle_group = models.IntegerField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='tasks', blank=True)

    location = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    meetings = models.ManyToManyField(Meeting, related_name='tasks', blank=True)

    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subtasks')
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='unlocks')

    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    context = models.ForeignKey(Context, on_delete=models.CASCADE, blank=True, null=True)
    tasktype = models.ForeignKey(TaskType, on_delete=models.CASCADE, blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, blank=True, null=True)

    attachment = models.FileField(blank=True, null=True)
    git_branch = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.subject}"


class Cycle(models.Model):
    source_task = models.ForeignKey(Task, on_delete=models.SET_NULL, blank=True, null=True)
    start = models.DateField()
    end = models.DateField()
    MODELS = [('each', 'elke'), ('every', 'om de'), ('dayofweek', 'dag(en) van de week'), ('monthsofyear', 'maand(en) van het jaar'), ('firstlastof', 'eerste/laatste van'), ('dayofmonth', 'dag van de maand')]
    cycle_model = models.CharField(max_length=50, choices=MODELS, blank=True, default='')
    number = models.IntegerField()
    ONE_LEVEL = [('day', 'dag'), ('week', 'week'), ('month', 'maand'), ('year', 'jaar')]
    LEVELS = [('days', 'dagen'), ('weeks', 'weken'), ('months', 'maanden'), ('years', 'jaren')]
    WEEKDAYS = [('Monday', 'maandag'), ('Tuesday', 'dinsdag'), ('Wednesday', 'woensdag'), ('Thursday', 'donderdag'),
                ('Friday', 'vrijdag'), ('Saturday', 'zaterdag'), ('Sunday', 'zondag')]
    MONTHS = [('January', 'januari'), ('February', 'februari'), ('March', 'maart'), ('April', 'april'), ('May', 'mei'),
              ('June', 'juni'), ('July', 'juli'), ('August', 'augustus'), ('September', 'september'),
              ('October', 'oktober'), ('November', 'november'), ('December', 'december')]
    DAYPARTS = [('morning', 'ochtend'), ('afternoon', 'namiddag'), ('evening', 'avond'), ('full', 'volledige dag')]
    level = models.CharField(max_length=50, choices=LEVELS, blank=True, default='')
    one_level = models.CharField(max_length=50, choices=ONE_LEVEL, blank=True, default='')
    weekday = models.CharField(max_length=50, choices=WEEKDAYS, blank=True, default='')
    month = models.CharField(max_length=50, choices=MONTHS, blank=True, default='')

    def each(self):
        step = self.one_level
        date_to_add = self.start
        dates = []

        while date_to_add <= self.end:
            dates.append(date_to_add)

            if step == 'day':
                date_to_add += relativedelta(days=1)
            elif step == 'week':
                date_to_add += relativedelta(weeks=1)
            elif step == 'month':
                date_to_add += relativedelta(months=1)
            elif step == 'year':
                date_to_add += relativedelta(years=1)
            else:
                break

        return dates

    def every(self):
        step_size = self.number
        level = self.level
        date_to_add = self.start
        dates = []

        while date_to_add <= self.end:
            dates.append(date_to_add)

            if level == 'days':
                date_to_add += relativedelta(days=int(step_size))
            elif level == 'weeks':
                date_to_add += relativedelta(weeks=int(step_size))
            elif level == 'months':
                date_to_add += relativedelta(months=int(step_size))
            elif level == 'years':
                date_to_add += relativedelta(years=int(step_size))
            else:
                break

        return dates

    def dayofweek(self):
        date_to_add = self.start
        startdate_weekday = date_to_add.weekday()

        weekday_map = {
            "Monday": 0,
            "Tuesday": 1,
            "Wednesday": 2,
            "Thursday": 3,
            "Friday": 4,
            "Saturday": 5,
            "Sunday": 6
        }

        def get_weekday_number(weekdayword):
            return weekday_map.get(weekdayword, -1)  #

        desired_weekday = get_weekday_number(self.weekday)
        if not startdate_weekday == desired_weekday:
            if desired_weekday < startdate_weekday:
                days_to_add = 7 - (startdate_weekday - desired_weekday)
            else:
                days_to_add = abs(desired_weekday - startdate_weekday)
            date_to_add += relativedelta(days=days_to_add)
        dates = []

        while date_to_add <= self.end:
            dates.append(date_to_add)
            date_to_add += relativedelta(weeks=1)

        return dates

    def get_repeating_dates(self):
        if self.cycle_model == 'each':
            return self.each()
        elif self.cycle_model == 'every':
            return self.every()
        elif self.cycle_model == 'dayofweek':
            return self.dayofweek()
        else:
            return []
