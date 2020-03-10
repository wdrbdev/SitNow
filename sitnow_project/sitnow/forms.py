from django import forms
from django.contrib.auth.models import User
from sitnow.models import UserProfile

# Form for user model provide by Django

class UserForm(forms.ModelForm):
    # Hide the password when user input the password by PasswordInput()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
        )


# Form for custom user profile
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("preferred_name", 'picture',)


# class SearchForm(forms.ModelForm):
#     google_id = forms.CharField()
#     # CHOICES = [
#     #     ('hasTable', 'hasTable'),
#     #     ('hasWifi','hasWifi'),
#     #     ('hasMicrowave','hasMicrowave'),]
#     # select = forms.MultipleChoiceField(choices = CHOICES)
#     class Meta:
#         model = Place
#         fields = (
#             "google-id",
#             # "select",
#             # "capacity",
#         )


