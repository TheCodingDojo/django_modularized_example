from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.urls import reverse

from task_manager.models.user import User


@require_http_methods(["GET"])
def login_register(request):
    return render(request, 'task_manager/users/login_register.html')


@require_http_methods(["GET"])
def all(request):
    return render(request, 'task_manager/users/all.html')


@require_http_methods(["POST"])
def login(request):
    user = User.objects.attempt_login(request)

    if user is None:
        return HttpResponseRedirect(reverse('users_login_register'))

    return HttpResponseRedirect(reverse('users_dashboard'))


@require_http_methods(["POST"])
def register(request):
    new_user = User.objects.register(request)

    if new_user is None:
        return HttpResponseRedirect(reverse('users_login_register'))

    return HttpResponseRedirect(reverse('users_dashboard'))


@require_http_methods(["GET"])
def dashboard(request):
    user = User.objects.get_logged_in_user(request)

    if user is None:
        return HttpResponseRedirect(reverse('users_login_register'))

    context = {
        'logged_user': user,
        'rows': [
            {
                'heading': 'Assigned Tasks',
                'cols': [
                    {
                        'heading': 'Incompleted Tasks',
                        'filtered_tasks': user.assigned_tasks.filter(
                            is_complete=False).order_by('due_date').all(),
                    },
                    {
                        'heading': 'Completed Tasks',
                        'filtered_tasks': user.assigned_tasks.filter(
                            is_complete=True).order_by('due_date').all(),
                    }
                ]
            },
            {
                'heading': 'Delegated Tasks',
                'cols': [
                    {
                        'heading': 'Incompleted Tasks',
                        'filtered_tasks': user.created_tasks.exclude(
                            assigned_to=user).filter(
                            is_complete=False).order_by('due_date').all(),
                    },
                    {
                        'heading': 'Completed Tasks',
                        'filtered_tasks': user.created_tasks.exclude(
                            assigned_to=user).filter(
                            is_complete=True).order_by('due_date').all(),
                    }
                ]
            },
        ]
    }

    return render(request, 'task_manager/users/dashboard.html', context)


@require_http_methods(["GET"])
def logout(request):
    request.session.clear()
    return HttpResponseRedirect(reverse('users_login_register'))
