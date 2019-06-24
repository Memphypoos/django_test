from django.urls import path, include
from django.conf.urls import url
from django.contrib import admin
from .views import HomePageView, ReadMeView

urlpatterns = [
    url(r'^admin/', admin.site.urls), 
    url('readme',ReadMeView.as_view(), name='readme'),
    url('', HomePageView.as_view(), name='home'), 
]
