# instance/config.py is for local settings, it overrides upper level config.py.

#################### SAMPLE ####################
DEBUG = True

SECRET_KEY = b'123456789'
MAX_SIZE_UPLOAD_MEGS = 16 * 1000 * 1000  # limit the maximum allowed payload to 16 megabytes

LOCATION_OF_STATIC_FILE = './dir/'
CONTENT_PATH = './dir/content'
IMG_UPLOAD_FOLDER = './dir/static/img'
ARCHETYPES_PATH = './dir/archetypes'
ABS_PATH_DEPLOY_SCRIPT = '/home/user/test_script.sh'