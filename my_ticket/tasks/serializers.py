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
    meetingroom_name = serializers.CharField(source='meetingroom.name', read_only=True)
    contacts = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=ContextContact.objects.all(),
        required=False
    )

    class Meta:
        model = Meeting
        fields = ['id', 'name', 'startdate', 'enddate', 'contacts', 'digital_space', 'meetingroom', 'meetingroom_name']

    def create(self, validated_data):
        print(f"Validated data in create: {validated_data}")

        contacts_data = validated_data.pop('contacts', [])
        print(f"Contacts data: {contacts_data}")

        # Create the meeting without contacts first
        meeting = Meeting.objects.create(**validated_data)
        print(f"Created meeting: {meeting.id}")

        # Handle the through table manually
        if contacts_data:
            for contact in contacts_data:
                MeetingContextContact.objects.create(
                    meeting=meeting,
                    contextcontact=contact  # Use the correct field name from your through model
                )
            print(f"Created {len(contacts_data)} contact relationships")

        return meeting

    def update(self, instance, validated_data):
        print(f"Validated data in update: {validated_data}")

        contacts_data = validated_data.pop('contacts', None)
        print(f"Contacts data for update: {contacts_data}")

        # Update regular fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handle contacts update through the through table
        if contacts_data is not None:
            # Delete existing relationships
            MeetingContextContact.objects.filter(meeting=instance).delete()

            # Create new relationships
            for contact in contacts_data:
                MeetingContextContact.objects.create(
                    meeting=instance,
                    contextcontact=contact  # Use the correct field name
                )
            print(f"Updated with {len(contacts_data)} contact relationships")

        return instance

    def to_representation(self, instance):
        """Customize the output to include contact details if needed"""
        representation = super().to_representation(instance)

        # Get contacts through the through table
        meeting_contacts = MeetingContextContact.objects.filter(meeting=instance)
        contact_ids = [mc.contextcontact.id for mc in meeting_contacts]
        representation['contacts'] = contact_ids

        return representation


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    contextcontact_name = serializers.SerializerMethodField()

    def get_contextcontact_name(self, obj):
        if obj.assignment and obj.assignment.contact:
            firstname = obj.assignment.contact.firstname or ""
            lastname = obj.assignment.contact.lastname or ""
            function = obj.assignment.function or "onbekend"
            return f"{firstname} {lastname} ({function})".strip()
        return ""

    class Meta:
        model = Task
        fields = '__all__'

class CycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cycle
        fields = '__all__'
