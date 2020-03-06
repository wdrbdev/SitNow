from django.urls import path
from sitnow import views

app_name = "sitnow"

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("test/", views.test, name="test"),
]
