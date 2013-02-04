from django.conf.urls import patterns, url
from django.conf.urls.defaults import *
from character import views

urlpatterns = patterns('',
    url(r'^profile/(?P<username>[^/]+)/$', views.profile, name="profile"),
    url(r'^switch/', views.switch, name="switch"),
    url(r'^autocomplete/user', views.character_lookup, name="character_lookup"),
)
