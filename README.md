# Sit Now

### Local Deployment
1. Clone the `lightcoker/Sit-Now` repository into a directory
2. Initialize a python 3.7.5 environment and install packages by `$ pip install -r requirements.txt`
3. Copy and paste your Google API key into `/sitnow_project/sitnow_project/config/prod.py` and replace both `os.getenv("GOOGLE_API_KEY")` and `os.getenv("GOOGLE_JS_API_KEY")`
4. Initialize the database by `$ python manage.py makemigrations` and `$ python manage.py migrate`
5. Create admin by `$ python manage.py createsuperuser`
6. Populating data for places, users and comments by `$ python poplate_sitnow.py`
7. Ready to go!
