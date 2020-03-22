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
# Create your views here.

BUILDINGS_JSON = [
    {
        "building": "St Andrews Building",
        "latitude": 55.8717315,
        "longitude": -4.279621199999999
    },
    {
        "building": "Kelvin Hall",
        "latitude": 55.86900070000001,
        "longitude": -4.2932081
    },
    {
        "building": "Glasgow International College",
        "latitude": 55.87027759999999,
        "longitude": -4.296623
    },
    {
        "building": "Robertson Building",
        "latitude": 55.87060229999999,
        "longitude": -4.296550499999999
    },
    {
        "building": "Sir James Black Building",
        "latitude": 55.87087339999999,
        "longitude": -4.292354700000001
    },
    {
        "building": "Wolfson Building",
        "latitude": 55.8708469,
        "longitude": -4.292517000000001
    },
    {
        "building": "Davidson Building",
        "latitude": 55.8709702,
        "longitude": -4.2915936
    },
    {
        "building": "Mathematics and Statistics Building",
        "latitude": 55.87260729999999,
        "longitude": -4.2944843
    },
    {
        "building": "Joseph Black Building",
        "latitude": 55.8719964,
        "longitude": -4.2933843
    },
    {
        "building": "Western Infirmary Lecture Theatre",
        "latitude": 55.872027,
        "longitude": -4.2941475
    },
    {
        "building": "Graham Kerr Building",
        "latitude": 55.8714317,
        "longitude": -4.2929365
    },
    {
        "building": "Kelvin Building",
        "latitude": 55.8715313,
        "longitude": -4.2917421
    },
    {
        "building": "Isabella Elder Building",
        "latitude": 55.8724783,
        "longitude": -4.2921985
    },
    {
        "building": "Bower Building",
        "latitude": 55.872391,
        "longitude": -4.2914581
    },
    {
        "building": "Main Gatehouse",
        "latitude": 55.8723468,
        "longitude": -4.2893085
    },
    {
        "building": "McIntyre Building",
        "latitude": 55.87221649999999,
        "longitude": -4.2888242
    },
    {
        "building": "Main Building",
        "latitude": 55.87147030000001,
        "longitude": -4.2884926
    },
    {
        "building": "Thomson Building",
        "latitude": 55.8715264,
        "longitude": -4.286881899999999
    },
    {
        "building": "James Watt Building",
        "latitude": 55.87113129999999,
        "longitude": -4.2864642
    },
    {
        "building": "Pearce Lodge",
        "latitude": 55.8719143,
        "longitude": -4.2858711
    },
    {
        "building": "Gilmorehill Halls",
        "latitude": 55.87211379999999,
        "longitude": -4.284410200000001
    },
    {
        "building": "Sir Charles Wilson Building",
        "latitude": 55.8726314,
        "longitude": -4.284052000000001
    },
    {
        "building": "Glasgow University Union",
        "latitude": 55.8723812,
        "longitude": -4.2851665
    },
    {
        "building": "Rankine Building",
        "latitude": 55.8725956,
        "longitude": -4.2857091
    },
    {
        "building": "Stevenson Sports Building",
        "latitude": 55.87288899999999,
        "longitude": -4.2852912
    },
    {
        "building": "Ivy Lodge",
        "latitude": 55.8732522,
        "longitude": -4.285847899999999
    },
    {
        "building": "Southpark House",
        "latitude": 55.8738786,
        "longitude": -4.287020099999999
    },
    {
        "building": "Florentine House",
        "latitude": 55.87358709999999,
        "longitude": -4.287916399999999
    },
    {
        "building": "The Fraser Building",
        "latitude": 55.873081,
        "longitude": -4.287935299999999
    },
    {
        "building": "McMillan Round Reading Room",
        "latitude": 55.8727392,
        "longitude": -4.2879725
    },
    {
        "building": "Hetherington Building",
        "latitude": 55.8742069,
        "longitude": -4.2888531
    },
    {
        "building": "Glasgow University Library",
        "latitude": 55.8733667,
        "longitude": -4.288945699999999
    },
    {
        "building": "Hunterian Art Gallery",
        "latitude": 55.8730183,
        "longitude": -4.289102
    },
    {
        "building": "Adam Smith Building",
        "latitude": 55.8737664,
        "longitude": -4.2898664
    },
    {
        "building": "Lilybank House",
        "latitude": 55.8740368,
        "longitude": -4.2904601
    },
    {
        "building": "Sir Alwyn Williams Building",
        "latitude": 55.8739481,
        "longitude": -4.2918572
    },
    {
        "building": "Queen Margaret Union",
        "latitude": 55.87370989999999,
        "longitude": -4.2917144
    },
    {
        "building": "Sir Alexander Stone Building",
        "latitude": 55.8735569,
        "longitude": -4.2909882
    },
    {
        "building": "Gregory Building",
        "latitude": 55.8740534,
        "longitude": -4.2928603
    },
    {
        "building": "Boyd Orr Building",
        "latitude": 55.8735672,
        "longitude": -4.2925851
    },
    {
        "building": "Glasgow University Library",
        "latitude": 55.8733667,
        "longitude": -4.288945699999999
    },
    {
        "building": "Fraser Building",
        "latitude": 55.873081,
        "longitude": -4.287935299999999
    }
]


