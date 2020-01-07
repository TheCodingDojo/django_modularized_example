from django.urls import path
from . import views

urlpatterns = [
    path('', views.users.login_register, name='users_login_register'),
    path('users/login', views.users.login, name='users_login'),
    path('users/register', views.users.register, name='users_register'),
    path('users/dashboard', views.users.dashboard, name='users_dashboard'),
    path('users/all', views.users.all, name='users_all'),
    path('users/logout', views.users.logout, name='users_logout'),

    path('tasks/all', views.tasks.all, name='tasks_all'),
    path('tasks/new', views.tasks.new, name='tasks_new'),
    path('tasks/create', views.tasks.create, name='tasks_create'),
    path('tasks/<int:task_id>/edit', views.tasks.edit, name='tasks_edit'),
    path('tasks/<int:task_id>/details',
         views.tasks.details, name='tasks_details'),
    path(
        'tasks/<int:task_id>/delete',
        views.tasks.delete,
        name='tasks_delete'),
    path(
        'tasks/<int:task_id>/toggle',
        views.tasks.toggle_completed,
        name='tasks_toggle_completed'),
]
