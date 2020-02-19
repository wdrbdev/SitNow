import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(BASE_DIR, 'config')

# filepath for dev/prod keys
dev_keys_path = os.path.join(CONFIG_DIR, 'dev.py')
prod_keys_path = os.path.join(CONFIG_DIR, 'prod.py')

# Check for environment and import corresponding keys
if os.path.isfile(dev_keys_path):
    from letsgo_project.config.dev import *
else:
    from letsgo_project.config.prod import *


def print_env():
    print('------------------------------')
    print(f'Current environment is \'{environment}\'.')
    print('------------------------------')
