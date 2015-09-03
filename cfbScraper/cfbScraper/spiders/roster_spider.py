import re
import scrapy
from cfbScraper.items import PlayerItem, TeamItem

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
         rosterUrl = sel.xpath( 'span/a/@href' ).extract()[ 2 ]
         teamItem[ 'espnId' ] = re.match( teamIdRegex, rosterUrl ).group(1)
         teamItem[ 'name' ] = sel.xpath( 'h5/a/text()' ).extract()
         yield teamItem
         yield scrapy.Request( 'http://espn.go.com' + rosterUrl,
                               callback=self.parseRosterUrl,
                               dont_filter=True )
         
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
         
