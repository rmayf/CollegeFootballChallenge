import re
import scrapy
from cfbScraper.items import PlayerItem

class PlayerSpider(scrapy.Spider):
   name = "player"
   allowed_domains = ["espn.com"]
   # TODO: instead of hardcoding 12 team roster links, get it dynamically frpm team scraper's IDs
   start_urls = [ "http://espn.go.com/ncf/teams/roster?teamId=12",
                  "http://espn.go.com/ncf/teams/roster?teamId=9",
                  "http://espn.go.com/ncf/teams/roster?teamId=25",
                  "http://espn.go.com/ncf/teams/roster?teamId=38",
                  "http://espn.go.com/ncf/teams/roster?teamId=2483",
                  "http://espn.go.com/ncf/teams/roster?teamId=204",
                  "http://espn.go.com/ncf/teams/roster?teamId=24",
                  "http://espn.go.com/ncf/teams/roster?teamId=26",
                  "http://espn.go.com/ncf/teams/roster?teamId=30",
                  "http://espn.go.com/ncf/teams/roster?teamId=254",
                  "http://espn.go.com/ncf/teams/roster?teamId=264",
                  "http://espn.go.com/ncf/teams/roster?teamId=265" ]
   
   def parse(self, response):
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
         
