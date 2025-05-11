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
    source_task = models.ForeignKey(Task, on_delete=models.DO_NOTHING, blank=True, null=True)
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

    def get_repeating_dates(self):
        if not self.start or not self.end:
            return []

        if not self.cycle_model or self.cycle_model != 'each':
            return []

        if not self.one_level or not self.one_level:
            return []

        step = self.one_level
        current = self.start
        dates = []

        while current <= self.end:
            dates.append(current)

            if step == 'day':
                current += relativedelta(days=1)
            elif step == 'week':
                current += relativedelta(weeks=1)
            elif step == 'month':
                current += relativedelta(months=1)
            elif step == 'year':
                current += relativedelta(years=1)
            else:
                break

        return dates
