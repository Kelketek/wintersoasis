from django.conf.urls import patterns, url
from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(r'^inbox', views.inbox, name="inbox"),
    url(r'^view/(?P<msg_id>\d+)', views.view_message, name="view_message"),
    url(r'^compose', views.compose_message, name="compose"),
    url(r'^delete', views.delete_message, name="trash"),
)
