DEBUG = False

SECRET_KEY = b''
MAX_SIZE_UPLOAD_MEGS = 16 * 1000 * 1000  # limit the maximum allowed payload to 16 megabytes

# Paths should be overridden locally in instance/config.py
LOCATION_OF_STATIC_DIR = './website/'
CONTENT_PATH = './website/content'
IMG_UPLOAD_FOLDER = './website/static/img'
ARCHETYPES_PATH = './website/archetypes'
ABS_PATH_DEPLOY_SCRIPT = '/home/user/test_script.sh'

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

CONTENT_TYPES = [
    'agenda',
    'contemporain',
    'dessins',
    'home',
    'peintures',
]

LANGUAGES_AVAILABLE = [
    'fr',
    'en',
]

PARAMETERS = {
    'date': {
        'type_of_param': 'datetime',
        'is_in_quotes': True,
        'is_required': True,
        'is_upload': False,
    },
    'draft': {
        'type': 'bool',
        'is_in_quotes': False,
        'is_required': True,
        'is_upload': False,
    },
    'og_image': {
        'type': 'url',
        'is_in_quotes': True,
        'is_required': False,
        'is_upload': True,
    },
    'og_description': {
        'type': 'str',
        'is_in_quotes': True,
        'is_required': False,
        'is_upload': False,
    },
    'title': {
        'type': 'str',
        'is_in_quotes': True,
        'is_required': True,
        'is_upload': False,
    },
    'subtitle': {
        'type': 'str',
        'is_in_quotes': True,
        'is_required': False,
        'is_upload': False,
    },
    'technique': {
        'type': 'str',
        'is_in_quotes': True,
        'is_required': False,
        'is_upload': False,
    },
    'dimensions': {
        'type': 'str',
        'is_in_quotes': True,
        'is_required': False,
        'is_upload': False,
    },
    'url_image_main': {
        'type': 'url',
        'is_in_quotes': True,
        'is_required': False,
        'is_upload': True,
    },
    'date_creation': {
        'type': 'str',
        'is_in_quotes': True,
        'is_required': False,
        'is_upload': False,
    },
    'weight': {
        'type': 'int',
        'is_in_quotes': False,
        'is_required': False,
        'is_upload': False,
    },
    'detail_titre': {
        'type': 'str',
        'is_in_quotes': True,
        'is_required': False,
        'is_upload': False,
    },
    'detail_image_url': {
        'type': 'url',
        'is_in_quotes': True,
        'is_required': False,
        'is_upload': True,
    },
    'detail_texte': {
        'type': 'str',
        'is_in_quotes': True,
        'is_required': False,
        'is_upload': False,
    },
    'lieu': {
        'type': 'str',
        'is_in_quotes': True,
        'is_required': False,
        'is_upload': False,
    },
    'date_expo_format_texte': {
        'type': 'str',
        'is_in_quotes': True,
        'is_required': False,
        'is_upload': False,
    },
    'date_expo_start_format_machine': {
        'type': 'datetime',
        'is_in_quotes': True,
        'is_required': False,
        'is_upload': False,
    },
    'date_expo_end_format_machine': {
        'type': 'datetime',
        'is_in_quotes': True,
        'is_required': False,
        'is_upload': False,
    },
    'summary': {
        'type': 'str',
        'is_in_quotes': True,
        'is_required': False,
        'is_upload': False,
    },
    'external_link': {
        'type': 'url',
        'is_in_quotes': True,
        'is_required': False,
        'is_upload': False,
    },
    'image': {
        'type': 'url',
        'is_in_quotes': True,
        'is_required': False,
        'is_upload': True,
    },
    'caption': {
        'type': 'str',
        'is_in_quotes': True,
        'is_required': False,
        'is_upload': False,
    },
    'widget': {
        'type': 'str',
        'is_in_quotes': True,
        'is_required': False,
        'is_upload': False,
    },
    'image_url': {
        'type': 'url',
        'is_in_quotes': True,
        'is_required': False,
        'is_upload': True,
    },
    'image_href': {
        'type': 'str',
        'is_in_quotes': True,
        'is_required': False,
        'is_upload': False,
    },
    'youtube_video_id': {
        'type': 'str',
        'is_in_quotes': True,
        'is_required': False,
        'is_upload': False,
    },
    'youtube_video_width': {
        'type': 'str',
        'is_in_quotes': True,
        'is_required': False,
        'is_upload': False,
    },
    'youtube_video_height': {
        'type': 'str',
        'is_in_quotes': True,
        'is_required': False,
        'is_upload': False,
    },
    'end_text': {
        'type': 'str',
        'is_in_quotes': True,
        'is_required': False,
        'is_upload': False,
    },
    'template_display_only_raw_html': {
        'type': 'str',
        'is_in_quotes': True,
        'is_required': False,
        'is_upload': False,
    },
}

