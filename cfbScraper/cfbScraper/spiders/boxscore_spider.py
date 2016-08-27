import re
import scrapy
import django
from stats.models import DefenseStat, Game, Player, PlayerStat, Team
django.setup()

class BoxscoreSpider( scrapy.Spider ):
	name = "boxscore"
	allowed_domains = ["espn.com"]

	def __init__( self, gameId ):
		try:
			game = Game.objects.get( gameId=gameId )
			awayTeamId = game.opponent.teamId
			homeTeamId = game.team.teamId
			self.week = game.week
		except Game.DoesNotExist:
			# TODO: handle more gracefully
			awayTeamId = -1
			homeTeamId = -1
			self.week = -1
		self.teamIds = [ awayTeamId, homeTeamId ]
		self.start_urls = [ "http://espn.go.com/college-football/boxscore?gameId=%s" % gameId ]

	def parsePlayerPassing( self, playerPassingSel ):
		playerUrl = playerPassingSel.xpath( './/a/@href' ).extract()[ 0 ]
		try:
		   player = Player.objects.get( espnId=re.match( '.*?([0-9]+)', playerUrl ).group( 1 ) )
		except Player.DoesNotExist:
		   return

   		try:
			playerStat = PlayerStat.objects.get( player=player, week=self.week )
			existingScore = playerStat.score
		except PlayerStat.DoesNotExist:
			existingScore = 0
		m = re.match( '([0-9]+)\/([0-9]+)', playerPassingSel \
											   .xpath( ".//td[ @class='c-att' ]/text()" ) \
											   .extract()[ 0 ] )
		completions = m.group( 1 )
		attempts = m.group( 2 )
		passingYards = int( playerPassingSel.xpath( ".//td[ @class='yds' ]/text()" ).extract()[ 0 ] )
		passingTD = int( playerPassingSel.xpath( ".//td[ @class='td' ]/text()" ).extract()[ 0 ] )
		thrownInterceptions = int( playerPassingSel.xpath( ".//td[ @class='int' ]/text()" ).extract()[ 0 ] )
		newScore = 4 * passingTD + 0.04 * passingYards - 2 * thrownInterceptions
		PlayerStat.objects.update_or_create( player=player, week=self.week,
			defaults={ 'completions' : completions, 'attempts' : attempts,
					   'passingYards' : passingYards, 'passingTD' : passingTD,
					   'thrownInterceptions' : thrownInterceptions,
					   'score' : existingScore + newScore } )
		 
	def parsePlayerRushing( self, playerRushingSel ):
		playerUrl = playerRushingSel.xpath( './/a/@href' ).extract()[ 0 ]
		try:
			player = Player.objects.get( espnId=re.match( '.*?([0-9]+)', playerUrl ).group( 1 ) )
		except Player.DoesNotExist:
			return
   		
		try:
			playerStat = PlayerStat.objects.get( player=player, week=self.week )
			existingScore = playerStat.score
		except PlayerStat.DoesNotExist:
			existingScore = 0
		
		rushingTD = int( playerRushingSel.xpath( ".//td[ @class='td' ]/text()" ).extract()[ 0 ] )
		carries = int( playerRushingSel.xpath( ".//td[ @class='car' ]/text()" ).extract()[ 0 ] )
		rushingYards = int( playerRushingSel.xpath( ".//td[ @class='yds' ]/text()" ).extract()[ 0 ] )
		newScore = 6 * rushingTD + 0.1 * rushingYards
		PlayerStat.objects.update_or_create( player=player, week=self.week,
			defaults={ 'rushingTD' : rushingTD, 'carries' : carries,
					   'rushingYards' : rushingYards,
					   'score' : existingScore + newScore } )

	def parsePlayerReceiving( self, playerReceivingSel ):
		playerUrl = playerReceivingSel.xpath( './/a/@href' ).extract()[ 0 ]
		try:
			player = Player.objects.get( espnId=re.match( '.*?([0-9]+)', playerUrl ).group( 1 ) )
		except Player.DoesNotExist:
			return
   		
		try:
			playerStat = PlayerStat.objects.get( player=player, week=self.week )
			existingScore = playerStat.score
		except PlayerStat.DoesNotExist:
			existingScore = 0
		
		receivingTD = int( playerReceivingSel.xpath( ".//td[ @class='td' ]/text()" ).extract()[ 0 ] )
		receptions = int( playerReceivingSel.xpath( ".//td[ @class='rec' ]/text()" ).extract()[ 0 ] )
		receivingYards = int( playerReceivingSel.xpath( ".//td[ @class='yds' ]/text()" ).extract()[ 0 ] )
		newScore = 6 * receivingTD + 0.1 * receivingYards
		PlayerStat.objects.update_or_create( player=player, week=self.week,
			defaults={ 'receivingTD' : receivingTD, 'receptions' : receptions,
					   'receivingYards' : receivingYards,
					   'score' : existingScore + newScore } )
   
	def parsePlayerKicking( self, playerKickingSel ):
		playerUrl = playerKickingSel.xpath( './/a/@href' ).extract()[ 0 ]
		try:
			player = Player.objects.get( espnId=re.match( '.*?([0-9]+)', playerUrl ).group( 1 ) )
		except Player.DoesNotExist:
			return
   		
		try:
			playerStat = PlayerStat.objects.get( player=player, week=self.week )
			existingScore = playerStat.score
		except PlayerStat.DoesNotExist:
			existingScore = 0
		
		kickRegex = '([0-9]+)\/([0-9]+)'
		extraPoints = int( re.match( kickRegex, playerKickingSel.xpath( ".//td[ @class='xp' ]/text()" ).extract()[ 0 ] ).group( 1 ) )
		fieldGoals = int( re.match( kickRegex, playerKickingSel.xpath( ".//td[ @class='fg' ]/text()" ).extract()[ 0 ] ).group( 1 ) )
		newScore = 1 * extraPoints + 3 * fieldGoals
		PlayerStat.objects.update_or_create( player=player, week=self.week,
			defaults={ 'extraPoints' : extraPoints, 'fieldGoals' : fieldGoals,
					   'score' : existingScore + newScore } )
   
	def parseTeamPassing( self, teamPassingSel ):
		for playerPassingSel in teamPassingSel.xpath( ".//tr" )[ : -1 ]:
			self.parsePlayerPassing( playerPassingSel )

	def parseTeamRushing( self, teamRushingSel ):
		for playerRushingSel in teamRushingSel.xpath( ".//tr" )[ : -1 ]:
			self.parsePlayerRushing( playerRushingSel )
   
	def parseTeamReceiving( self, teamReceivingSel ):
		for playerReceivingSel in teamReceivingSel.xpath( ".//tr" )[ : -1 ]:
			self.parsePlayerReceiving( playerReceivingSel )

	def parseTeamKicking( self, teamKickingSel ):
		for playerKickingSel in teamKickingSel.xpath( ".//tr" )[ : -1 ]:
			self.parsePlayerKicking( playerKickingSel )
   
	def parseTeamInterceptions( self, idx, teamInterceptionsSel ):
		try:
			team = Team.objects.get( teamId=self.teamIds[ idx ] )
		except Team.DoesNotExist:
			return
   		
		try:
			defenseStat = DefenseStat.objects.get( team=team, week=self.week )
			existingScore = defenseStat.score
		except DefenseStat.DoesNotExist:
			existingScore = 0

		if len( teamInterceptionsSel.xpath( ".//tr" ) ) > 1: 
			sel = teamInterceptionsSel.xpath( ".//tr" )[ -1 ]
			interceptions = int( sel.xpath( ".//td[ @class='int' ]/text()" ).extract()[ 0 ] )
			interceptionsTD = int( sel.xpath( ".//td[ @class='td' ]/text()" ).extract()[ 0 ] )
			newScore = 2 * interceptions + 6 * interceptionsTD
			DefenseStat.objects.update_or_create( team=team, week=self.week,
				defaults={ 'interceptions' : interceptions,
						  'interceptionsTD' : interceptionsTD,
						  'score' : existingScore + newScore } )
   
	def parseTeamKickReturns( self, idx, teamKickReturnsSel):
		try:
			team = Team.objects.get( teamId=self.teamIds[ idx ] )
		except Team.DoesNotExist:
			return
   		
		try:
			defenseStat = DefenseStat.objects.get( team=team, week=self.week )
			existingScore = defenseStat.score
		except DefenseStat.DoesNotExist:
			existingScore = 0
		
		if len( teamKickReturnsSel.xpath( ".//tr" ) ) > 1:
			sel = teamKickReturnsSel.xpath( ".//tr" )[ -1 ]
			kickoffTD = int( sel.xpath( ".//td[ @class='td' ]/text()" ).extract()[ 0 ] )
			newScore = 6 * kickoffTD
			DefenseStat.objects.update_or_create( team=team, week=self.week,
				defaults={ 'kickoffTD' : kickoffTD, 'score' : existingScore + newScore } )
   
	def parseTeamPuntReturns( self, idx, teamPuntReturnsSel ):
		try:
			team = Team.objects.get( teamId=self.teamIds[ idx ] )
		except Team.DoesNotExist:
			return
   		
		try:
			defenseStat = DefenseStat.objects.get( team=team, week=self.week )
			existingScore = defenseStat.score
		except DefenseStat.DoesNotExist:
			existingScore = 0
		
		if len( teamPuntReturnsSel.xpath( ".//tr" ) ) > 1:
			sel = teamPuntReturnsSel.xpath( ".//tr" )[ -1 ]
			puntTD = int( sel.xpath( ".//td[ @class='td' ]/text()" ).extract()[ 0 ] )
			newScore = 6 * puntTD
			DefenseStat.objects.update_or_create( team=team, week=self.week,
				defaults={ 'puntTD' : puntTD, 'score' : existingScore + newScore } )

	def parseTeamPointsAgainst( self, idx, teamPointsAgainstSel ):
		try:
			team = Team.objects.get( teamId=self.teamIds[ 0 if idx else 1 ] )
		except Team.DoesNotExist:
			return

		try:
			defenseStat = DefenseStat.objects.get( team=team, week=self.week )
			existingScore = defenseStat.score
		except DefenseStat.DoesNotExist:
			existingScore = 0

		pointsAgainst = int( teamPointsAgainstSel.extract() )
		if pointsAgainst == 0:
			newScore = 10
		elif pointsAgainst < 7:
			newScore = 8
		elif pointsAgainst < 14:
			newScore = 6
		elif pointsAgainst < 21:
			newScore = 4
		elif pointsAgainst < 28:
			newScore = 2
		elif pointsAgainst < 35:
			newScore = 1
		elif pointsAgainst < 42:
			newScore = 0
		elif pointsAgainst < 49:
			newScore = -2
		else:
			newScore = -4
		DefenseStat.objects.update_or_create( team=team, week=self.week,
			defaults={ 'pointsAgainst' : pointsAgainst, 'score' : existingScore + newScore } )
   
	def parse(self, response):
		boxscoresSel = response.xpath( '//div[ @id="gamepackage-box-score" ]' )
		for teamPassingSel in boxscoresSel.xpath( ".//div[ @id='gamepackage-passing' ]//tbody" ):
			self.parseTeamPassing( teamPassingSel )
		for teamRushingSel in boxscoresSel.xpath( ".//div[ @id='gamepackage-rushing' ]//tbody" ):
			self.parseTeamRushing( teamRushingSel )
		for teamReceivingSel in boxscoresSel.xpath( ".//div[ @id='gamepackage-receiving' ]//tbody" ):
			self.parseTeamReceiving( teamReceivingSel )
		for teamKickingSel in boxscoresSel.xpath( ".//div[ @id='gamepackage-kicking' ]//tbody" ):
			self.parseTeamKicking( teamKickingSel )
		for idx, teamInterceptionsSel in enumerate( boxscoresSel.xpath( ".//div[ @id='gamepackage-interceptions' ]//tbody" ) ):
			self.parseTeamInterceptions( idx, teamInterceptionsSel )
		for idx, teamKickReturnsSel in enumerate( boxscoresSel.xpath( ".//div[ @id='gamepackage-kickReturns' ]//tbody" ) ):
			self.parseTeamKickReturns( idx, teamKickReturnsSel )
		for idx, teamPuntReturnsSel in enumerate( boxscoresSel.xpath( ".//div[ @id='gamepackage-puntReturns' ]//tbody" ) ):
			self.parseTeamPuntReturns( idx, teamPuntReturnsSel )

		# Parse points against for defensestat
		for idx, teamPointsAgainstSel in enumerate( response.xpath( "//td[ @class='final-score' ]/text()" ) ):
			self.parseTeamPointsAgainst( idx, teamPointsAgainstSel )

