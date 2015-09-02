from django.conf.urls import include, url

from . import views as stats_views

urlpatters = [
   url( r'^$', stats_views.index ),
]