def index(request):
    form = SearchForm()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        # Have we been provided with a valid form?
        if form.is_valid():
            # Now that the category is saved, we could confirm this.
            # For now, just redirect the user back to the index view.
            return redirect('/result/')
        else:
            # The supplied form contained errors -
            # just print them to the terminal.
            print(form.errors)
    # BUILDINGS_JSON_PATH = os.path.join(
    #     BASE_DIR, "sitnow_project", "buildings.json")
    # locations = read_json(BUILDINGS_JSON_PATH)
    locations = BUILDINGS_JSON

    context_dict = {"form": form, "locations": locations,
                    "GOOGLE_JS_API_KEY": GOOGLE_JS_API_KEY}
    return render(request, "sitnow/index.html", context=context_dict)


def result(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = SearchForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            search_location = validate_querydict(request.POST)
            filtered_places = filter(search_location)
            k_nearset = get_k_nearest(
                search_location, filtered_places, 3)
            k_google_nearset = get_google_k_nearest(
                search_location, k_nearset, 2)
            d = {}
            start = {"latitude": float(search_location["latitude"]), "longitude": float(
                search_location["longitude"])}
            d["start"] = start

            # BUILDINGS_JSON_PATH = os.path.join(
            #     BASE_DIR, "sitnow_project", "buildings.json")
            # locations = read_json(BUILDINGS_JSON_PATH)
            # d["locations"] = locations
            d["locations"] = BUILDINGS_JSON

            d["form"] = form
            d["GOOGLE_JS_API_KEY"] = GOOGLE_JS_API_KEY

            d["n_results"] = len(k_google_nearset)
            if len(k_google_nearset) > 0:
                i = 1
                for place in k_google_nearset:
                    place_dict = model_to_dict(place)
                    place_dict['rate'], place_dict['n_rates'] = get_avg_rate(
                        place)
                    if request.user.is_authenticated:
                        favorite = Favorite.objects.filter(
                            user=request.user, place=place).first()
                        if not favorite:
                            favorite = Favorite.objects.create(
                                user=request.user, place=place)
                        place_dict['favorite'] = model_to_dict(favorite)

                    d["place" + str(i)] = place_dict
                    i += 1
                    print(place_dict)
            else:
                d['isEmpty'] = True
                response = render(request, "sitnow/result.html", context=d)
            response = render(request, "sitnow/result.html", context=d)

            return response
        else:
            # The supplied form contained errors -
            # just print them to the terminal.
            print(form.errors)
    return HttpResponseBadRequest(content="400 Bad Request")


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
    return HttpResponseBadRequest(content="400 Bad Request")


def get_avg_rate(place):
    comments = Comment.objects.filter(place=place)
    n_rates = len(comments)
    if(len(comments) != 0):
        rate_sum = 0
        for comment in comments:
            rate_sum += comment.rate
        return (rate_sum / len(comments), n_rates)
    return (-1, 0)


def get_user(request):
    if request.method == 'POST':
        d = {}
        user_profile = model_to_dict(
            UserProfile.objects.get(user=request.user))
        d['picture'] = "media/" + str(user_profile['picture'])
        d['preferred_name'] = user_profile['preferred_name']
        return JsonResponse(d, safe=False)
    return HttpResponseBadRequest(content="400 Bad Request")


def favorite(request):
    if request.method == 'POST':
        place = Place.objects.get(pk=request.POST['placeId'])
        user = User.objects.get(pk=request.user.id)
        favorite = Favorite.objects.get_or_create(user=user, place=place)[0]
        favorite.favorite = not favorite.favorite
        favorite.save()
        return JsonResponse(model_to_dict(favorite), safe=False)
    return HttpResponseBadRequest(content="400 Bad Request")


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


@login_required
def post_comment(request):
    if request.method == 'POST':
        data = dict(request.POST)
        print(data)
        place = Place.objects.get(pk=int(data['place_id'][0]))
        user = User.objects.get(pk=request.user.id)
        try:
            comment = Comment.objects.create(place=place, user=user,
                                             comment="\"" + data['comment'][0] + "\"", rate=data['rate'][0])
        except KeyError:
            comment = Comment.objects.create(place=place, user=user,
                                             comment="", rate=data['rate'][0])
        comment.save()
        return JsonResponse(model_to_dict(place), safe=False)
    return HttpResponseBadRequest(content="400 Bad Request")


@csrf_exempt
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
    return HttpResponseBadRequest(content="400 Bad Request")


def get_place(request):
    name = request.POST['name']
    google_id = request.POST['google_id']
    building = request.POST['building']
    place = Place.objects.get(
        name=name, google_id=google_id, building=building)
    return place


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


def aboutus(request):
    context_dict = {}
    context_dict["about_msg"] = "About SitNow"

    response = render(request, "sitnow/aboutus.html", context=context_dict)

    return response


def forwhom(request):
    context_dict = {}
    context_dict["forwhom_msg"] = "For Whom SitNow"

    response = render(request, "sitnow/forwhom.html", context=context_dict)

    return response


def tutorial(request):
    context_dict = {}
    context_dict["tutorial_msg"] = "Tutorial SitNow"

    response = render(request, "sitnow/tutorial.html", context=context_dict)

    return response


def map(request):
    context_dict = {}
    context_dict["map_msg"] = "map"
    context_dict["GOOGLE_JS_API_KEY"] = GOOGLE_JS_API_KEY

    response = render(request, "sitnow/map.html", context=context_dict)

    return response


@login_required
def favorites(request):
    context_dict = {}
    favorites = list(Favorite.objects.filter(user=request.user, favorite=True))
    favorite_places = []
    for favorite in favorites:
        d = {}
        favorite_dict = model_to_dict(favorite)
        place = Place.objects.get(pk=favorite_dict["place"])
        d["place"] = model_to_dict(place)
        d["favorite"] = favorite_dict["favorite"]
        rate, d['n_rates'] = get_avg_rate(
            place)
        d['rate'] = round((rate * 100 / 5) / 10) * 10 if rate != -1 else 0
        favorite_places.append(d)
        print(d)

    user_profile = UserProfile.objects.get(user=request.user)
    context_dict["user_profile"] = model_to_dict(user_profile)
    if context_dict["user_profile"]["picture"] == "/media/profile_images/default_profile_img.svg":
        context_dict["user_profile"]["picture"] = "/profile_images/default_profile_img.svg"
    context_dict["favorites"] = favorite_places

    return render(request, "sitnow/favorites.html", context=context_dict)


# @login_required
# def setting(request):
#     context_dict = {}
#     context_dict["setting_msg"] = "setting"

#     print(context_dict["user_profile"])
#     response = render(request, "sitnow/setting.html", context=context_dict)

#     return response


def register(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == "POST":
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            if profile.preferred_name is "":
                profile.preferred_name = user.username

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            else:
                profile.picture = "/media/profile_images/default_profile_img.svg"

            profile.save()

            # Update our variable to indicate that the template
            # registration was successful.
            registered = True
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
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


def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == "POST":
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>']
        # will raise a KeyError exception.
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return redirect(reverse("sitnow:index"))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Sit Now account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print(f"Invalid login details: {username}, {password}")
            return redirect(reverse("sitnow:login"))

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, "sitnow/login.html")


# Use the login_required() decorator to ensure only those logged in can
# access the view.
@login_required(login_url="/login/")
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse("sitnow:index"))


def update_profile(request):
    d = {}
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user

            if 'picture' in request.FILES:
                user_profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            user_profile.save()
        return redirect(reverse("sitnow:update_profile"))

    form = UserProfileForm(instance=request.user.userprofile)

    d['form'] = form

    user_profile = UserProfile.objects.get(user=request.user)
    d["user_profile"] = model_to_dict(user_profile)
    if d["user_profile"]["picture"] == "/media/profile_images/default_profile_img.svg":
        d["user_profile"]["picture"] = "/profile_images/default_profile_img.svg"
    return render(request, 'sitnow/setting.html', d)
