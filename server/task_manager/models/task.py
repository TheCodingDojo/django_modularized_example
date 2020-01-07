from datetime import datetime

from django.db import models
from django.contrib import messages
from django.contrib.messages import get_messages

from .user import User
from .tag import Tag


class TaskManager(models.Manager):
    def create_task(self, request):
        new_task = None
        tag_errors = False

        logged_in_user = User.objects.get_logged_in_user(request)

        if logged_in_user is None:
            messages.error(request, "Must be logged in.")

        if len(request.POST['title']) < 2:
            messages.error(request, "Title must be at least 2 characters.")

        due = datetime.strptime(request.POST['due_date'], "%Y-%m-%dT%H:%M")

        if due < datetime.now():
            messages.error(request, 'Due date must be in the future.')

        assigned_to = User.objects.filter(
            id=request.POST['assigned_to']).first()

        if assigned_to is None:
            messages.error(request, "Assigned user not found.")

        error_messages = messages.get_messages(request)
        error_messages.used = False  # don't clear messages

        if not error_messages:
            new_task = Task(
                title=request.POST['title'],
                description=request.POST['description'],
                due_date=request.POST['due_date'],
                created_by=logged_in_user,
                assigned_to=assigned_to
            )

            new_task.save()
            tag_errors = self.add_tags(request, new_task)

        return new_task, tag_errors

    def add_tags(self, request, task):
        tags = request.POST['tags'].split(",")
        errors = False

        if not tags:
            return False

        for tag_name in tags:
            tag_name = tag_name.strip()

            tag_to_add = None
            existing_tag = Tag.objects.filter(name=tag_name).first()

            if existing_tag:
                tag_to_add = existing_tag
            else:
                tag_to_add = Tag.objects.create_tag(tag_name, request)

                if tag_to_add is None:
                    errors = True

            task.tags.add(tag_to_add)

        return errors

    def toggle_completed(self, request, task_id):
        task = Task.objects.filter(id=task_id).first()

        if task is not None:
            uid = request.session.get('user_id')

            if task.created_by.id == uid or task.assigned_to.id == uid:
                task.is_complete = not task.is_complete

                if task.is_complete:
                    task.completed_at = datetime.now()
                else:
                    task.completed_at = None

                task.save()

    def delete(self, request, task_id):
        uid = request.session.get('user_id')
        task = Task.objects.filter(id=task_id).first()

        if task and task.created_by.id == uid:
            task.delete()
            return True
        return False


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    is_complete = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # When a User is deleted
    # the delete will 'cascade' to delete all the user's created_tasks as well
    created_by = models.ForeignKey(
        User, related_name="created_tasks", on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(
        User, related_name="assigned_tasks", on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name="tasks")
    objects = TaskManager()
