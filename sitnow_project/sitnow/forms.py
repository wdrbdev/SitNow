from django import forms
from django.contrib.auth.models import User
from sitnow.models import Comment, Place, UserProfile

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


class SearchForm(forms.Form):
    latitude = forms.FloatField(
        required=True, help_text="Your latitude", widget=forms.HiddenInput())
    longitude = forms.FloatField(
        required=True, help_text="Your longitude", widget=forms.HiddenInput())

    CAPACITY = [("1", "1 - 2 persons"),
                ("2", "3 - 8 persons"),
                ("3", "Above 8 persons"), ]
    hasTable = forms.CharField(
        help_text="Has Table?", widget=forms.HiddenInput(), initial="None")
    hasWifi = forms.CharField(
        help_text="Has WIFI?", widget=forms.HiddenInput(), initial="None")
    capacity = forms.ChoiceField(
        choices=CAPACITY, help_text="How many people with you?")
    hasMicrowave = forms.CharField(
        help_text="Has Microwave", widget=forms.HiddenInput(), initial="None")
    hasSocket = forms.CharField(
        help_text="Has Socket?", widget=forms.HiddenInput(), initial="None")
    hasFood = forms.CharField(
        help_text="Providing Food?", widget=forms.HiddenInput(), initial="None")
    noEating = forms.CharField(
        help_text="Can eat inside?", widget=forms.HiddenInput(), initial="None")
    hasCoffee = forms.CharField(
        help_text="Providing Coffee?", widget=forms.HiddenInput(), initial="None")
    hasComputer = forms.CharField(
        help_text="Has computer?", widget=forms.HiddenInput(), initial="None")
