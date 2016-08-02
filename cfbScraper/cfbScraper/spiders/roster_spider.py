import datetime
import re
import scrapy
import unicodedata
from cfbScraper.items import GameItem, PlayerItem, TeamItem
from stats.models import Game, Player, Team
import django
django.setup()

currentYear = 2016
monthStrDict = { 'Aug' : 8, 'Sept' : 9, 'Oct' : 10, 'Nov' : 11, 'Dec' : 12 }
weekStartMonthDays = [ ( 8, 29 ), ( 9, 5 ), ( 9, 12 ), ( 9, 19 ), ( 9, 26 ),
                       ( 10, 3 ), ( 10, 10 ), ( 10, 17 ), ( 10, 24 ), ( 10, 31 ),
                       ( 11, 7 ), ( 11, 14 ), ( 11, 21 ), ( 11, 28 ) ]
weekStartDates = [ datetime.date( currentYear, month, day ) for month, day in weekStartMonthDays ]

def getGameWeek( date ):
   # ugly but I'm tired and just want to get this to work
   for idx, val in enumerate( weekStartDates ):
      if date < val:
         return idx
   return -1

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
			opponentUrl = sel.xpath( './/td' )[ 1 ].xpath( './/a/@href' ).extract()[ 0 ]
			opponentTeamId = re.match( urlNumRegex, opponentUrl ).group( 1 )
			opponent = Team.objects.get( teamId=opponentTeamId, )
			self.logger.info( "Parsing schedule for %s, opponent: %s" %
							  ( team.name, opponent.name ) )
			dateString = unicodedata.normalize( 'NFKD', sel.xpath( './/td/text()' ) \
							.extract()[ 0 ] ).encode( 'ascii', 'ignore' )
			date = datetime.date( currentYear, monthStrDict[ dateString.split()[ 1 ] ],
								  int( dateString.split()[ 2 ] ) )
			week = getGameWeek( date )
			gameId = None
			recapSel = sel.xpath( './/td' )[ 2 ].xpath( './/a/@href' ).extract()
			if recapSel and 'recap' in recapSel[ 0 ]:
				self.logger.info( "Game ID is up for %s vs. %s. recapUrl: %s" %
								  ( team.name, opponent.name, recapSel[ 0 ] ) )
				gameId = re.match( urlNumRegex, recapSel[ 0 ] ).group( 1 )
			else:
				self.logger.info( "Game ID not up yet for %s vs. %s" %
								   ( team.name, opponent.name ) )
			# Check if game is already in DB with team/opponent flipped,
			# create new game if not
			try:
				self.logger.info( "Game already exists for %s vs. %s" %
								  ( team.name, opponent.name ) )
				game = Game.objects.get( team=opponent, opponent=team )
			except Game.DoesNotExist:
				self.logger.info( "Creating game for %s vs. %s" %
								  ( team.name, opponent.name ) )
				game = Game.objects.get_or_create( team=team, opponent=opponent,
													  date=date, week=week, gameId=gameId )
				 
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
			espnId = re.match( urlNumRegex, playerUrl ).group( 1 )
			if position in [ 'QB', 'RB', 'WR', 'PK' ]:
				# Check is player ID already exists in database
				# (e.g. Troy Williams showing up on both Utah and Washington ESPN rosters
				try:
					player = Player.objects.get( espnId=espnId )
				except Player.DoesNotExist:
						player = Player.objects.get_or_create( name=name,
															   position=position,
															   espnId=espnId,
															   team=team )
