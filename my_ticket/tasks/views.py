from rest_framework import viewsets, filters
from .models import (
    Action, Context, State, Tag, TaskType, MeetingRoom, Meeting,
    MeetingAcceptance, MeetingContextContact, Project, Task, Cycle
)
from .serializers import (
    ActionSerializer, ContextSerializer, StateSerializer, TagSerializer,
    TaskTypeSerializer, MeetingRoomSerializer, MeetingSerializer,
    MeetingAcceptanceSerializer, MeetingContextContactSerializer,
    ProjectSerializer, TaskSerializer, CycleSerializer
)


class ActionViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class ContextViewSet(viewsets.ModelViewSet):
    queryset = Context.objects.all()
    serializer_class = ContextSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class TaskTypeViewSet(viewsets.ModelViewSet):
    queryset = TaskType.objects.all()
    serializer_class = TaskTypeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['subject', 'deadline']


class MeetingRoomViewSet(viewsets.ModelViewSet):
    queryset = MeetingRoom.objects.all()
    serializer_class = MeetingRoomSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'capacity']


class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'date', 'contacts', 'meetingroom', 'digital_space']


class MeetingAcceptanceViewSet(viewsets.ModelViewSet):
    queryset = MeetingAcceptance.objects.all()
    serializer_class = MeetingAcceptanceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class MeetingContextContactViewSet(viewsets.ModelViewSet):
    queryset = MeetingContextContact.objects.all()
    serializer_class = MeetingContextContactSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['contextcontact', 'meeting', 'status']


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'startdate', 'enddate', 'total_projected_time_internal', 'total_projected_time_external']


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["subject", "description"]
    ordering_fields = ["deadline", "subject", "created_at"]
    ordering = ["-deadline"]


class CycleViewSet(viewsets.ModelViewSet):
    queryset = Cycle.objects.all()
    serializer_class = CycleSerializer
