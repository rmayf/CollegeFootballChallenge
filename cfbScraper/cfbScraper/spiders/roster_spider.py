import datetime
import re
import scrapy
import unicodedata
from cfbScraper.items import GameItem, PlayerItem, TeamItem
from stats.models import Game, Player, Team
import django
django.setup()

currentYear = 2015
monthStrDict = { 'Aug' : 8, 'Sept' : 9, 'Oct' : 10, 'Nov' : 11, 'Dec' : 12 }
weekStartMonthDays = [ ( 8, 31 ), ( 9, 7 ), ( 9, 14 ), ( 9, 21 ), ( 9, 28 ),
                       ( 10, 5 ), ( 10, 12 ), ( 10, 19 ), ( 10, 26 ),
                       ( 11, 2 ), ( 11, 9 ), ( 11, 16 ), ( 11, 23 ), ( 11, 30 ) ] 
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
         dateString = unicodedata.normalize( 'NFKD', sel.xpath( './/td/text()' ) \
                         .extract()[ 0 ] ).encode( 'ascii', 'ignore' )
         date = datetime.date( currentYear, monthStrDict[ dateString.split()[ 1 ] ],
                               int( dateString.split()[ 2 ] ) )
         week = getGameWeek( date )
         # TODO: Handle case where game hasn't happened yet, what to do with gameId?
         recapUrl = sel.xpath( './/td' )[ 2 ].xpath( './/a/@href' ).extract()[ 0 ]
         gameId = re.match( urlNumRegex, recapUrl ).group( 1 )
         # Check if game is already in DB with team/opponent flipped, create new game if not
         try:
            game = Game.objects.get( team=opponent, opponent=team )
         except Game.DoesNotExist:
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
            player = Player.objects.get_or_create( name=name, position=position, espnId=espnId, team=team )
