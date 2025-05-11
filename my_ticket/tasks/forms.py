from django import forms
from django.core.exceptions import ValidationError

from .models import Action, Context, Cycle, Meeting, MeetingAcceptance, MeetingContextContact, MeetingRoom, Project, State, Tag, Task, TaskType


class ActionForm(forms.ModelForm):
    class Meta:
        model = Action
        fields = '__all__'


class ContextForm(forms.ModelForm):
    class Meta:
        model = Context
        fields = '__all__'


class CycleForm(forms.ModelForm):
    level = forms.ChoiceField(
        choices=Cycle.LEVELS,
        widget=forms.Select,
        required=False,
        label="Niveau"
    )
    one_level = forms.ChoiceField(
        choices=Cycle.ONE_LEVEL,
        widget=forms.Select,
        required=False,
        label="Eén niveau"
    )
    cycle_model = forms.ChoiceField(
        choices=Cycle.MODELS,
        widget=forms.Select,
        required=False,
        label="Model"
    )
    weekday = forms.ChoiceField(
        choices=Cycle.WEEKDAYS,
        widget=forms.Select,
        required=False,
        label="Weekdagen"
    )
    month = forms.ChoiceField(
        choices=Cycle.MONTHS,
        widget=forms.Select,
        required=False,
        label="Maanden"
    )

    class Meta:
        model = Cycle
        fields = '__all__'
        widgets = {
            'start': forms.DateInput(attrs={'type': 'date'}),
            'end': forms.DateInput(attrs={'type': 'date'}),
            'weekday': forms.CheckboxSelectMultiple,
            'month': forms.CheckboxSelectMultiple,
        }


class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = '__all__'


class MeetingAcceptanceForm(forms.ModelForm):
    class Meta:
        model = MeetingAcceptance
        fields = '__all__'


class MeetingContextContactForm(forms.ModelForm):
    class Meta:
        model = MeetingContextContact
        fields = '__all__'


class MeetingRoomForm(forms.ModelForm):
    class Meta:
        model = MeetingRoom
        fields = '__all__'


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'


class StateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = '__all__'


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        parent = cleaned_data.get('parent')
        prerequisites = cleaned_data.get('prerequisites', [])
        instance = self.instance

        if parent and prerequisites and parent in prerequisites:
            raise ValidationError("A task's parent cannot also be one of its prerequisites.")

        current = parent
        while current:
            if current == instance:
                raise ValidationError("Cyclic parent relationship detected.")
            current = current.parent

        def has_prerequisite_cycle(task, visited=None):
            if visited is None:
                visited = set()
            if task == instance:
                return True
            if task in visited:
                return False
            visited.add(task)
            for prereq in task.prerequisites.all():
                if has_prerequisite_cycle(prereq, visited):
                    return True
            return False

        for prereq in prerequisites:
            if has_prerequisite_cycle(prereq):
                raise ValidationError("Cyclic prerequisite chain detected.")

        return cleaned_data


class TaskTypeForm(forms.ModelForm):
    class Meta:
        model = TaskType
        fields = '__all__'
