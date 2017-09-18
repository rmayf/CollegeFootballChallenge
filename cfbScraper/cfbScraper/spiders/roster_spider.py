import datetime
import calendar
import re
import scrapy
import unicodedata
from cfbScraper.items import GameItem, PlayerItem, TeamItem
from stats.models import Game, Player, Team, Season
import django
django.setup()

now = datetime.datetime.now()
currentYear = now.year
months = list( calendar.month_abbr )

def getGameWeek( date ):
	return int( Season.objects.get().currentWeek )

class RosterSpider(scrapy.Spider):
	name = "roster"
	allowed_domains = ["espn.com"]
	start_urls = [ "http://espn.go.com/college-football/teams" ]
   
	def parse(self, response):
		for confSel in response.xpath( "//div[ @class='mod-header colhead' ]" ):
			conference = confSel.xpath( 'h4/text()' ).extract()[ 0 ]
			for team in confSel.xpath( '..//li' ):
				teamIdRegex = '.*?([0-9]+)$'
				links = team.xpath( 'span/a/@href' ).extract()
				scheduleUrl = links[ 1 ]
				teamId = re.match( teamIdRegex, scheduleUrl ).group( 1 )
				name = team.xpath( 'h5/a/text()' ).extract()[ 0 ]
				self.logger.info( "Creating a team object for team: " + name )
				teamItem = Team.objects.get_or_create( teamId=teamId, name=name,
													   conference=conference )
				# only grab player and schedule data from pac12 teams
				if conference.startswith( 'Pac-12' ):
					rosterUrl = links[ 2 ]
					request = scrapy.Request( 'http://espn.go.com' + scheduleUrl,
											  callback=self.parseScheduleUrl,
											  dont_filter=True )
					request.meta[ 'teamId' ] = teamId
					yield request 
					yield scrapy.Request( 'http://espn.go.com' + rosterUrl,
										  callback=self.parseRosterUrl,
										  dont_filter=True )
   
	def parseScheduleUrl(self, response):
		urlNumRegex = '.*?([0-9]+)'
		gameSelectorXPath = '//table[@class="tablehead"]/tr'
		for sel in response.xpath( gameSelectorXPath )[ 2 : ]:
			teamId =  response.meta[ 'teamId' ]
			team = Team.objects.get( teamId=teamId )
                        opponentTD = sel.xpath( './/td' )[ 1 ]
			opponentUrl = opponentTD.xpath( './/a/@href' ).extract()[ 0 ]
			opponentTeamId = re.match( urlNumRegex, opponentUrl ).group( 1 )
			opponent = Team.objects.get( teamId=opponentTeamId, )
			self.logger.info( "Parsing schedule for %s, opponent: %s" %
							  ( team.name, opponent.name ) )
			dateString = unicodedata.normalize( 'NFKD', sel.xpath( './/td/text()' ) \
							.extract()[ 0 ] ).encode( 'ascii', 'ignore' )
			date = datetime.date( currentYear, months.index( dateString.split()[ 1 ][ 0:3 ] ),
								  int( dateString.split()[ 2 ] ) )
			week = getGameWeek( date )
			gameId = None
			recapSel = sel.xpath( './/ul[@class="game-schedule"]' ).extract()
			if len( recapSel ) > 1:
				gameId = re.match( urlNumRegex, recapSel[ 1 ] ).group( 1 )
				self.logger.info( "Game ID is up for %s vs. %s. GameId: %s" %
								  ( team.name, opponent.name, gameId ) )
			else:
				self.logger.info( "Game ID not up yet for %s vs. %s" %
								   ( team.name, opponent.name ) )
			# Check if game is already in DB, create new game if not
                        isHome = opponentTD.css( '.game-status' ).xpath( 'text()' ).extract()[ 0 ] == "vs"
                        home = team if isHome else opponent
                        away = opponent if isHome else team
			try:
				game = Game.objects.get( team=home, opponent=away )
			except Game.DoesNotExist:
				self.logger.info( "Creating game for %s vs. %s" %
								  ( home.name, away.name ) )
				game = Game.objects.get_or_create( team=home, opponent=away, date=date, week=week, gameId=gameId )
				 
	def parseRosterUrl(self, response):
		playerSelectorXPath = '//table[@class="tablehead"]/tr'
		teamSel = response.xpath( playerSelectorXPath )[ 1 ]
		urlNumRegex = '.*?([0-9]+)'
		teamId = re.match( urlNumRegex, teamSel.xpath( './/a/@href' ).extract()[ 0 ] ).group( 1 )
		for sel in response.xpath( playerSelectorXPath )[ 2 : ]:
			playerUrl = sel.xpath( './/td' )[ 1 ].xpath( './/a/@href' ).extract()[ 0 ]
			name = sel.xpath( './/td/a/text()' ).extract()[ 0 ]
			position = sel.xpath( './/td/text()' ).extract()[ 1 ]
			team = Team.objects.get( teamId=teamId )
			self.logger.debug( "Parsing a player for team: %s, name: %s, position: %s" %
							   ( team.name, name, position ) )
			espnId = re.match( urlNumRegex, playerUrl ).group( 1 )
			if position in [ 'QB', 'RB', 'WR', 'PK', 'FB', 'TE' ]:
				# Check is player ID already exists in database
				# (e.g. Troy Williams showing up on both Utah and Washington ESPN rosters
				try:
					player = Player.objects.get( espnId=espnId )
				except Player.DoesNotExist:
					self.logger.info( "Creating player for name: %s, team: %s" %
									  ( name, team.name ) )
					if position == 'FB':
						position = 'RB'
					if position == 'TE':
						position = 'WR'
					player = Player.objects.get_or_create( name=name,
														   position=position,
														   espnId=espnId,
														   team=team )
