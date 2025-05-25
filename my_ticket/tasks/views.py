from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models.functions import Cast
from django.db.models import CharField

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


class ContextViewSet(viewsets.ModelViewSet):
    queryset = Context.objects.all()
    serializer_class = ContextSerializer


class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TaskTypeViewSet(viewsets.ModelViewSet):
    queryset = TaskType.objects.all()
    serializer_class = TaskTypeSerializer


class MeetingRoomViewSet(viewsets.ModelViewSet):
    queryset = MeetingRoom.objects.all()
    serializer_class = MeetingRoomSerializer


class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get("search")

        if search:
            # Cast date to string to allow partial matching
            queryset = queryset.annotate(
                date_str=Cast("date", CharField())
            )

            filters = (
                    Q(name__icontains=search) |
                    Q(digital_space__icontains=search) |
                    Q(meetingroom__id__icontains=search) |
                    Q(date_str__icontains=search)
            )

            queryset = queryset.filter(filters)

        return queryset


class MeetingAcceptanceViewSet(viewsets.ModelViewSet):
    queryset = MeetingAcceptance.objects.all()
    serializer_class = MeetingAcceptanceSerializer


class MeetingContextContactViewSet(viewsets.ModelViewSet):
    queryset = MeetingContextContact.objects.all()
    serializer_class = MeetingContextContactSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


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
