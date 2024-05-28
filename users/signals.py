from django.contrib.auth.models import User
from django.contrib.auth import user_logged_in
from django.dispatch import receiver
from .models import CustomUser


# when someone logs in, create an instance of CustomUser for them if it doesn't exist
@receiver(user_logged_in)
def create_custom_user_if_not_exists(sender, user, request, **kwargs):
    custom_user, created = CustomUser.objects.get_or_create(email=user.email)

    if created:
        custom_user.save()
