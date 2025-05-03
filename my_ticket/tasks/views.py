from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render, redirect
from .models import Action, Context, Project, State, Task, TaskType
from .forms import ActionForm, ContextForm, ProjectForm, StateForm, TaskForm, TaskTypeForm


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

    return render(request, 'tasks/actions/list_actions.html', {'page_obj': page_obj, 'query': query})


def action_create(request):
    if request.method == "POST":
        form = ActionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('action_list')
    else:
        form = ActionForm()
    return render(request, 'tasks/actions/new_action.html', {'form': form})


def action_delete(request, action_id):
    action = get_object_or_404(Action, id=action_id)

    if request.method == 'POST':
        action.delete()
        return redirect('action_list')

    return render(request, 'tasks/actions/delete_action.html', {'action': action})


def action_update(request, action_id):
    action = get_object_or_404(Action, id=action_id)

    if request.method == "POST":
        form = ActionForm(request.POST, instance=action)
        if form.is_valid():
            form.save()
            return redirect('action_list')
    else:
        form = ActionForm(instance=action)

    return render(request, 'tasks/actions/update_action.html', {'form': form, 'action': action})


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
    return render(request, 'tasks/contexts/new_context.html', {'form': form})


def context_delete(request, context_id):
    context = get_object_or_404(Context, id=context_id)

    if request.method == 'POST':
        context.delete()
        return redirect('context_list')

    return render(request, 'tasks/contexts/delete_context.html', {'context': context})


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
