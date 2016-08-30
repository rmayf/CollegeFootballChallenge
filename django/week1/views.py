from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_safe
from leaderboard.models import Picks
from stats.models import Player, Team, Season, PlayerStat, DefenseStat, Game
from django.http import Http404

from django.http import HttpResponseRedirect
from django.utils import timezone

from datetime import datetime

PAC = "Pac-12"
THURSDAY = 3

@login_required
def myPicks( req ):
   week = Season.objects.all()[ 0 ].currentWeek
   picks = Picks.objects.get_or_create( week=week, user=req.user )[ 0 ]
   # If it's past the deadline, just show your picks
   now = datetime.now()
   if ( now.weekday() == THURSDAY and now >= datetime( now.year, now.month, now.day, 17 ) ) or now.weekday() > THURSDAY: 
      closedPickList = []
      if picks.QB1:
         closedPickList.append( { "id": 1, "position": "QB", "name": picks.QB1.name } )
      if picks.QB2:
         closedPickList.append( { "id": 2, "position": "QB", "name": picks.QB2.name } )
      if picks.RB1:
         closedPickList.append( { "id": 3, "position": "RB", "name": picks.RB1.name } )
      if picks.RB2:
         closedPickList.append( { "id": 4, "position": "RB", "name": picks.RB2.name } )
      if picks.WR1:
         closedPickList.append( { "id": 5, "position": "WR", "name": picks.WR1.name } )
      if picks.WR2:
         closedPickList.append( { "id": 6, "position": "WR", "name": picks.WR2.name } )
      if picks.TD:
         closedPickList.append( { "id": 7, "position": "TD", "name": picks.TD.name } )
      if picks.PK:
         closedPickList.append( { "id": 8, "position": "PK", "name": picks.PK.name } )
      return render( req, "picksLocked.html", { "picks": closedPickList,
                                                "week": week } )
   if req.method == 'POST':
      qb1 = req.POST.get( 'QB1' )
      if qb1 == '':
         qb1 = None
      qb2 = req.POST.get( 'QB2' ) 
      if qb2 == '':
         qb2 = None
      rb1 = req.POST.get( 'RB1' ) 
      if rb1 == '':
         rb1 = None
      rb2 = req.POST.get( 'RB2' ) 
      if rb2 == '':
         rb2 = None
      wr1 = req.POST.get( 'WR1' ) 
      if wr1 == '':
         wr1 = None
      wr2 = req.POST.get( 'WR2' ) 
      if wr2 == '':
         wr2 = None
      pk = req.POST.get( 'PK' ) 
      if pk == '':
         pk = None
      td = req.POST.get( 'TD' ) 
      if td == '':
         td = None
      # Make sure picks are valid
      # Can't pick the same player twice
      if qb1 and qb1 == qb2:
         return HttpResponseRedirect( '/myPicks#error' )
      if wr1 and wr1 == wr2:
         return HttpResponseRedirect( '/myPicks#error' )
      if rb1 and rb1 == rb2:
         return HttpResponseRedirect( '/myPicks#error' )
      # playerIDs must be valid
      # must have picked a player for the proper position
      try:
         if qb1:
            qb1 = Player.objects.get( espnId=qb1 )
            if qb1.position != 'QB':
               return HttpResponseRedirect( '/myPicks#error' )
         if qb2:
            qb2 = Player.objects.get( espnId=qb2 )
            if qb2.position != 'QB':
               return HttpResponseRedirect( '/myPicks#error' )
         if rb1:
            rb1 = Player.objects.get( espnId=rb1 )
            if rb1.position != 'RB':
               return HttpResponseRedirect( '/myPicks#error' )
         if rb2:
            rb2 = Player.objects.get( espnId=rb2 )
            if rb2.position != 'RB':
               return HttpResponseRedirect( '/myPicks#error' )
         if wr1:
            wr1 = Player.objects.get( espnId=wr1 )
            if wr1.position != 'WR':
               return HttpResponseRedirect( '/myPicks#error' )
         if wr2:
            wr2 = Player.objects.get( espnId=wr2 )
            if wr2.position != 'WR':
               return HttpResponseRedirect( '/myPicks#error' )
         if pk:
            pk = Player.objects.get( espnId=pk )
            if pk.position != 'PK':
               return HttpResponseRedirect( '/myPicks#error' )
         if td:
            td = Team.objects.get( teamId=td )
      except Player.DoesNotExist, Team.DoesNotExist:
         return HttpResponseRedirect( '/myPicks#error' )
      # Update picks
      picks.QB1 = qb1 if qb1 else picks.QB1
      picks.QB2 = qb2 if qb2 else picks.QB2
      picks.RB1 = rb1 if rb1 else picks.RB1
      picks.RB2 = rb2 if rb2 else picks.RB2
      picks.WR1 = wr1 if wr1 else picks.WR1
      picks.WR2 = wr2 if wr2 else picks.WR2
      picks.PK = pk if pk else picks.PK
      picks.TD = td if td else picks.TD
      picks.save()
      return HttpResponseRedirect( '/myPicks#success' )
   else: 
      teams = Team.objects.filter( conference=PAC ).order_by( "name" )
      td = {}
      for team in teams:
         stats = DefenseStat.objects.filter( team=team ).order_by( "week" )
	 try:
	    opp = Game.objects.get( team=team, week=week )
	    opp = opp.opponent.name
	 except Game.DoesNotExist:
	    opp = "BYE"
         lastWeek = None
         for stat in stats:
            if stat.week == week -1:
               lastWeek = stat
         if lastWeek:
            scoreSum = sum( map( lambda stat: stat.score, stats ) )
            avg = scoreSum / len( stats )
            stats = { 'kickoffTD': lastWeek.kickoffTD,
                      'puntTD': lastWeek.puntTD,
                      'interceptionsTD': lastWeek.interceptionsTD,
                      'interceptions': lastWeek.interceptions,
                      'pointsAgainst': lastWeek.pointsAgainst }
            td[ team.name ] = { 'opp': opp, 'avg': avg, 'last': lastWeek.score, 'total': scoreSum,
                                'stats': stats, 'team': team.name.replace( ' ', '_' ),
                                'id': team.teamId }
         else:
            td[ team.name ] = { 'opp': opp, 'team': team.name.replace( ' ', '_' ),
                                'id': team.teamId }

      players = Player.objects.filter( team__conference=PAC ).order_by( "team", "name" )
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
         lastWeek = None
         for stat in stats:
            if stat.week == week -1:
               lastWeek = stat
         if lastWeek:
	    scoreSum = sum( map( lambda stat: stat.score, stats ) )
	    avg = scoreSum / len( stats )
	    if player.position == 'QB':
	       stats = { 'ca': "%d / %d" % ( lastWeek.completions, lastWeek.attempts ),
			 'passingYards': lastWeek.passingYards,
			 'passingTD': lastWeek.passingTD,
			 'thrownInterceptions': lastWeek.thrownInterceptions,
			 'yards': lastWeek.rushingYards,
			 'TD': lastWeek.rushingTD }
	       qb[ player.name ] = { 'opp': opp, 'avg': avg, 'last': lastWeek.score, 'total': scoreSum,
				     'stats': stats, 'team': player.team.name.replace( ' ', '_' ),
                                     'id': player.espnId }
	    elif player.position == 'RB':
	       stats = { 'TD': lastWeek.rushingTD,
			 'carries': lastWeek.carries,
			 'receptions': lastWeek.receptions,
			 'yards': lastWeek.rushingYards }
	       rb[ player.name ] = { 'opp': opp, 'avg': avg, 'last': lastWeek.score, 'total': scoreSum,
				     'stats': stats, 'team': player.team.name.replace( ' ', '_' ),
                                     'id': player.espnId }
	    elif player.position == 'WR':
	       stats = { 'TD': lastWeek.receivingTD,
			 'carries': lastWeek.carries,
			 'receptions': lastWeek.receptions,
			 'yards': lastWeek.receivingYards }
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
      pickList = []
      def pickList_helper( pick, l, position=None, id=None, team=None ):
         if pick:
            if not position:
               position = pick.position
            if not id:
               id = pick.espnId
            if not team:
               team = pick.team.name.replace( ' ', '_' )
            l.append( { 'position': position,
                        'name': pick.name,
                        'espnId': id,
                        'team': team, } )
      if picks.QB1:
         pickList_helper( picks.QB1, pickList )
      if picks.QB2:
         pickList_helper( picks.QB2, pickList )
      if picks.RB1:
         pickList_helper( picks.RB1, pickList )
      if picks.RB2:
         pickList_helper( picks.RB2, pickList )
      if picks.WR1:
         pickList_helper( picks.WR1, pickList )
      if picks.WR2:
         pickList_helper( picks.WR2, pickList )
      if picks.TD:
         pickList_helper( picks.TD, pickList, position='TD', id=picks.TD.teamId,
                          team=picks.TD.name.replace( ' ', '_' ) )
      if picks.PK:
         pickList_helper( picks.PK, pickList )
      context = { 'picks': pickList, 'posi': { 'qb': qb, 'wr': wr, 'rb': rb,
                                               'pk': pk, 'td': td } }
      return render( req, 'myPicks.html', context )
   
