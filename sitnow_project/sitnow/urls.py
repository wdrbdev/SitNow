from django.urls import path
from sitnow import views

app_name = "sitnow"

urlpatterns = [
    path("", views.index, name="index"),
    path("aboutus/", views.aboutus, name="aboutus"),
    path("advantages/", views.advantages, name="advantages"),
    path("forwhom/", views.forwhom, name="forwhom"),
    path("tutorial/", views.tutorial, name="tutorial"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("favorite/", views.favorite, name="favorite"),
    path("setting/", views.setting, name="setting"),
    path("logout/", views.user_logout, name="logout"),
    path("forum/", views.forum, name="forum"),
    path("result/", views.result, name="result"),

    # path("test/", views.test, name="test"),
]
