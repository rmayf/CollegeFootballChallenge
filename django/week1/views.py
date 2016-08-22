from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_safe
from leaderboard.models import Picks
from stats.models import Player, Team, Season, PlayerStat, DefenseStat, Game
from django.http import Http404

from django.http import HttpResponseRedirect
from django.utils import timezone

PAC = "Pac-12"

@login_required
def myPicks( req ):
   if req.method == 'POST':
      return HttpResponseRedirect( '/myPicks#success' )
   else: 
      week = Season.objects.all()[ 0 ].currentWeek
      picks = Picks.objects.get_or_create( week=week, user=req.user )
      teams = Team.objects.filter( conference=PAC )
      td = {}
      for team in teams:
         stats = DefenseStat.objects.filter( team=team ).order_by( "week" )
	 try:
	    opp = Game.objects.get( team=team, week=week )
	    opp = opp.opponent.name
	 except Game.DoesNotExist:
	    opp = "BYE"
         if stats:
            scoreSum = sum( map( lambda stat: stat.score, stats ) )
            avg = scoreSum / len( stats )
            lastWeek = list( stats )[ -1 ]
            stats = { 'kickoffTD': lastWeek.kickoffTD,
                      'puntTD': lastWeek.puntTD,
                      'interceptionsTD': lastWeek.interceptionsTD,
                      'interception': lastWeek.interceptions }
            td[ team.name ] = { 'opp': opp, 'avg': avg, 'last': lastWeek.score, 'total': scoreSum,
                                'stats': stats, 'team': team.name.replace( ' ', '_' ),
                                'id': team.teamId }
         else:
            td[ team.name ] = { 'opp': opp, 'team': team.name.replace( ' ', '_' ),
                                'id': team.teamId }

      players = Player.objects.filter( team__conference=PAC )
      qb = {}
      rb = {}
      wr = {}
      pk = {}
      for player in players:
	 stats = PlayerStat.objects.filter( player=player ).order_by( "week" )
	 try:
	    opp = Game.objects.get( team=player.team, week=week )
	    opp = opp.opponent.name
	 except Game.DoesNotExist:
	    opp = "BYE"
	 if stats:
	    scoreSum = sum( map( lambda stat: stat.score, stats ) )
	    avg = scoreSum / len( stats )
	    lastWeek = list( stats )[ -1 ]
	    if player.position == 'QB':
	       stats = { 'ca': "%d / %d" % ( lastWeek.completions, lastWeek.attempts ),
			 'passingYards': lastWeek.passingYards,
			 'passingTD': lastWeek.passingTD,
			 'thrownInterceptions': lastWeek.thrownInterceptions,
			 'yards': lastWeek.yards,
			 'TD': lastWeek.TD }
	       qb[ player.name ] = { 'opp': opp, 'avg': avg, 'last': lastWeek.score, 'total': scoreSum,
				     'stats': stats, 'team': player.team.name.replace( ' ', '_' ),
                                     'id': player.espnId }
	    elif player.position == 'RB':
	       stats = { 'TD': lastWeek.TD,
			 'carries': lastWeek.carries,
			 'receptions': lastWeek.receptions,
			 'yards': lastWeek.yards }
	       rb[ player.name ] = { 'opp': opp, 'avg': avg, 'last': lastWeek.score, 'total': scoreSum,
				     'stats': stats, 'team': player.team.name.replace( ' ', '_' ),
                                     'id': player.espnId }
	    elif player.position == 'WR':
	       stats = { 'TD': lastWeek.TD,
			 'carries': lastWeek.carries,
			 'receptions': lastWeek.receptions,
			 'yards': lastWeek.yards }
	       wr[ player.name ] = { 'opp': opp, 'avg': avg, 'last': lastWeek.score, 'total': scoreSum,
				     'stats': stats, 'team': player.team.name.replace( ' ', '_' ), 
                                     'id': player.espnId }
            elif player.position == 'PK':
               stats = { 'FG': lastWeek.fieldGoals,
                         'PAT': lastWeek.extraPoints }
               pk[ player.name ] = { 'opp': opp, 'avg': avg, 'last': lastWeek.score,
                                     'stats': stats, 'team': player.team.name.replace( ' ', '_' ), 
                                     'id': player.espnId }
	 else:
	    if player.position == 'QB':
	       qb[ player.name ] = { 'opp': opp, 'team': player.team.name.replace( ' ', '_' ),
                                     'id': player.espnId }
	    elif player.position == 'RB':
	       rb[ player.name ] = { 'opp': opp, 'team': player.team.name.replace( ' ', '_' ), 
                                     'id': player.espnId }
	    elif player.position == 'WR':
	       wr[ player.name ] = { 'opp': opp, 'team': player.team.name.replace( ' ', '_' ),
                                     'id': player.espnId }
	    elif player.position == 'PK':
	       pk[ player.name ] = { 'opp': opp, 'team': player.team.name.replace( ' ', '_' ),
                                     'id': player.espnId }

      teamStat = DefenseStat.objects.filter( week=( week - 1 ) )
      context = { 'picks': picks[ 0 ], 'posi': { 'qb': qb, 'wr': wr, 'rb': rb,
                                                 'pk': pk, 'td': td } }
      return render( req, 'myPicks.html', context )
   
