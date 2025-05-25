from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tasks/actions', views.ActionViewSet, basename='action')
router.register(r'tasks/contexts', views.ContextViewSet, basename='context')
router.register(r'tasks/states', views.StateViewSet, basename='state')
router.register(r'tasks/tags', views.TagViewSet, basename='tag')
router.register(r'tasks/tasktypes', views.TaskTypeViewSet, basename='tasktype')

router.register(r'tasks/meetingrooms', views.MeetingRoomViewSet, basename='meetingroom')
router.register(r'tasks/meetings', views.MeetingViewSet, basename='meeting')
router.register(r'tasks/meetingacceptances', views.MeetingAcceptanceViewSet, basename='meetingacceptance')
router.register(r'tasks/meetingcontextcontacts', views.MeetingContextContactViewSet, basename='meetingcontextcontact')

router.register(r'tasks/projects', views.ProjectViewSet, basename='project')
router.register(r'tasks/tasks', views.TaskViewSet, basename='task')
router.register(r'tasks/cycles', views.CycleViewSet, basename='cycle')

urlpatterns = router.urls
