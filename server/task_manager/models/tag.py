from django.db import models
from django.contrib import messages
from django.contrib.messages import get_messages


class TagManager(models.Manager):

    def create_tag(self, tag_name, request):
        new_tag = None

        if self.is_valid(tag_name, request):
            new_tag = Tag(name=tag_name)
            new_tag.save()

        return new_tag

    def is_valid(self, tag_name, request):
        if len(tag_name) < 2:
            messages.error(
                request,
                f"'{tag_name}' tag was not created because it is "
                "less than 2 characters.")

        storage = messages.get_messages(request)
        storage.used = False  # don't clear messages
        return len(storage) == 0


class Tag(models.Model):
    name = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TagManager()
