import datetime
import re
import scrapy
import unicodedata
from cfbScraper.items import GameItem, PlayerItem, TeamItem

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
      teamSelectorXPath = '//div[@class="mod-container mod-open-list '
      teamSelectorXPath += 'mod-teams-list-medium mod-no-footer"]/'
      teamSelectorXPath +=  'div[@class="mod-header colhead"]/'
      teamSelectorXPath += 'h4[text()="Pac-12"]/../..//li'
      for sel in response.xpath( teamSelectorXPath ):
         teamItem = TeamItem()
         teamIdRegex = '.*?([0-9]+)$'
         scheduleUrl = sel.xpath( 'span/a/@href' ).extract()[ 1 ]
         rosterUrl = sel.xpath( 'span/a/@href' ).extract()[ 2 ]
         teamId = re.match( teamIdRegex, rosterUrl ).group(1)
         teamItem[ 'teamId' ] = teamId
         teamItem[ 'name' ] = sel.xpath( 'h5/a/text()' ).extract()
         yield teamItem
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
         gameItem = GameItem()
         gameItem[ 'teamId' ] =  response.meta[ 'teamId' ]
         opponentUrl = sel.xpath( './/td' )[ 1 ].xpath( './/a/@href' ).extract()[ 0 ]
         gameItem[ 'opponentTeamId' ] = re.match( urlNumRegex, opponentUrl ).group( 1 )
         dateString = unicodedata.normalize( 'NFKD', sel.xpath( './/td/text()' ) \
                         .extract()[ 0 ] ).encode( 'ascii', 'ignore' )
         date = datetime.date( currentYear, monthStrDict[ dateString.split()[ 1 ] ],
                               int( dateString.split()[ 2 ] ) )
         gameItem[ 'week' ] = getGameWeek( date )
         gameItem[ 'date' ] = date 
         yield gameItem 
         
   def parseRosterUrl(self, response):
      playerSelectorXPath = '//table[@class="tablehead"]/tr'
      teamSel = response.xpath( playerSelectorXPath )[ 1 ]
      urlNumRegex = '.*?([0-9]+)'
      teamId = re.match( urlNumRegex, teamSel.xpath( './/a/@href' ).extract()[ 0 ] ).group( 1 )
      for sel in response.xpath( playerSelectorXPath )[ 2 : ]:
         playerItem = PlayerItem()
         playerUrl = sel.xpath( './/td' )[ 1 ].xpath( './/a/@href' ).extract()[ 0 ]
         playerItem[ 'name' ] = sel.xpath( './/td/a/text()' ).extract()
         playerItem[ 'position' ] = sel.xpath( './/td/text()' ).extract()[ 1 ]
         playerItem[ 'teamId' ] = teamId
         playerItem[ 'espnId' ] = re.match( urlNumRegex, playerUrl ).group( 1 )
         if playerItem[ 'position' ] in [ 'QB', 'RB', 'WR' ]:
            yield playerItem
