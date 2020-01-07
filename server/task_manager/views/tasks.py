from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.urls import reverse

from task_manager.models.task import Task
from task_manager.models.user import User


@require_http_methods(["GET"])
def all(request):
    return render(request, 'task_manager/tasks/all.html')


@require_http_methods(["GET"])
def new(request):
    if request.session.get('user_id') is None:
        return HttpResponseRedirect(reverse('users_login_register'))

    context = {
        'users': User.objects.all()
    }
    return render(request, 'task_manager/tasks/new.html', context)


@require_http_methods(["POST"])
def create(request):
    new_task, tag_errors = Task.objects.create_task(request)

    if new_task is None or tag_errors is True:
        return HttpResponseRedirect(reverse('tasks_new'))

    return HttpResponseRedirect(reverse('users_dashboard'))


@require_http_methods(["POST"])
def edit(request, task_id):
    pass


@require_http_methods(["POST"])
def delete(request, task_id):
    Task.objects.delete(request, task_id)
    return HttpResponseRedirect(reverse('users_dashboard'))


@require_http_methods(["GET"])
def details(request, task_id):

    logged_user = User.objects.get_logged_in_user(request)

    if logged_user:
        task = Task.objects.filter(id=task_id).first()

        if task:
            context = {
                'logged_user': logged_user,
                'task': task,
            }
            return render(request, 'task_manager/tasks/details.html', context)

    return HttpResponseRedirect(reverse('users_dashboard'))


@require_http_methods(["POST"])
def toggle_completed(request, task_id):

    Task.objects.toggle_completed(request, task_id)
    return HttpResponseRedirect(reverse('users_dashboard'))
