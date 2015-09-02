from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_safe
from leaderboard.models import Picks
from stats.models import Player, Team
from django.http import Http404

#from django.http import HttpResponse

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
def roster( req, position ):
   #I know, I know... this is terrible 
   position = position.lower()
   if position.startswith( 'quarterback' ):
      position = 'QB'
      querySet = Player.objects.filter( position=position ).values_list( 'name', 'team__name',
                                                                         'number', 'position' )
   elif position.startswith( 'running back' ):
      position = 'RB'
      querySet = Player.objects.filter( position=position )
   elif position.startswith( 'wide receiver' ):
      position = 'WR'
      querySet = Player.objects.filter( position=position )
   elif position.startswith( 'team kicker' ):
      position = 'TK'
      querySet = Team.objects.all()
   elif position.startswith( 'team defense' ):
      position = 'TD'
      querySet = Team.objects.all()
   else:
      raise Http404( 'invalid position: %s' % position )

   context = { 'set' : querySet }
   return render( req, 'roster.html', context )
