import re
import scrapy
import django
from stats.models import Player, PlayerStat
django.setup()

class BoxscoreSpider(scrapy.Spider):
   name = "boxscore"
   allowed_domains = ["espn.com"]
   start_urls = [ "http://espn.go.com/college-football/boxscore?gameId=400756904" ]

   def parsePlayerPassing( self, playerPassingSel ):
      playerUrl = playerPassingSel.xpath( './/a/@href' ).extract()[ 0 ]
      player = Player.objects.get( espnId=re.match( '.*?([0-9]+)', playerUrl ).group( 1 ) )
      week = -1 # TODO
      m = re.match( '([0-9]+)\/([0-9]+)', playerPassingSel \
                                             .xpath( ".//td[ @class='c-att' ]/text()" ) \
                                             .extract()[ 0 ] )
      completions = m.group( 1 )
      attempts = m.group( 2 )
      passingYards = playerPassingSel.xpath( ".//td[ @class='yds' ]/text()" ).extract()[ 0 ]
      passingTD = playerPassingSel.xpath( ".//td[ @class='td' ]/text()" ).extract()[ 0 ]
      thrownInterceptions = playerPassingSel.xpath( ".//td[ @class='int' ]/text()" ).extract()[ 0 ]
      playerStat = PlayerStat.objects.get_or_create( player=player, week=week,
                      completions=completions, attempts=attempts, passingYards=passingYards,
                      passingTD=passingTD, thrownInterceptions=thrownInterceptions )
   
   def parseTeamPassing( self, teamPassingSel ):
      for playerPassingSel in teamPassingSel.xpath( ".//tr" )[ : -1 ]:
         self.parsePlayerPassing( playerPassingSel )
   
   def parse(self, response):
      boxscoresSel = response.xpath( "//article[ @data-behavior='boxscore_tabs' ]" )
      passingSel = boxscoresSel.xpath( ".//div[ @id='gamepackage-passing' ]" )
      self.parseTeamPassing( passingSel.xpath( ".//tbody" )[ 1 ] ) # TODO: temp until below todo is resolved 
      # TODO: for OOC games, need to somehow skip processing if player ID is not found in DB
      #for teamPassingSel in passingSel.xpath( ".//tbody" ):
      #   self.parseTeamPassing( teamPassingSel )
      #  parsePassing( boxscoresSel.xpath( ".//div[ @id='gamepackage-passing' ]" ) )
      #  parseRushing( boxscoresSel.xpath( ".//div[ @id='gamepackage-rushing' ]" ) )
      #  parseReceiving( boxscoresSel.xpath( ".//div[ @id='gamepackage-receiving' ]" ) )
      #  parseInterceptions( boxscoresSel.xpath( ".//div[ @id='gamepackage-interceptions' ]" ) )
      #  parseKickReturns( boxscoresSel.xpath( ".//div[ @id='gamepackage-kickReturns' ]" ) )
      #  parsePuntReturns( boxscoresSel.xpath( ".//div[ @id='gamepackage-puntReturns' ]" ) )
      #  parseKicking( boxscoresSel.xpath( ".//div[ @id='gamepackage-kicking' ]" ) )
      #  parsePunting( boxscoresSel.xpath( ".//div[ @id='gamepackage-punting' ]" ) )
