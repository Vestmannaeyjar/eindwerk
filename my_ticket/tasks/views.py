from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from .models import Action, Context, Meeting, MeetingAcceptance, MeetingContextContact, MeetingRoom, Project, State, Tag, Task, TaskType
from .forms import ActionForm, ContextForm, CycleForm, MeetingForm, MeetingAcceptanceForm, MeetingContextContactForm, MeetingRoomForm, ProjectForm, StateForm, TagForm, TaskForm, TaskTypeForm


def action_list(request):
    query = request.GET.get('q')
    actions = Action.objects.all()

    if query:
        actions = actions.filter(
            Q(name__icontains=query)
        )

    paginator = Paginator(actions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tasks/actions/list_tags.html', {'page_obj': page_obj, 'query': query})


def action_create(request):
    if request.method == "POST":
        form = ActionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('action_list')
    else:
        form = ActionForm()
    return render(request, 'tasks/actions/new_tag.html', {'form': form})


def action_delete(request, action_id):
    action = get_object_or_404(Action, id=action_id)

    if request.method == 'POST':
        action.delete()
        return redirect('action_list')

    return render(request, 'tasks/actions/delete_tag.html', {'action': action})


def action_update(request, action_id):
    action = get_object_or_404(Action, id=action_id)

    if request.method == "POST":
        form = ActionForm(request.POST, instance=action)
        if form.is_valid():
            form.save()
            return redirect('action_list')
    else:
        form = ActionForm(instance=action)

    return render(request, 'tasks/actions/update_tag.html', {'form': form, 'action': action})


def context_list(request):
    query = request.GET.get('q')
    contexts = Context.objects.all()

    if query:
        contexts = contexts.filter(
            Q(name__icontains=query)
        )

    paginator = Paginator(contexts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tasks/contexts/list_contexts.html', {'page_obj': page_obj, 'query': query})


def context_create(request):
    if request.method == "POST":
        form = ContextForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('context_list')
    else:
        form = ContextForm()
    return render(request, 'tasks/contexts/new_cycle.html', {'form': form})


def cycle_create(request):
    if request.method == "POST":
        form = CycleForm(request.POST)
        print("POST received")
        if form.is_valid():
            cycle = form.save()
            print("Form is valid, cycle saved.")
            print("Cycle model:", cycle.cycle_model)
            print("Start:", cycle.start, "End:", cycle.end)

            dates = cycle.get_repeating_dates()
            print("Generated dates:", dates)
            return HttpResponse(f"Dates: {dates}")
        else:
            print("Form is **NOT** valid")
            print("Form errors:", form.errors.as_json())  # JSON is clearer for nested fields
            return HttpResponse(f"Form errors: {form.errors.as_json()}")
    else:
        form = CycleForm()
        print("GET request - showing empty form")

    return render(request, 'tasks/cycles/new_cycle.html', {'form': form})


def context_delete(request, context_id):
    context = get_object_or_404(Context, id=context_id)

    if request.method == 'POST':
        context.delete()
        return redirect('context_list')

    return render(request, 'tasks/contexts/delete_cycle.html', {'context': context})


def context_update(request, context_id):
    context = get_object_or_404(Context, id=context_id)

    if request.method == "POST":
        form = ContextForm(request.POST, instance=context)
        if form.is_valid():
            form.save()
            return redirect('context_list')
    else:
        form = ContextForm(instance=context)

    return render(request, 'tasks/contexts/update_context.html', {'form': form, 'context': context})


def meeting_list(request):
    query = request.GET.get('q')
    meetings = Meeting.objects.all()

    if query:
        meetings = meetings.filter(
            Q(name__icontains=query)
        )

    paginator = Paginator(meetings, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tasks/meetings/list_meetings.html', {'page_obj': page_obj, 'query': query})


def meeting_create(request):
    if request.method == "POST":
        form = MeetingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('meeting_list')
    else:
        form = MeetingForm()
    return render(request, 'tasks/meetings/new_meeting.html', {'form': form})


def meeting_delete(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)

    if request.method == 'POST':
        meeting.delete()
        return redirect('meeting_list')

    return render(request, 'tasks/meetings/delete_meeting.html', {'meeting': meeting})


def meeting_update(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)

    if request.method == "POST":
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            form.save()
            return redirect('meeting_list')
    else:
        form = MeetingForm(instance=meeting)

    return render(request, 'tasks/meetings/update_meeting.html', {'form': form, 'meeting': meeting})


def meetingacceptance_list(request):
    query = request.GET.get('q')
    meetingacceptances = MeetingAcceptance.objects.all()

    if query:
        meetingacceptances = meetingacceptances.filter(
            Q(name__icontains=query)
        )

    paginator = Paginator(meetingacceptances, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tasks/meetingacceptances/list_meetingacceptances.html', {'page_obj': page_obj, 'query': query})


def meetingacceptance_create(request):
    if request.method == "POST":
        form = MeetingAcceptanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('meetingacceptance_list')
    else:
        form = MeetingAcceptanceForm()
    return render(request, 'tasks/meetingacceptances/new_meetingacceptance.html', {'form': form})


def meetingacceptance_delete(request, meetingacceptance_id):
    meetingacceptance = get_object_or_404(MeetingAcceptance, id=meetingacceptance_id)

    if request.method == 'POST':
        meetingacceptance.delete()
        return redirect('meetingacceptance_list')

    return render(request, 'tasks/meetingacceptances/delete_meetingacceptance.html', {'meetingacceptance': meetingacceptance})


def meetingacceptance_update(request, meetingacceptance_id):
    meetingacceptance = get_object_or_404(MeetingAcceptance, id=meetingacceptance_id)

    if request.method == "POST":
        form = MeetingAcceptanceForm(request.POST, instance=meetingacceptance)
        if form.is_valid():
            form.save()
            return redirect('meetingacceptance_list')
    else:
        form = MeetingAcceptanceForm(instance=meetingacceptance)

    return render(request, 'tasks/meetingacceptances/update_meetingacceptance.html', {'form': form, 'meetingacceptance': meetingacceptance})


def meetingcontextcontact_list(request):
    query = request.GET.get('q')
    meetingcontextcontacts = MeetingContextContact.objects.all()

    if query:
        meetingcontextcontacts = meetingcontextcontacts.filter(
            Q(name__icontains=query)
        )

    paginator = Paginator(meetingcontextcontacts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tasks/meetingcontextcontacts/list_meetingcontextcontacts.html', {'page_obj': page_obj, 'query': query})


def meetingcontextcontact_create(request):
    if request.method == "POST":
        form = MeetingContextContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('meetingcontextcontact_list')
    else:
        form = MeetingContextContactForm()
    return render(request, 'tasks/meetingcontextcontacts/new_meetingcontextcontact.html', {'form': form})


def meetingcontextcontact_delete(request, meetingcontextcontact_id):
    meetingcontextcontact = get_object_or_404(MeetingContextContact, id=meetingcontextcontact_id)

    if request.method == 'POST':
        meetingcontextcontact.delete()
        return redirect('meetingcontextcontact_list')

    return render(request, 'tasks/meetingcontextcontacts/delete_meetingcontextcontact.html', {'meetingcontextcontact': meetingcontextcontact})


def meetingcontextcontact_update(request, meetingcontextcontact_id):
    meetingcontextcontact = get_object_or_404(MeetingContextContact, id=meetingcontextcontact_id)

    if request.method == "POST":
        form = MeetingContextContactForm(request.POST, instance=meetingcontextcontact)
        if form.is_valid():
            form.save()
            return redirect('meetingcontextcontact_list')
    else:
        form = MeetingContextContactForm(instance=meetingcontextcontact)

    return render(request, 'tasks/meetingcontextcontacts/update_meetingcontextcontact.html', {'form': form, 'meetingcontextcontact': meetingcontextcontact})


def meetingroom_list(request):
    query = request.GET.get('q')
    meetingrooms = MeetingRoom.objects.all()

    if query:
        meetingrooms = meetingrooms.filter(
            Q(name__icontains=query)
        )

    paginator = Paginator(meetingrooms, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tasks/meetingrooms/list_meetings.html', {'page_obj': page_obj, 'query': query})


def meetingroom_create(request):
    if request.method == "POST":
        form = MeetingRoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('meetingroom_list')
    else:
        form = MeetingRoomForm()
    return render(request, 'tasks/meetingrooms/new_meeting.html', {'form': form})


def meetingroom_delete(request, meetingroom_id):
    meetingroom = get_object_or_404(MeetingRoom, id=meetingroom_id)

    if request.method == 'POST':
        meetingroom.delete()
        return redirect('meetingroom_list')

    return render(request, 'tasks/meetingrooms/delete_meetingroom.html', {'meetingroom': meetingroom})


def meetingroom_update(request, meetingroom_id):
    meetingroom = get_object_or_404(MeetingRoom, id=meetingroom_id)

    if request.method == "POST":
        form = MeetingRoomForm(request.POST, instance=meetingroom)
        if form.is_valid():
            form.save()
            return redirect('meetingroom_list')
    else:
        form = MeetingRoomForm(instance=meetingroom)

    return render(request, 'tasks/meetingrooms/update_meeting.html', {'form': form, 'meetingroom': meetingroom})


def project_list(request):
    query = request.GET.get('q')
    projects = Project.objects.all()

    if query:
        projects = projects.filter(
            Q(name__icontains=query)
        )

    paginator = Paginator(projects, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tasks/projects/list_projects.html', {'page_obj': page_obj, 'query': query})


def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'tasks/projects/new_project.html', {'form': form})


def project_delete(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        project.delete()
        return redirect('project_list')

    return render(request, 'tasks/projects/delete_project.html', {'project': project})


def project_update(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'tasks/projects/update_project.html', {'form': form, 'project': project})


def state_list(request):
    query = request.GET.get('q')
    states = State.objects.all()

    if query:
        states = states.filter(
            Q(name__icontains=query)
        )

    paginator = Paginator(states, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tasks/states/list_states.html', {'page_obj': page_obj, 'query': query})


def state_create(request):
    if request.method == "POST":
        form = StateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('state_list')
    else:
        form = StateForm()
    return render(request, 'tasks/states/new_state.html', {'form': form})


def state_delete(request, state_id):
    state = get_object_or_404(State, id=state_id)

    if request.method == 'POST':
        state.delete()
        return redirect('state_list')

    return render(request, 'tasks/states/delete_state.html', {'state': state})


def state_update(request, state_id):
    state = get_object_or_404(State, id=state_id)

    if request.method == "POST":
        form = StateForm(request.POST, instance=state)
        if form.is_valid():
            form.save()
            return redirect('state_list')
    else:
        form = StateForm(instance=state)

    return render(request, 'tasks/states/update_state.html', {'form': form, 'state': state})


def tag_list(request):
    query = request.GET.get('q')
    tags = Tag.objects.all()

    if query:
        tags = tags.filter(
            Q(name__icontains=query)
        )

    paginator = Paginator(tags, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tasks/tags/list_tags.html', {'page_obj': page_obj, 'query': query})


def tag_create(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tag_list')
    else:
        form = TagForm()
    return render(request, 'tasks/tags/new_tag.html', {'form': form})


def tag_delete(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)

    if request.method == 'POST':
        tag.delete()
        return redirect('tag_list')

    return render(request, 'tasks/tags/delete_tag.html', {'tag': tag})


def tag_update(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)

    if request.method == "POST":
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return redirect('tag_list')
    else:
        form = TagForm(instance=tag)

    return render(request, 'tasks/tags/update_tag.html', {'form': form, 'tag': tag})


def task_list(request):
    query = request.GET.get('q')
    tasks = Task.objects.all()

    if query:
        tasks = tasks.filter(
            Q(name__icontains=query) | Q(subject__icontains=query) | Q(action__icontains=query)
        )

    paginator = Paginator(tasks, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tasks/list.html', {'page_obj': page_obj, 'query': query})


def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/new.html', {'form': form})


def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.delete()
        return redirect('task_list')

    return render(request, 'tasks/delete.html', {'task': task})


def task_update(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/update.html', {'form': form, 'task': task})


def tasktype_list(request):
    query = request.GET.get('q')
    tasktypes = TaskType.objects.all()

    if query:
        tasktypes = tasktypes.filter(
            Q(name__icontains=query)
        )

    paginator = Paginator(tasktypes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tasks/tasktypes/list_tasktypes.html', {'page_obj': page_obj, 'query': query})


def tasktype_create(request):
    if request.method == "POST":
        form = TaskTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasktype_list')
    else:
        form = TaskTypeForm()
    return render(request, 'tasks/tasktypes/new_tasktype.html', {'form': form})


def tasktype_delete(request, tasktype_id):
    tasktype = get_object_or_404(TaskType, id=tasktype_id)

    if request.method == 'POST':
        tasktype.delete()
        return redirect('tasktype_list')

    return render(request, 'tasks/tasktypes/delete_tasktype.html', {'type': type})


def tasktype_update(request, tasktype_id):
    tasktype = get_object_or_404(TaskType, id=tasktype_id)

    if request.method == "POST":
        form = TaskTypeForm(request.POST, instance=tasktype)
        if form.is_valid():
            form.save()
            return redirect('tasktype_list')
    else:
        form = TaskTypeForm(instance=tasktype)

    return render(request, 'tasks/tasktypes/update_tasktype.html', {'form': form, 'tasktype': tasktype})
