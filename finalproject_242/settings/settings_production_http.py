import dj_database_url
DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = [".herokuapp.com"]
STATIC_ROOT = "staticfiles"

DATABASES = {'default': dj_database_url.config()}