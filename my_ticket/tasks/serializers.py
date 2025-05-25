from rest_framework import serializers
from .models import (
    Action, Context, State, Tag, TaskType, MeetingRoom, Meeting,
    MeetingAcceptance, MeetingContextContact, Project, Task, Cycle
)
from contacts.models import Address, ContextContact


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'


class ContextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Context
        fields = '__all__'


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class TaskTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskType
        fields = '__all__'


class MeetingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRoom
        fields = '__all__'


class MeetingAcceptanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingAcceptance
        fields = '__all__'


class ContextContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContextContact
        fields = '__all__'


class MeetingContextContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingContextContact
        fields = '__all__'


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class CycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cycle
        fields = '__all__'
