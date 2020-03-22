from django.urls import path
from sitnow import views

app_name = "sitnow"

urlpatterns = [
    path("", views.index, name="index"),
    path("aboutus/", views.aboutus, name="aboutus"),
    path("forwhom/", views.forwhom, name="forwhom"),
    path("tutorial/", views.tutorial, name="tutorial"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("map/", views.map, name="map"),
    path("favorite/", views.favorite, name="favorite"),

    # Usually by get, get info of all the places
    path("places/", views.places, name="places"),

    # Page of setting user profile
    path("setting/", views.update_profile, name="update_profile"),
    # POST only, to get the search result
    path("result/", views.result, name="result"),
    # POST only, to get info of a specific place
    path("place/", views.place, name="place"),
    # POST only, to get all comment of a place
    path("comments/", views.comments, name="comments"),
    # POST only, to comment a place
    path("comment/", views.post_comment, name="comment"),
    # POST only, to get the user information
    path("getuser/", views.get_user, name="getuser"),
    # POST only, to get the current user's favorite places
    path("favorites/", views.favorites, name="favorites"),
]
