#
# File that determines what each URL points to. This uses _Python_ regular
# expressions, not Perl's.
#
# See:
# http://diveintopython.org/regular_expressions/street_addresses.html#re.matching.2.3
#

from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic import RedirectView

# Wiki imports
from wiki.urls import get_pattern as get_wiki_pattern
from django_notify.urls import get_pattern as get_notify_pattern

# fix to resolve lazy-loading bug
# https://code.djangoproject.com/ticket/10405#comment:11
#from django.db.models.loading import cache as model_cache
#if not model_cache.loaded:
#    model_cache.get_models()

from djangobb_forum import settings as forum_settings
#from sitemap import SitemapForum, SitemapTopic

#from django.contrib.auth.views import login
#from django.contrib.auth.views import logout
# loop over all settings.INSTALLED_APPS and execute code in 
# files named admin.py in each such app (this will add those
# models to the admin site)
admin.autodiscover()

# Setup the root url tree from / 

# AJAX stuff.
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

urlpatterns = patterns('',
    # User Authentication
    url(r'^login/', 'web.views.login', name="login"),
    url(r'^logout/', 'django.contrib.auth.views.logout', name="logout"),

    url(r'^accounts/login', 'views.login_gateway'),

    # News stuff
    #url(r'^news/', include('src.web.news.urls')),

    # Page place-holder for things that aren't implemented yet.
    url(r'^tbi/', 'game.gamesrc.oasis.web.website.views.to_be_implemented'),
    
    # Admin interface
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    # favicon
    url(r'^favicon\.ico$', RedirectView.as_view(url='/media/images/favicon.ico')),

    # ajax stuff
    url(r'^webclient/',include('game.gamesrc.oasis.web.webclient.urls', namespace="webclient")),

    # Wiki
    url(r'^notify/', get_notify_pattern()),
    url(r'^wiki/', get_wiki_pattern()),

    #(r'^mail/', include('game.gamesrc.oasis.web.mail_urls')),

    # Forum
    (r'^forum/', include('bb_urls', namespace='djangobb')),
    # Favicon
    (r'^favicon\.ico$', RedirectView.as_view(url='/media/images/favicon.ico')),

    # Registration stuff
    url(r'^roster/', include('roster.urls', namespace='roster')),

    # Character related stuff.
    url(r'^character/', include('character.urls', namespace='character')),

    # Mail stuff
    url(r'^mail/', include('mail.urls', namespace='mail')),

    # Search utilities
    url(r'^search/', include('haystack.urls', namespace='search')),

    # AJAX stuff
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^selectable/', include('selectable.urls')),

    # Ticket system
    url(r'^tickets/', include('helpdesk.urls', namespace='helpdesk')),

    url(r'^$', 'views.page_index', name='index'),
)

# 500 Errors:
handler500 = 'web.views.custom_500'
# This sets up the server if the user want to run the Django
# test server (this should normally not be needed).
if settings.SERVE_MEDIA:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
        (r'^wiki/([^/]+/)*wiki/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT + '/wiki/'})
    )

# PM Extension
if (forum_settings.PM_SUPPORT):
    urlpatterns += patterns('',
        (r'^mail/', include('mail_urls')),
   )

if (settings.DEBUG):
    urlpatterns += patterns('',
        (r'^%s(?P<path>.*)$' % settings.MEDIA_URL.lstrip('/'),
            'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
