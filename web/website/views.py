
"""
This file contains the generic, assorted views that don't fall under one of
the other applications. Views are django's way of processing e.g. html
templates on the fly.

"""
from django.shortcuts import render_to_response
from django.template import RequestContext
#from django.contrib.auth.models import User
from django.conf import settings

#from src.objects.models import ObjectDB
#from src.typeclasses.models import TypedObject
#from src.players.models import PlayerDB
from src.web.news.models import NewsEntry

from djangobb_forum.templatetags import forum_extras

_BASE_CHAR_TYPECLASS = settings.BASE_CHARACTER_TYPECLASS

def page_index(request):
    """
    Main root page.
    """
    # Some misc. configurable stuff.
    # TODO: Move this to either SQL or settings.py based configuration.

    # A QuerySet of recent news entries.
    news_entries = NewsEntry.objects.all().order_by('-date_posted')[:fpage_news_entries]
    pagevars = {
        "page_title": "Front Page",
        "news_entries": news_entries,
    }

    context_instance = RequestContext(request)
    return render_to_response('index.html', pagevars, context_instance)

def to_be_implemented(request):
    """
    A notice letting the user know that this particular feature hasn't been
    implemented yet.
    """

    pagevars = {
        "page_title": "To Be Implemented...",
    }

    context_instance = RequestContext(request)
    return render_to_response('tbi.html', pagevars, context_instance)


