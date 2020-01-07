from django.db import models
from django.contrib import messages
from django.contrib.messages import get_messages
import bcrypt
import re  # regex

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):

    def register(self, request):
        user = None

        if self.is_reg_valid(request):
            user = User(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                password=bcrypt.hashpw(
                    request.POST['password'].encode(),
                    bcrypt.gensalt()).decode()
            )
            user.save()
            request.session['user_id'] = user.id
        return user

    def is_reg_valid(self, request):

        if not EMAIL_REGEX.match(request.POST['email']):
            messages.error(request, "Invalid email address.")

        if len(request.POST['first_name']) < 3:
            messages.error(
                request, "First Name must be more than 2 characters.")

        if len(request.POST['last_name']) < 3:
            messages.error(
                request, "Last Name must be more than 2 characters.")

        if len(request.POST['password']) < 8:
            messages.error(
                request, "Password must be more than 8 characters."
            )

        if request.POST["password"] != request.POST["password_confirm"]:
            messages.error(request, "Passwords must match.")

        if super().get_queryset().filter(email=request.POST['email']).first():
            messages.error(request, "Email taken.")

        error_messages = messages.get_messages(request)
        error_messages.used = False  # don't clear messages
        return len(error_messages) == 0

    def attempt_login(self, request):

        # get the User.objects queryset to filter
        # UserManager is a subclass of User, so User is parent (super)
        user_matching_email = super().get_queryset().filter(
            email=request.POST['email']).first()

        if user_matching_email:

            if bcrypt.checkpw(
                request.POST['password'].encode(),
                user_matching_email.password.encode()
            ):
                request.session['user_id'] = user_matching_email.id
                return user_matching_email

        messages.error(request, "Invalid credentials.")
        return user_matching_email

    def get_logged_in_user(self, request):

        return super().get_queryset().filter(
            id=request.session.get('user_id')
        ).first()


class User(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def full_name(self):
        return self.first_name + ' ' + self.last_name
