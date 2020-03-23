from django.shortcuts import render
from sitnow.forms import UserForm, UserProfileForm
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, JsonResponse
from sitnow.forms import SearchForm
from django.views.defaults import bad_request
from sitnow_project.config.keys import *
from sitnow.models import Comment, Favorite, Place, UserProfile
from django.forms.models import model_to_dict
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from sitnow.utils.validation import *
from sitnow.utils.csv_2_json import *
from sitnow.utils.get_places import *
from django.core.handlers import exception


# Index with SearchForm and building locations as option of the form
def index(request):
    form = SearchForm()

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            return redirect('/result/')
        else:
            print(form.errors)

    BUILDINGS_JSON_PATH = os.path.join(
        BASE_DIR, "sitnow_project", "buildings.json")
    locations = read_json(BUILDINGS_JSON_PATH)
    # locations = BUILDINGS_JSON

    # Include form, location options, and google api key
    context_dict = {"form": form, "locations": locations,
                    "GOOGLE_JS_API_KEY": GOOGLE_JS_API_KEY}
    return render(request, "sitnow/index.html", context=context_dict)


# Apply method in sitnow.utils to get the search result
def result(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = SearchForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Convert form input as the input of utils.get_places.filter()
            search_location = validate_querydict(request.POST)
            # Filter places according to search filter
            filtered_places = place_filter(search_location)
            # Calculate the top 5 nearest places according to the Euclidean distance
            k_nearset = get_k_nearest(
                search_location, filtered_places, 5)
            # Calculate the top 3 nearest places according to Google Directions API
            k_google_nearset = get_google_k_nearest(
                search_location, k_nearset, 3)

            d = {}
            # Pass the start location of the SearchForm
            start = {"latitude": float(search_location["latitude"]), "longitude": float(
                search_location["longitude"])}
            d["start"] = start

            # Pass building location as options of the SearchForm
            BUILDINGS_JSON_PATH = os.path.join(
                BASE_DIR, "sitnow_project", "buildings.json")
            locations = read_json(BUILDINGS_JSON_PATH)
            d["locations"] = locations

            d["form"] = form
            d["GOOGLE_JS_API_KEY"] = GOOGLE_JS_API_KEY

            # Convert the list of the top 3 nearest place into dictionary as place1, place2, and place3
            d["n_results"] = len(k_google_nearset)
            if len(k_google_nearset) > 0:
                i = 1
                for place in k_google_nearset:
                    place_dict = model_to_dict(place)
                    # Include rating of the place
                    place_dict['rate'], place_dict['n_rates'] = get_avg_rate(
                        place)
                    # Include info about whether the places is the current user's favorite place
                    if request.user.is_authenticated:
                        favorite = Favorite.objects.filter(
                            user=request.user, place=place).first()
                        if not favorite:
                            favorite = Favorite.objects.create(
                                user=request.user, place=place)
                        place_dict['favorite'] = model_to_dict(favorite)

                    # Name the top 3 places as place1, place2, and place3
                    d["place" + str(i)] = place_dict
                    i += 1
            # If no search result
            else:
                d['isEmpty'] = True
                response = render(request, "sitnow/result.html", context=d)
            response = render(request, "sitnow/result.html", context=d)

            return response
        else:
            print(form.errors)

    # POST only, if by GET, redirect to index
    return redirect(reverse("sitnow:index"))


# Get the place information according to place name and building
def place(request):
    if request.method == 'POST':
        name = request.POST['name']
        building = request.POST['building']
        place = Place.objects.filter(name=name, building=building).first()
        place_dict = model_to_dict(place)

        place_dict['rate'], place_dict['n_rates'] = get_avg_rate(
            place)

        if request.user.is_authenticated:
            favorite_tuple = Favorite.objects.get_or_create(
                user=request.user, place=place)
            if not favorite_tuple[1]:
                favorite_tuple[0].save()
            place_dict['favorite'] = model_to_dict(favorite_tuple[0])

        return JsonResponse(place_dict, safe=False)

    # POST only
    return bad_request(request, exception)


# Calculate the average rating of the place and how many user rate this place
def get_avg_rate(place):
    comments = Comment.objects.filter(place=place)

    n_rates = len(comments)
    if(n_rates != 0):
        rate_sum = 0
        for comment in comments:
            rate_sum += comment.rate
        return (rate_sum / n_rates, n_rates)

    return (-1, 0)


# Get the user's profile data, including pic and preferred name
def get_user(request):
    if request.method == 'POST':
        d = {}
        user_profile = model_to_dict(
            UserProfile.objects.get(user=request.user))
        d['picture'] = "media/" + str(user_profile['picture'])
        d['preferred_name'] = user_profile['preferred_name']
        return JsonResponse(d, safe=False)

    # POST only
    return bad_request(request, exception)


# Get the current user's favorite places
@login_required
def favorite(request):
    if request.method == 'POST':
        place = Place.objects.get(pk=request.POST['placeId'])
        user = User.objects.get(pk=request.user.id)
        favorite = Favorite.objects.get_or_create(user=user, place=place)[0]
        favorite.favorite = not favorite.favorite
        favorite.save()
        return JsonResponse(model_to_dict(favorite), safe=False)

    # POST only
    return bad_request(request, exception)

# Get all info of all places in the database


def places(request):
    places_dicts = []
    places = Place.objects.all()
    for place in places:
        d = model_to_dict(place)

        d['rate'], d['n_rates'] = get_avg_rate(
            place)

        if request.user.is_authenticated:
            favorite_tuple = Favorite.objects.get_or_create(
                user=request.user, place=place)
            if not favorite_tuple[1]:
                favorite_tuple[0].save()
            d['favorite'] = model_to_dict(favorite_tuple[0])

        places_dicts.append(d)

    return JsonResponse(places_dicts, safe=False)

# Save the comment when the user post it
@login_required
def post_comment(request):
    if request.method == 'POST':
        data = dict(request.POST)
        place = Place.objects.get(pk=int(data['place_id'][0]))
        user = User.objects.get(pk=request.user.id)

        # catch the exception when user leave the comment empty
        try:
            comment = Comment.objects.create(place=place, user=user,
                                             comment="\"" + data['comment'][0] + "\"", rate=data['rate'][0])
        except KeyError:
            comment = Comment.objects.create(place=place, user=user,
                                             comment="", rate=data['rate'][0])

        comment.save()
        return JsonResponse(model_to_dict(place), safe=False)

    # POST only
    return bad_request(request, exception)


# Get all the comment for a place
def comments(request):
    if request.method == "POST":
        place = get_place(request)
        comments = list(Comment.objects.filter(place=place))
        comment_dicts = []
        for comment in comments:
            comment_dict = model_to_dict(comment)
            d = {}
            d['rate'] = comment_dict['rate']
            d['comment'] = comment_dict['comment']
            d['user'] = get_comment_user(comment_dict['user'])
            comment_dicts.append(d)
        return JsonResponse(comment_dicts, safe=False)

    # POST only
    return bad_request(request, exception)


# Get a place according to place name, google place id and building
def get_place(request):
    name = request.POST['name']
    google_id = request.POST['google_id']
    building = request.POST['building']
    place = Place.objects.get(
        name=name, google_id=google_id, building=building)
    return place


# Get the user who post the comment
def get_comment_user(id):
    user = User.objects.get(pk=id)
    user_dict = model_to_dict(user)

    user_profile = UserProfile.objects.get(user=user)
    user_profile_dict = model_to_dict(user_profile)

    d = {}
    d['id'] = user_dict['id']
    d['preferred_name'] = user_profile_dict['preferred_name']
    d['picture'] = "media/" + str(user_profile_dict['picture'])
    return d


# Page of "About us"
def aboutus(request):
    context_dict = {}
    context_dict["about_msg"] = "About SitNow"
    response = render(request, "sitnow/aboutus.html", context=context_dict)
    return response


# Page of "For whom"
def forwhom(request):
    context_dict = {}
    context_dict["forwhom_msg"] = "For Whom SitNow"

    response = render(request, "sitnow/forwhom.html", context=context_dict)

    return response


# Page of "Tutorial"
def tutorial(request):
    context_dict = {}
    context_dict["tutorial_msg"] = "Tutorial SitNow"

    response = render(request, "sitnow/tutorial.html", context=context_dict)

    return response


# Page of "Map"
def map(request):
    context_dict = {}
    context_dict["map_msg"] = "map"
    context_dict["GOOGLE_JS_API_KEY"] = GOOGLE_JS_API_KEY

    response = render(request, "sitnow/map.html", context=context_dict)

    return response

# Display all favortie places of the current user
@login_required
def favorites(request):
    context_dict = {}
    favorite_places = []
    favorites = list(Favorite.objects.filter(user=request.user, favorite=True))

    for favorite in favorites:
        d = {}
        favorite_dict = model_to_dict(favorite)
        place = Place.objects.get(pk=favorite_dict["place"])
        d["place"] = model_to_dict(place)
        d["favorite"] = favorite_dict["favorite"]
        rate, d['n_rates'] = get_avg_rate(
            place)

        # Convert 5 star rating to percentage from 0% to 100%
        d['rate'] = round((rate * 100 / 5) / 10) * 10 if rate != -1 else 0
        favorite_places.append(d)

    # Get user profile
    user_profile = UserProfile.objects.get(user=request.user)
    context_dict["user_profile"] = model_to_dict(user_profile)
    if context_dict["user_profile"]["picture"] == "/media/profile_images/default_profile_img.svg":
        context_dict["user_profile"]["picture"] = "/profile_images/default_profile_img.svg"
    context_dict["favorites"] = favorite_places

    return render(request, "sitnow/favorites.html", context=context_dict)


# Page of "Sign up"
def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            # Hash the password with the set_password method.
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if profile.preferred_name is "":
                profile.preferred_name = user.username

            # Get the picture uploaded
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            else:
                profile.picture = "/media/profile_images/default_profile_img.svg"

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(
        request,
        "sitnow/register.html",
        context={
            "user_form": user_form,
            "profile_form": profile_form,
            "registered": registered,
        },
    )


# Page of "Login"
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse("sitnow:index"))
            else:
                return HttpResponse("Your Sit Now account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return redirect(reverse("sitnow:login"))

    else:
        return render(request, "sitnow/login.html")


# Page of "Logout"
@login_required(login_url="/login/")
def user_logout(request):
    logout(request)
    return redirect(reverse("sitnow:index"))


# Page of "Setting"
@login_required
def update_profile(request):
    d = {}
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user

            if 'picture' in request.FILES:
                user_profile.picture = request.FILES['picture']
            user_profile.save()
        return redirect(reverse("sitnow:update_profile"))

    form = UserProfileForm(instance=request.user.userprofile)
    d['form'] = form

    user_profile = UserProfile.objects.get(user=request.user)
    d["user_profile"] = model_to_dict(user_profile)
    if d["user_profile"]["picture"] == "/media/profile_images/default_profile_img.svg":
        d["user_profile"]["picture"] = "/profile_images/default_profile_img.svg"

    return render(request, 'sitnow/setting.html', d)
