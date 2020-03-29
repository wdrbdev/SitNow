# Sit Now

### Local Deployment

1. Clone the `lightcoker/Sit-Now` repository into your working directory.
2. Initialize a python 3.7.5 (virtual) environment and install packages by `$ pip install -r requirements.txt`.
3. To run the app, you need to get your own **Google API key** for Directions API, Maps JavaScript API, and Places API. And then copy and paste your Google API key into `./sitnow_project/sitnow_project/config/prod.py` file and replace both `os.getenv("GOOGLE_API_KEY")` and `os.getenv("GOOGLE_JS_API_KEY")` by the key as Strings.
   > Note: **If you already have the `dev.py` file from developers of this repository, simply move the `dev.py` file to `./sitnow_project/sitnow_project/config/`.**
4. Go to the project directory `/sitnow_project/` by `$ cd /sitnow_project/`
5. Initialize the database by `$ python manage.py makemigrations` and then `$ python manage.py migrate`.
6. Create root account by `$ python manage.py createsuperuser`.
7. Populate data for places, users and comments by `$ python population_script.py`.
8. Good to go! Run the server by `$ python manage.py runserver` and go to [localhost:8000](http://localhost:8000/).
