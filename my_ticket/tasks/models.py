from django.contrib.postgres.fields import ArrayField
from django.db import models
from contacts.models import Address, ContextContact
import datetime


class Action(models.Model):
    name = models.CharField(max_length=255)


class Context(models.Model):
    name = models.CharField(max_length=255)


class Cycle(models.Model):
    LEVELS = [('day', 'Dag'), ('week', 'Week'), ('month', 'Maand'), ('year', 'Jaar')]
    WEEKDAYS = [('Monday', 'maandag'), ('Tuesday', 'dinsdag'), ('Wednesday', 'woensdag'), ('Thursday', 'donderdag'), ('Friday', 'vrijdag'), ('Saturday', 'zaterdag'), ('Sunday', 'zondag')]
    MONTHS = [('January', 'januari'), ('February', 'februari'), ('March', 'maart'), ('April', 'april'), ('May', 'mei'), ('June', 'juni'), ('July', 'juli'), ('August', 'augustus'), ('September', 'september'), ('October', 'oktober'), ('November', 'november'), ('December', 'december')]
    level = ArrayField(models.CharField(max_length=50, choices=LEVELS), blank=True, default=list)
    weekday = ArrayField(models.CharField(max_length=50, choices=WEEKDAYS), blank=True, default=list)
    month = ArrayField(models.CharField(max_length=50, choices=MONTHS), blank=True, default=list)
    cycle_distance = models.IntegerField()
    days_of_level = ArrayField(
        base_field=models.IntegerField(),
        blank=True,
        default=list
    )
    start = models.DateTimeField()
    end = models.DateTimeField()


class State(models.Model):
    name = models.CharField(max_length=255)


class Tag(models.Model):
    name = models.CharField(max_length=255)


class Type(models.Model):
    name = models.CharField(max_length=255)


class MeetingRoom(models.Model):
    name = models.CharField()
    capacity = models.IntegerField()


class Meeting(models.Model):
    name = models.CharField()
    date = models.DateTimeField()
    contacts = models.ManyToManyField(ContextContact, through='MeetingContextContact')
    meetingroom = models.ForeignKey(MeetingRoom, on_delete=models.CASCADE)
    digital_space = models.URLField()


class MeetingAcceptance(models.Model):
    name = models.CharField()


class MeetingContextContact(models.Model):
    contextcontact = models.ForeignKey(ContextContact, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    status = models.ForeignKey(MeetingAcceptance, on_delete=models.CASCADE)


class Project(models.Model):
    name = models.CharField(max_length=255)
    startdate = models.DateField()
    enddate = models.DateField()
    total_projected_time_internal = models.TimeField
    total_projected_time_external = models.TimeField


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
    duration_registered = models.TimeField(blank=True, null=True)
    duration_projected_internal = models.TimeField(blank=True, null=True)
    duration_projected_external = models.TimeField(blank=True, null=True)

    deadline = models.DateTimeField(blank=True, null=True)

    cycle_group = models.ForeignKey(Cycle, on_delete=models.CASCADE, blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='tasks', blank=True)

    location = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    meetings = models.ManyToManyField(Meeting, related_name='tasks', blank=True)

    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subtasks')
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='unlocks')

    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    context = models.ForeignKey(Context, on_delete=models.CASCADE, blank=True, null=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, blank=True, null=True)

    attachment = models.FileField(blank=True, null=True)
    git_branch = models.CharField(max_length=255, blank=True)
