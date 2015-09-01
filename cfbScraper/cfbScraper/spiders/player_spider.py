import re
import scrapy
from cfbScraper.items import PlayerItem

class PlayerSpider(scrapy.Spider):
   name = "player"
   allowed_domains = ["espn.com"]
   # TODO: instead of hardcoding 12 team roster links, get it dynamically frpm team scraper's IDs
   start_urls = [ "http://espn.go.com/college-football/team/roster/_/id/26/ucla-bruins" ]
   
   def parse(self, response):
      playerSelectorXPath = '//table[@class="tablehead"]/tr'
      teamSel = response.xpath( playerSelectorXPath )[ 1 ]
      urlNumRegex = '.*?([0-9]+)'
      teamId = re.match( urlNumRegex, teamSel.xpath( './/a/@href' ).extract()[ 0 ] ).group( 1 )
      for sel in response.xpath( playerSelectorXPath )[ 2 : ]:
         playerItem = PlayerItem()
         playerUrl = sel.xpath( './/td' )[ 1 ].xpath( './/a/@href' ).extract()[ 0 ]
         playerItem[ 'playerId' ] = re.match( urlNumRegex, playerUrl ).group( 1 )
         playerItem[ 'teamId' ] = teamId
         playerItem[ 'name' ] = sel.xpath( './/td/a/text()' ).extract()
         playerItem[ 'position' ] = sel.xpath( './/td/text()' ).extract()[ 1 ]
         yield playerItem
         
