import re
import scrapy
from cfbScraper.items import TeamItem

class TeamSpider(scrapy.Spider):
   name = "team"
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
         teamItem[ 'espnId' ] = re.match( teamIdRegex,
                                   sel.xpath( 'span/a/@href' ).extract()[0] ).group(1)
         teamItem[ 'name' ] = sel.xpath( 'h5/a/text()' ).extract()[ 0 ]
         yield teamItem
         
