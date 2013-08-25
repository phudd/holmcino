from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'player.views.home', name='player_home'),
    url(r'^login$', 'player.views.login', name='player_login'),	
    url(r'^create$', 'player.views.create', name='player_create'),
)
