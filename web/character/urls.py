from django.conf.urls import patterns, url
from django.conf.urls.defaults import *
from character import views

urlpatterns = patterns('',
    url(r'^profile/(?P<username>[^/]+)/$', views.profile, name="profile"),
    url(r'^switch/', views.switch, name="switch"),
    url(r'^mail/inbox', views.inbox, name="inbox"),
    url(r'^mail/view/(?P<msg_id>\d+)', views.view_message, name="view_message"),
    url(r'^mail/compose', views.compose_message, name="compose"),
    url(r'^mail/reply/(\d+)', views.inbox, name="reply"),
    url(r'^mail/delete', views.delete_message, name="trash"),
    url(r'^autocomplete/user', views.character_lookup, name="character_lookup"),
)
