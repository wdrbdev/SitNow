from django import forms
from django.contrib.auth.models import User
from sitnow.models import Comment, Place, UserProfile
from sitnow.utils.upload import user_directory_path
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


# Form for user model provide by Django
# For login and register
class UserForm(forms.ModelForm):
    # Hide the password when user input the password by PasswordInput()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = (
            "username",
            "password",
        )

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields["username"].help_text = None


# Form for custom user profile
# For login, register and modify user profile in /setting/
class UserProfileForm(forms.ModelForm):
    PREFERRED_NAME_MAX_LENGTH = 255
    preferred_name = forms.CharField(
        max_length=PREFERRED_NAME_MAX_LENGTH, required=False)
    picture = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ("preferred_name", 'picture',)


# To search the places according to user location and choices in / and /result/
class SearchForm(forms.Form):
    latitude = forms.FloatField(
        required=True, help_text="Your latitude", widget=forms.HiddenInput())
    longitude = forms.FloatField(
        required=True, help_text="Your longitude", widget=forms.HiddenInput())

    CAPACITY = [("1", "0 - 4 persons"),
                ("2", "4 - 8 persons"),
                ("3", "Above 8 persons"), ]
    hasTable = forms.CharField(
        help_text="Has Table?", widget=forms.HiddenInput(), initial="None")
    hasWifi = forms.CharField(
        help_text="Has WIFI?", widget=forms.HiddenInput(), initial="None")
    capacity = forms.ChoiceField(
        choices=CAPACITY)
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

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['capacity'].label = "How many people with you?"
