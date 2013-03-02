from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
#from calorie_bank.views import *
urlpatterns = patterns('',
    url(r'^$', 'calorie_bank.views.home', name='home'),
)
