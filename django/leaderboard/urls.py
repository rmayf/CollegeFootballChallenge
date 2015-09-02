from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
   url( r'^list/$', views.index, name='index' ),
   url( r'^auth/$', rest_views.obtain_auth_token ),
]
