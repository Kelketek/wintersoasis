"""
This structures the (simple) structure of the 
webpage 'application'. 
"""
from django.conf.urls.defaults import *

urlpatterns = patterns('',
   url(r'^$', 'web.webclient.views.webclient'),)
