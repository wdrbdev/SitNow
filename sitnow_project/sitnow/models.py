from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import os
from sitnow.utils.upload import user_directory_path


# Add custom feature on user model provide by Django
class UserProfile(models.Model):
    PREFERRED_NAME_MAX_LENGTH = 200
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # The additional attributes we wish to include.
    preferred_name = models.CharField(
        max_length=PREFERRED_NAME_MAX_LENGTH, blank=True)
    picture = models.ImageField(upload_to=user_directory_path, blank=True,
                                default='sitnow_project/media/profile_images/default_profile_img.svg')

    # return a meaningful value when a string representation of a `UserProfile` model instance is requested
    def __str__(self):
        return self.user.username


# Information of each places with seats
class Place(models.Model):
    CHAR_MAX_LENGTH = 255
    name = models.CharField(max_length=CHAR_MAX_LENGTH)
    building = models.CharField(max_length=CHAR_MAX_LENGTH)
    level = models.IntegerField(null=True)

    google_id = models.CharField(max_length=CHAR_MAX_LENGTH)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    address = models.TextField(null=True)
    image_url = models.URLField(null=True)

    permission = models.TextField(null=True)
    hasTable = models.BooleanField(default=True, null=True)
    hasWifi = models.BooleanField(default=True, null=True)
    capacity = models.IntegerField(null=True)
    hasMicrowave = models.BooleanField(default=False, null=True)
    hasSocket = models.BooleanField(default=False, null=True)
    hasFood = models.BooleanField(default=False, null=True)
    hasCoffee = models.BooleanField(default=False, null=True)
    noEating = models.BooleanField(default=False, null=True)
    hasComputer = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.name + " @ " + self.building


# Information about users' rating and comment of a place
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    rate = models.IntegerField()
    comment = models.TextField(null=True)

    def __str__(self):
        return self.user.username + " comments " + self.place.name


# Information about users' favorite place
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    favorite = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.user.username + " likes " + self.place.name
