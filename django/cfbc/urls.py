"""cfbc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from leaderboard.views import *
from rest_framework.authtoken import views as rest_views

router = DefaultRouter()
router.register( r'users', UserViewSet )
router.register( r'userConfig', UserConfigViewSet )
#router.register( r'picks', PicksViewSet )

urlpatterns = [
   url( r'^admin/', include( admin.site.urls ) ),
   url( r'^', include( router.urls ) ),
   url( r'^auth/', rest_views.obtain_auth_token ), 
]
