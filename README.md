# Sit Now

A seat finder app of Glasgow University.

## Contents

- [Objective](#objective)
- [Feature](#feature)
- [Technologies](#technologies)
- [ER Diagram](#er-diagram)
- [Site Map](#site-map) 
- [Screenshot](#screenshot)
- [Local Deployment](#local-deployment) 

## Objective

- It is the final assessment of the Internet Technology lecture.
- The objective of this application is to provide users, who happen to be at the UoG campus, with the location of a place to have a seat.

## Feature

- Users can use the app to find a location available in UoG where they can sit down and study.
- User can find the three most suitable places among 30+ buildings within campus by selecting multiple requirements. For instance, sockets and WiFi access, food service (microwave/ hot water tap), and quiet study.
- The app applies Google map APIs to direct users to chosen destination.
- The app provides up-to-date information about each place by other users. For instance, rating and comments.

## Technologies

- Frontend: JQuery & Bootstrap
- Backend: Django
- Database: SQLite
- Third-party APIs: Google Map APIs
  - Directions API
  - Maps JavaScript API
  - Places API

## ER Diagram

<img src="https://raw.githubusercontent.com/lightcoker/Sit-Now/master/doc/img/ER_diagram_w_background.png" alt="ER diagram" style="zoom:24%;" />

## Site Map

<img src="https://raw.githubusercontent.com/lightcoker/Sit-Now/master/doc/img/site_map.png" alt="site map" style="zoom:48%;" />

## Screenshot

- Homepage: Users can choose their location and filtering conditions to find seat locations.

<img src="https://raw.githubusercontent.com/lightcoker/Sit-Now/master/doc/img/screenshot_homepage.jpg" alt="home page" style="zoom:24%;" />

- Search result: Top three nearest location would be shown, including the information and the direction to the place. Users can also change their filtering conditions on the search bar above.

![search result](https://raw.githubusercontent.com/lightcoker/Sit-Now/master/doc/img/screenshot_search_result.jpg)

- Map of all places: Users could click on the map and see all places with pictures and information in the system.

<img src="https://raw.githubusercontent.com/lightcoker/Sit-Now/master/doc/img/screenshot_map.jpg" alt="map" />

- Rating and comments: Users can rate and comment on the place after logging in. The rate would be averaged and shown as the overall rating of the place.

![comment 1](https://raw.githubusercontent.com/lightcoker/Sit-Now/master/doc/img/screenshot_comment_1.jpg)

![comment 2](https://raw.githubusercontent.com/lightcoker/Sit-Now/master/doc/img/screenshot_comment_2.jpg)

- Favourite place: Users could add favourite places to their collection after logging in.

![favourite](https://raw.githubusercontent.com/lightcoker/Sit-Now/master/doc/img/screenshot_favorite.jpg)

## Local Deployment

1. Clone the `lightcoker/Sit-Now` repository into your working directory.

2. Initialize a python 3.7.5 (virtual) environment and install packages by `$ pip install -r requirements.txt`.

3. To run the app, you need to get your own **Google API key** for Directions API, Maps JavaScript API, and Places API. And then copy and paste your Google API key into `./sitnow_project/sitnow_project/config/prod.py` file and replace both `os.getenv("GOOGLE_API_KEY")` and `os.getenv("GOOGLE_JS_API_KEY")` by the key as Strings.

   > Note: **If you already have the `dev.py` file from developers of this repository, simply move the `dev.py` file to `./sitnow_project/sitnow_project/config/`.**

4. `IS_DEBUG` in `dev.py` could be set to `True` in your development environment but should always be `False` in any production environment.

5. Go to the project directory `/sitnow_project/` by `$ cd /sitnow_project/`

6. Initialize the database by `$ python manage.py makemigrations` and then `$ python manage.py migrate`.

7. Create root account by `$ python manage.py createsuperuser`.

8. Populate data for places, users and comments by `$ python population_script.py`.

9. Good to go! Run the server by `$ python manage.py runserver` and go to [localhost:8000](http://localhost:8000/).
