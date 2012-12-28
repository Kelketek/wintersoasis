#
# Evennia MU* server configuration file
#
# You may customize your setup by copy&pasting the variables you want
# to change from the master config file src/settings_default.py to
# this file. Try to *only* copy over things you really need to customize
# and do *not* make any changes to src/settings_default.py directly.
# This way you'll always have a sane default to fall back on
# (also, the master config file may change with server updates).
#
from src.settings_default import *
######################################################################
# Evennia base server config
######################################################################
SERVERNAME = "Winter's Oasis"

CONNECTION_SCREEN_MODULE = "game.gamesrc.oasis.conf.connection_screens"
SSL_ENABLED = True
# Ports to use for SSL
SSL_PORTS = [8802]
TELNET_PORTS = [8888, 4322]
ALLOW_MULTISESSION = False

CHARACTER_DEFAULT_HOME = "#153"
######################################################################
# Evennia Database config
######################################################################

######################################################################
# Evennia pluggable modules
######################################################################
# Module containing your custom at_server_start(), at_server_reload() and
# at_server_stop() methods. These methods will be called every time
# the server starts, reloads and resets/stops respectively.
AT_SERVER_STARTSTOP_MODULE = "game.gamesrc.oasis.scripts.startstop"
######################################################################
# Default command sets
######################################################################
CMDSET_DEFAULT = "game.gamesrc.oasis.commands.standard.DefaultCmdSet"
CMDSET_UNLOGGEDIN = "game.gamesrc.oasis.commands.standard.UnloggedinCmdSet"
CMDSET_OOC = "game.gamesrc.oasis.commands.standard.OOCCmdSet"
######################################################################
# Typeclasses
######################################################################
BASE_CHARACTER_TYPECLASS = "game.gamesrc.oasis.objects.character.WOCharacter"
######################################################################
# Batch processors
######################################################################

######################################################################
# Game Time setup
######################################################################

######################################################################
# In-game access
######################################################################

######################################################################
# In-game Channels created from server start
######################################################################

# Public discussion
CHANNEL_PUBLIC = ("Public", ('pub',), 'Public discussion',
                  "control:perm(Wizards);listen:all();send:all()")

# Newbie channel
CHANNEL_NEWBIE = ("Public", ('pub',), 'Newbie Channel',
                  "control:perm(Wizards);listen:all();send:all()")
# General info about the server
CHANNEL_MUDINFO = ("MUDinfo", '', 'Informative messages',
                   "control:perm(Immortals);listen:perm(Immortals);send:false()")
# Channel showing when new people connecting
CHANNEL_CONNECTINFO = ("MUDconnections", '', 'Connection log',
                       "control:perm(Immortals);listen:perm(Wizards);send:false()")
######################################################################
# External Channel connections
######################################################################

######################################################################
# Config for Django
#####################################################################

DEBUG = False

ADMINS = ('kelketek@gmail.com',)

SERVER_EMAIL = 'messages@wintersoasis.com'

ROOT_URLCONF = "game.gamesrc.oasis.web.urls"

ACTIVE_TEMPLATE = 'wonews'

TEMPLATE_DIRS = (os.path.join(GAME_DIR, "gamesrc", "oasis", "web", "templates", ACTIVE_TEMPLATE),)
TEMPLATE_CONTEXT_PROCESSORS = tuple(set( TEMPLATE_CONTEXT_PROCESSORS + (
    'sekizai.context_processors.sekizai',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'django_authopenid.context_processors.authopenid',
    'django_messages.context_processors.inbox',
    'djangobb_forum.context_processors.forum_settings',
)))

MEDIA_ROOT = os.path.join(GAME_DIR, "gamesrc", "oasis", "web", "media")

STATIC_ROOT = os.path.join(GAME_DIR, "gamesrc", "oasis", "web", "static") 

SERVE_MEDIA = True

MEDIA_URL = '/media/'

STATIC_URL = '/static/'

INSTALLED_APPS = tuple(set(INSTALLED_APPS + (
    'south',
    'django_notify',
    'mptt',
    'sekizai',
    'sorl.thumbnail',
    'wiki',
    'wiki.plugins.attachments',
    'wiki.plugins.notifications',
    'wiki.plugins.images',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'django.contrib.messages',
    'registration',
    'pagination',
    'django_authopenid',
    'djangobb_forum',
    'haystack',
    'polls',
    'raven.contrib.django',
)))

MIDDLEWARE_CLASSES = (
    #'sslify.middleware.SSLifyMiddleware',
    'pagination.middleware.PaginationMiddleware',
) + MIDDLEWARE_CLASSES

"""
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
"""

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = False

# Gravitar support for DjangoBB
DJANGOBB_GRAVATAR_SUPPORT = False
GRAVATAR_DEFAULT = 'identicon'

# Haystack settings
HAYSTACK_SITECONF = os.path.join('game.gamesrc.oasis.web.search_sites')
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = os.path.join(GAME_DIR, 'gamesrc', 'oasis', 'web', 'djangobb_index')

# Django-article additions
"""
INSTALLED_APPS = tuple(set(INSTALLED_APPS + (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.markup',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.syndication',
    'articles',
)))
"""

TEMPLATE_CONTEXT_PROCESSORS = tuple(set(TEMPLATE_CONTEXT_PROCESSORS + (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
)))

TEMPLATE_LOADERS = ('templateloaderwithpriorities.Loader', ) + TEMPLATE_LOADERS

TEMPLATE_LOADER_PRIORITIES = [
    os.path.join(GAME_DIR, 'gamesrc', 'oasis', 'web', 'templates')
]

FILE_UPLOAD_PERMISSIONS = 0644

AUTHENTICATION_BACKENDS = ('game.gamesrc.oasis.web.models.CaseInsensitiveModelBackend',)

