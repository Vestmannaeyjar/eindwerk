from django.contrib.postgres.fields import ArrayField
from django.db import models
from contacts.models import Address, ContextContact


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
    assignment = models.ForeignKey(ContextContact, on_delete=models.CASCADE)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    execution_startdate = models.DateField()
    execution_starttime = models.TimeField()
    execution_enddate = models.DateField()
    execution_endtime = models.TimeField()
    full_days = models.BooleanField()
    duration_registered = models.TimeField()
    duration_projected_internal = models.TimeField()
    duration_projected_external = models.TimeField()
    deadline = models.DateTimeField()
    cycle_group = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='tasks')
    location = models.ForeignKey(Address, on_delete=models.CASCADE)
    meetings = models.ManyToManyField(Meeting, related_name='tasks')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subtasks')
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='unlocks')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    context = models.ForeignKey(Context, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    attachment = models.FileField()
    git_branch = models.CharField(max_length=255)
