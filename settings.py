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
    'django_authopenid.context_processors.authopenid',
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
    'django.contrib.markup',
    'registration',
    'pagination',
    'django_authopenid',
    'djangobb_forum',
    'haystack',
    'character',
    'raven.contrib.django',
    'captcha',
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

# DjangoBB settings
DJANGOBB_GRAVATAR_SUPPORT = False
GRAVATAR_DEFAULT = 'identicon'
USE_TZ = True
TIME_ZONE = "America/Chicago"

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

# Character App Settings

AUP = """

Lorem Ipsum
===========

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque tortor nunc, porta luctus fringilla a, ullamcorper sit amet neque. Aenean elementum viverra congue. Sed quis justo lectus. Suspendisse potenti. Fusce mollis sagittis ullamcorper. Mauris volutpat augue metus. Nunc tristique augue eu sem auctor malesuada.

Vestibulum at imperdiet ipsum. Phasellus neque neque, fringilla quis dapibus vel, ultricies quis metus. Fusce dictum mi et lacus dapibus bibendum rhoncus metus rhoncus. Nullam tellus libero, pulvinar id consequat venenatis, rutrum eu tellus. Proin cursus lorem vitae libero tristique ac hendrerit mauris interdum. Nulla mollis venenatis rhoncus. Sed tincidunt, augue vitae congue laoreet, neque tortor tristique risus, id blandit turpis dui a nisi. Morbi vitae velit vel leo eleifend vulputate. In tellus dui, condimentum vel pellentesque vulputate, lacinia in justo. Praesent id lorem ornare ipsum vulputate lobortis.

Moar Lorem Ipsum crap
---------------------
Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Maecenas eu enim sed dui malesuada varius. Curabitur a sollicitudin mauris. Morbi nisi tellus, dapibus ac interdum sit amet, pellentesque vel tellus. Vivamus purus orci, placerat vel hendrerit ac, iaculis quis massa. Donec ultrices mi sit amet turpis blandit faucibus. Etiam libero mauris, adipiscing sit amet porttitor in, viverra venenatis leo.

Aliquam sed nulla elit. Morbi volutpat eleifend quam. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean vitae quam eros. Duis quis orci vel sapien cursus pellentesque. Etiam odio felis, venenatis a elementum eget, tincidunt quis enim. Sed consectetur auctor dictum.

* Stuff
* Things

Fusce rutrum ullamcorper lorem vitae lacinia. Integer vel dui augue. Aenean a erat eget arcu volutpat tempor quis nec urna. Phasellus ultrices, eros ac tincidunt porttitor, magna nunc dapibus nunc, nec rutrum ligula nisi eget mi. Cras blandit vehicula sollicitudin. Nam scelerisque urna nec dui condimentum venenatis. Etiam tincidunt tortor quis velit vehicula vitae blandit turpis consequat. Sed vitae risus dui. Vestibulum eros lectus, volutpat ut porttitor vel, vehicula in nisl. Vivamus faucibus nibh nec elit rhoncus et mollis quam tempor. Nullam a tortor sit amet mauris hendrerit faucibus sit amet non magna. Donec elementum adipiscing dui eu varius. Curabitur dignissim pellentesque sollicitudin. Donec posuere leo in dolor lacinia pharetra. Mauris nunc justo, consequat eget blandit eu, pulvinar vitae nisl. In hac habitasse platea dictumst.
"""

# Wiki settings
WIKI_ACCOUNT_HANDLING = False
