from django.conf.urls import patterns, url
from character import views

urlpatterns = patterns('',
    url(r'^new/', views.new, name='new'),
    url(r'^activate/(?P<uid>\w+)/(?P<activation_key>\w+)/$', views.activate, name='activate'),
    url(r'^profile/(?P<username>\w+)/$', views.profile, name="profile"),
)
