from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
   url( '^$', views.index, name='week1_index' ),
   url( '^roster/(?P<position>[\w\s]{1,30})$', views.roster, name='manage' ),
]
