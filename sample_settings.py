# Django settings for league project.

DEBUG          = True
TEMPLATE_DEBUG = DEBUG
RUN_LOCALLY    = False     # False = run on google appengine


ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)


from pytz.gae import pytz

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
import os.path
HOME = os.path.abspath(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)),'media')
#MEDIA_ROOT = path.replace('\\','/')


# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '-@v5@bixib9#b9wtxdodj1ke5tc(yfdvq(4&4p)ywo&w%ed6u1'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(HOME,'templates')
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'base'
)

""" Use a google gmail account to update news stories on your site. If
    you want to delete a story, go the gmail and just read the story
"""
GOOGLE = {'email':'your.webpage@gmail.com',
          'password':'your password'
         }

""" Set up an account with Contact.IO They provide the interface to googles
    email service internally
"""		 
CONTEXTIO = { 'CONSUMER_KEY'   : 'your key',
              'CONSUMER_SECRET': 'your secret',
              'your.webpage@gmail.com' :'your secret'
            }