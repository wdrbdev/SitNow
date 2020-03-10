from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User



# Create your models here.


# Add custom feature on user model provide by Django
class UserProfile(models.Model):
    PREFERRED_NAME_MAX_LENGTH = 200
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # add to upload photo file ################
    picture = models.ImageField(upload_to='profile_images', blank=True)


    # The additional attributes we wish to include.
    preferred_name = models.CharField(
        max_length=PREFERRED_NAME_MAX_LENGTH, blank=True, null=True)

    # return a meaningful value when a string representation of a `UserProfile` model instance is requested
    def __str__(self):
        return self.user.username


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
        return self.name


class SearchHistory(models.Model):
    CHAR_MAX_LENGTH = 255
    search_history_id = models.AutoField(primary_key=True)
    user = models.name = models.ForeignKey(User, on_delete=models.CASCADE)

    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    time_stamp = models.DateTimeField(auto_now_add=True, blank=True)

    place1 = models.ForeignKey(
        Place, related_name="place1", on_delete=models.CASCADE
    )
    place2 = models.ForeignKey(
        Place, related_name="place2", on_delete=models.CASCADE
    )
    place3 = models.ForeignKey(
        Place, related_name="place3", on_delete=models.CASCADE
    )

    hasTable = models.BooleanField(default=True, null=True)
    hasWifi = models.BooleanField(default=True, null=True)
    capacity = models.IntegerField(null=True)
    hasMicrowave = models.BooleanField(default=False, null=True)
    hasSocket = models.BooleanField(default=False, null=True)
    hasFood = models.BooleanField(default=False, null=True)
    hasCoffee = models.BooleanField(default=False, null=True)
    canEat = models.BooleanField(default=False, null=True)
    hasComputer = models.BooleanField(default=False, null=True)

    def __str__(self):
        return "Histroy id: " + str(self.search_history_id)

    class Meta:
        verbose_name_plural = "Search histories"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    rate = models.IntegerField()
    comment = models.TextField(null=True)

    def __str__(self):
        return self.user.username + " comments " + self.place.name
