from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
   url( '^$', views.index, name='week1_index' ),
   url( '^pickPlayer/(?P<position>[\w\s]{1,30})$', views.roster_player, name='manage_player' ),
   url( '^pickTeam/(?P<position>[\w\s]{1,30})$', views.roster_team, name='manage_team' ),
   url( '^fail/$', views.fail, name='fail' ),
   url( '^success/$', views.success, name='success' ),
]
