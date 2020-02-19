from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


# Create your models here.


# Add custom feature on user model provide by Django
class UserProfile(models.Model):
    PREFERRED_NAME_MAX_LENGTH = 200
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # The additional attributes we wish to include.
    preferred_name = models.CharField(
        max_length=PREFERRED_NAME_MAX_LENGTH, blank=True)

    # return a meaningful value when a string representation of a `UserProfile` model instance is requested
    def __str__(self):
        return self.user.username
