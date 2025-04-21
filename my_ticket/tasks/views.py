from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render, redirect
from .models import Task
from .forms import TaskForm


def task_list(request):
    query = request.GET.get('q')  # 'q' is the name of the input field in the form
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
