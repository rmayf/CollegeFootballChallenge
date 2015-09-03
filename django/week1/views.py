from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_safe
from leaderboard.models import Picks
from stats.models import Player, Team, Season
from django.http import Http404

from django.http import HttpResponseRedirect

def fail( req ):
   return render( req, 'fail.html', )

def success( req ):
   return render( req, 'success.html', )

@login_required
@require_safe
def index( req ):
   week = 1
   try:
      picks = Picks.objects.get( user=req.user, week=week )
   except Picks.DoesNotExist:
      picks = Picks.objects.create( user=req.user, week=week )
   except Picks.MultipleObjectsReturned:
      raise Http404( 'There are more than 1 pick for the player for the week' ) 
   except:
      raise Http404( 'unknown exception occured, contact rmayf' )

   context = { 'picks' : picks, 'user' : req.user }
   return render( req, 'week_selection.html', context )

@login_required
def roster_team( req, position ):
   if req.method == 'POST':
      id = req.POST.get( 'id', None )
      if len( req.POST.getlist( 'id' ) ) > 1:
         return HttpResponseRedirect( '/fail' )
      if not id:
         return HttpResponseRedirect( '/fail' )
      season = Season.objects.get()
      week = season.currentWeek
      try:
         picks = Picks.objects.get( user=req.user, week=week )
      except Picks.DoesNotExist:
         picks = Picks.objects.create( user=req.user, week=week )
      except Picks.MultipleObjectsReturned:
         raise Http404( 'There are more than 1 pick for the player for the week' ) 
      try:
         if position == 'TK':
            picks.TK = Team.objects.get( id=id )
         elif position == 'TD':
            picks.TD = Team.objects.get( id=id )
      except Team.DoesNotExist:
         return HttpResponseRedirect( '/fail' )
      picks.save()
      return HttpResponseRedirect( '/' )
   else:
      objs = Team.objects.all().values_list( 'name', 'id' )

      context = { 'set' : objs, 'position': position }
      return render( req, 'team.html', context )

@login_required
def roster_player( req, position, **kwargs ):
   if req.method == 'POST':
      ids = req.POST.getlist( 'id' )
      ids_len = len( ids )
      if not ids_len == 2 and not ids[ 0 ] == ids[ 1 ]:
         return HttpResponseRedirect( '/fail/' )
      season = Season.objects.get()
      week = season.currentWeek
      try:
         picks = Picks.objects.get( user=req.user, week=week )
      except Picks.DoesNotExist:
         picks = Picks.objects.create( user=req.user, week=week )
      except Picks.MultipleObjectsReturned:
         raise Http404( 'There are more than 1 pick for the player for the week' ) 
      try:
         if position == 'QB':
            picks.QB1 = Player.objects.get( id=ids[ 0 ] )
            picks.QB2 = Player.objects.get( id=ids[ 1 ] )
         elif position == 'RB':
            picks.RB1 = Player.objects.get( id=ids[ 0 ] )
            picks.RB2 = Player.objects.get( id=ids[ 1 ] )
         elif position == 'WR':
            picks.WR1 = Player.objects.get( id=ids[ 0 ] )
            picks.WR2 = Player.objects.get( id=ids[ 1 ] )
      except Player.DoesNotExist:
         return HttpResponseRedirect( '/fail' )
      picks.save()
      return HttpResponseRedirect( '/' )
   else:
      #I know, I know... this is terrible 
      objs = Player.objects.filter( position=position ).values_list( 'name', 'team__name',
                                                                     'number', 'position', 'id' )
      context = { 'set' : objs, 'position': position }
      return render( req, 'player.html', context )
