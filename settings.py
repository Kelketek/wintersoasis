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
import os, sys
######################################################################
# Evennia base server config
######################################################################
SERVERNAME = "Winter's Oasis"

CONNECTION_SCREEN_MODULE = "game.gamesrc.oasis.conf.connection_screens"
SSL_ENABLED = True
# Ports to use for SSL
SSL_PORTS = [8802]
TELNET_PORTS = [8888, 4322]
ALLOW_MULTISESSION = True
AMP_PORT = 5000

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
CMDSET_CHARACTER = "game.gamesrc.oasis.commands.standard.DefaultCmdSet"
CMDSET_UNLOGGEDIN = "game.gamesrc.oasis.commands.standard.UnloggedinCmdSet"
CMDSET_PLAYER = "game.gamesrc.oasis.commands.standard.OOCCmdSet"
######################################################################
# Typeclasses
######################################################################
BASE_OBJECT_TYPECLASS = "game.gamesrc.oasis.objects.object.WOObject"
BASE_CHARACTER_TYPECLASS = "game.gamesrc.oasis.objects.character.WOCharacter"
BASE_PLAYER_TYPECLASS = "game.gamesrc.oasis.objects.player.WOPlayer"
BASE_ROOM_TYPECLASS = "game.gamesrc.oasis.objects.room.WORoom"
######################################################################
# Batch processors
######################################################################

######################################################################
# Game Time setup
######################################################################

######################################################################
# In-game access
######################################################################
LOCK_FUNC_MODULES = LOCK_FUNC_MODULES + ("game.gamesrc.oasis.conf.lockfuncs",)
######################################################################
# In-game Channels created from server start
######################################################################

# Public discussion
CHANNEL_PUBLIC = ("Public", ('pub',), 'Public discussion',
                  "control:perm(Wizards);listen:all();send:all()")

# Newbie channel
CHANNEL_NEWBIE = ("Newbie", ('new',), 'Newbie Channel',
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

ADMINS = ('admin@example.com',)

SERVER_EMAIL = 'messages@example.com'

ROOT_URLCONF = "web.urls"

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
    #'django_authopenid.context_processors.authopenid',
    'djangobb_forum.context_processors.forum_settings',
    'django.contrib.messages.context_processors.messages',
    'game.gamesrc.oasis.web.context_processors.include_login_form',
)))

MEDIA_ROOT = os.path.join(GAME_DIR, "gamesrc", "oasis", "web", "media")
STATIC_ROOT = os.path.join(GAME_DIR, "gamesrc", "oasis", "web", "static") 

SERVE_MEDIA = False

MEDIA_URL = '/media/'

STATIC_URL = '/static/'

INSTALLED_APPS = (
    'south',
    'src.server',
    'src.typeclasses',
    'src.players',
    'src.objects',
    'src.comms',
    'src.help',
    'src.scripts',
    'django_notify',
    'mptt',
    'sekizai',
    'sorl.thumbnail',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'django.contrib.markup',
    'pagination',
    'django_authopenid',
    'djangobb_forum',
    'haystack',
    'wiki',
    'wiki.plugins.attachments',
    'wiki.plugins.notifications',
    'wiki.plugins.images',
    'wiki.plugins.macros',
    'character',
    'roster',
    'captcha',
    'dajaxice',
    'dajax',
    'bootstrap_toolkit',
    'widget_tweaks',)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'dajaxice.finders.DajaxiceFinder',
)

MIDDLEWARE_CLASSES = (
    #'sslify.middleware.SSLifyMiddleware',
    'pagination.middleware.PaginationMiddleware',
) + MIDDLEWARE_CLASSES

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = False

# DjangoBB settings
DJANGOBB_GRAVATAR_SUPPORT = False
GRAVATAR_DEFAULT = 'identicon'
USE_TZ = True
TIME_ZONE = "America/Chicago"
DJANGOBB_DEFAULT_MARKUP = 'markdown'

# Haystack settings
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(GAME_DIR, 'gamesrc', 'oasis', 'web', 'djangobb_index'),
        'STORAGE': 'file',
        'POST_LIMIT': 128 * 1024 * 1024,
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 100,
        'EXCLUDED_INDEXES': ['thirdpartyapp.search_indexes.BarIndex'],
    },
}
HAYSTACK_WHOOSH_PATH = os.path.join(GAME_DIR, 'gamesrc', 'oasis', 'web', 'djangobb_index')

TEMPLATE_CONTEXT_PROCESSORS = tuple(set(TEMPLATE_CONTEXT_PROCESSORS + (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
)))

TEMPLATE_LOADERS = (
    'templateloaderwithpriorities.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
 ) + TEMPLATE_LOADERS

TEMPLATE_LOADER_PRIORITIES = [
    os.path.join(GAME_DIR, 'gamesrc', 'oasis', 'web', 'templates')
]

FILE_UPLOAD_PERMISSIONS = 0644

# Character App Settings

# Wiki settings
WIKI_ACCOUNT_HANDLING = False

# DAJAX
DAJAXICE_MEDIA_PREFIX="dajaxice"

# Django REST Framework

