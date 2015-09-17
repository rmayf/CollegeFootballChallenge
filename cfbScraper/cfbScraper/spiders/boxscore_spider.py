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
      try:
         player = Player.objects.get( espnId=re.match( '.*?([0-9]+)', playerUrl ).group( 1 ) )
      except Player.DoesNotExist:
         return
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
 
   def parsePlayerRushing( self, playerRushingSel ):
      playerUrl = playerRushingSel.xpath( './/a/@href' ).extract()[ 0 ]
      try:
         player = Player.objects.get( espnId=re.match( '.*?([0-9]+)', playerUrl ).group( 1 ) )
      except Player.DoesNotExist:
         return
      week = -1 # TODO
      TD = playerRushingSel.xpath( ".//td[ @class='td' ]/text()" ).extract()[ 0 ]
      carries = playerRushingSel.xpath( ".//td[ @class='car' ]/text()" ).extract()[ 0 ]
      yards = playerRushingSel.xpath( ".//td[ @class='yds' ]/text()" ).extract()[ 0 ]
      playerStat = PlayerStat.objects.get_or_create( player=player, week=week, TD=TD,
                                                     carries=carries, yards=yards )

   def parsePlayerReceiving( self, playerReceivingSel ):
      playerUrl = playerReceivingSel.xpath( './/a/@href' ).extract()[ 0 ]
      try:
         player = Player.objects.get( espnId=re.match( '.*?([0-9]+)', playerUrl ).group( 1 ) )
      except Player.DoesNotExist:
         return
      week = -1 # TODO
      TD = playerReceivingSel.xpath( ".//td[ @class='td' ]/text()" ).extract()[ 0 ]
      yards = playerReceivingSel.xpath( ".//td[ @class='yds' ]/text()" ).extract()[ 0 ]
      playerStat = PlayerStat.objects.get_or_create( player=player, week=week, TD=TD,
                                                     yards=yards )
   
   def parseTeamPassing( self, teamPassingSel ):
      for playerPassingSel in teamPassingSel.xpath( ".//tr" )[ : -1 ]:
         self.parsePlayerPassing( playerPassingSel )

   def parseTeamRushing( self, teamRushingSel ):
      for playerRushingSel in teamRushingSel.xpath( ".//tr" )[ : -1 ]:
         self.parsePlayerRushing( playerRushingSel )
   
   def parseTeamReceiving( self, teamReceivingSel ):
      for playerReceivingSel in teamReceivingSel.xpath( ".//tr" )[ : -1 ]:
         self.parsePlayerReceiving( playerReceivingSel )
   
   def parse(self, response):
      boxscoresSel = response.xpath( "//article[ @data-behavior='boxscore_tabs' ]" )
      for teamPassingSel in boxscoresSel.xpath( ".//div[ @id='gamepackage-passing' ]//tbody" ):
         self.parseTeamPassing( teamPassingSel )
      for teamRushingSel in boxscoresSel.xpath( ".//div[ @id='gamepackage-rushing' ]//tbody" ):
         self.parseTeamRushing( teamRushingSel )
      for teamReceivingSel in boxscoresSel.xpath( ".//div[ @id='gamepackage-receiving' ]//tbody" ):
         self.parseTeamReceiving( teamReceivingSel )
      #  parseInterceptions( boxscoresSel.xpath( ".//div[ @id='gamepackage-interceptions' ]" ) )
      #  parseKickReturns( boxscoresSel.xpath( ".//div[ @id='gamepackage-kickReturns' ]" ) )
      #  parsePuntReturns( boxscoresSel.xpath( ".//div[ @id='gamepackage-puntReturns' ]" ) )
      #  parseKicking( boxscoresSel.xpath( ".//div[ @id='gamepackage-kicking' ]" ) )
      #  parsePunting( boxscoresSel.xpath( ".//div[ @id='gamepackage-punting' ]" ) )