def inDepth( req, week ):
   def helper_player( player ):
      if player:
         playerStat = PlayerStat.objects.get_or_create( player=player, week=week )[ 0 ]
         team = player.team
         game = Game.objects.get( team=team, week=week )
         if game.date <= timezone.now() or pick.user == req.user:
            return { 'name': player.name, 'school': team.name.replace( ' ', '_' ), 'score': playerStat.score }
      else:
         return None

   def helper_team( team ):
      if team:
         teamStat = DefenseStat.objects.get_or_create( team=team, week=week )[ 0 ]
         game = Game.objects.get( team=team, week=week )
         if game.date <= timezone.now() or pick.user == req.user:
            return { 'name': team.name, 'school': team.name.replace( ' ', '_' ), 'score': teamStat.score }
      else:
         return None
      
   data = []
   for pick in Picks.objects.filter( week=week ).order_by( 'score' ):
      pickList = []
      pickList.append( helper_player( pick.QB1 ) )
      pickList.append( helper_player( pick.QB2 ) )
      pickList.append( helper_player( pick.RB1 ) )
      pickList.append( helper_player( pick.RB2 ) )
      pickList.append( helper_player( pick.WR1 ) )
      pickList.append( helper_player( pick.WR2 ) )
      pickList.append( helper_team( pick.TD ) )
      pickList.append( helper_team( pick.TK ) )
      data.append( { 'name': pick.user.username, 'picks': pickList, 'score': pick.score } )

   context = { 'data': data, 'week': week }
   return render( req, 'inDepth.html', context )


@login_required
def settings( req ):
   if req.method == 'POST':
      uname = req.POST.get( 'username', None )
      if uname:
         req.user.username = uname
         req.user.save()
         return HttpResponseRedirect( '/' )
      else:
         raise Http404( 'No username specified' ) 
   else:
      return render( req, 'settings.html', )

def login( req ):
   return render( req, 'base.html', )

def fail( req ):
   return render( req, 'fail.html', )

def success( req ):
   return render( req, 'success.html', )

def leaderboard( req ):
   toTemp = []
   for user in User.objects.filter( is_superuser=False, is_active=True, is_staff=False ):
      userPicks = Picks.objects.filter( user=user ).order_by( 'week' )
      total = 0
      scores = []
      for picks in userPicks:
         total += picks.score
      dataIndex = 0
      for i in range( 0, 13 ):
         if dataIndex < len( userPicks ):
            if userPicks[ dataIndex ].week == i:
               scores.append( userPicks[ dataIndex ].score )
               dataIndex += 1
         else:
            scores.append( '-' )
      toTemp.append( { 'name': user.username, 'total': total, 'scores': scores } )
   week = Season.objects.first().currentWeek
   context = { 'data': toTemp,
               'week': week, 
   }
   return render( req, 'leaderboard.html', context )

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
      objs = Player.objects.filter( position=position ).values_list( 'name', 'teamId',
                                                                     'position', 'id' )
      context = { 'set' : objs, 'position': position }
      return render( req, 'player.html', context )
