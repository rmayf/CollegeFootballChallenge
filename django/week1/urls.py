from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
   url( r'^$', views.leaderboard, name='week1_index' ),
   url( r'^inDepth/(?P<week>\d{1,2})$', views.inDepth, name='inDepth' ),
   url( r'^login/$', auth_views.login,
        { 'template_name': 'cfbLogin.html' },
        name='cfbLogin' ),
   url( r'^pickPlayer/(?P<position>[\w\s]{1,30})$', views.roster_player, name='manage_player' ),
   url( r'^pickTeam/(?P<position>[\w\s]{1,30})$', views.roster_team, name='manage_team' ),
   url( r'^fail/$', views.fail, name='fail' ),
   url( r'^success/$', views.success, name='success' ),
   url( r'^accounts/settings/$', views.settings, name='settings' ),
   url( r'^myPicks/', views.myPicks, name='my_picks' ),
]