def results( req, week=None ):
   currentWeek = Season.objects.first().currentWeek
   if week is None:
      week = int( currentWeek )
   else:
      week = int( week )
   def helper_player( player ):
      if player:
         playerStat = PlayerStat.objects.get_or_create( player=player, week=week )[ 0 ]
         team = player.team
         now = datetime.now()
         if ( week < currentWeek ) or ( pick.user == req.user ) or ( week == currentWeek and ( ( now.weekday() > THURSDAY ) or ( now.weekday() == THURSDAY and now > datetime( now.year, now.month, now.date, 17 ) ) ) ):
            return { 'name': player.name, 'school': team.name.replace( ' ', '_' ), 'score': playerStat.score }
         else:
            return None
      else:
         return None

   def helper_team( team ):
      if team:
         teamStat = DefenseStat.objects.get_or_create( team=team, week=week )[ 0 ]
         now = datetime.now()
         if ( week < currentWeek ) or ( pick.user == req.user ) or ( week == currentWeek and ( ( now.weekday() > THURSDAY ) or ( now.weekday() == THURSDAY and now > datetime( now.year, now.month, now.date, 17 ) ) ) ):
            return { 'name': team.name, 'school': team.name.replace( ' ', '_' ), 'score': teamStat.score }
         else:
            return None
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
      pickList.append( helper_player( pick.PK ) )
      data.append( { 'name': pick.user.username, 'picks': pickList, 'score': pick.score } )

   context = { 'data': data, 'week': week }
   return render( req, 'results.html', context )


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
      for i in range( 1, 14 ):
         append = '-'
         for pick in userPicks:
            if pick.week == i:
               append = pick.score
         scores.append( append )
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
         if position == 'PK':
            picks.PK = Team.objects.get( id=id )
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
