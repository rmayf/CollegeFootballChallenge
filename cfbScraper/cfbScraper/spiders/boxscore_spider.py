import re
import scrapy
import django
from stats.models import DefenseStat, Game, Player, PlayerStat, Team
django.setup()

class BoxscoreSpider( scrapy.Spider ):
   name = "boxscore"
   allowed_domains = ["espn.com"]

   def __init__( self, gameId ):
      try:
         game = Game.objects.get( gameId=gameId )
         awayTeamId = game.opponent.teamId
         homeTeamId = game.team.teamId
         self.week = game.week
      except Game.DoesNotExist:
         # TODO: handle more gracefully
         awayTeamId = -1
         homeTeamId = -1
         self.week = -1
      self.teamIds = [ awayTeamId, homeTeamId ]
      self.start_urls = [ "http://espn.go.com/college-football/boxscore?gameId=%s" % gameId ]

   def parsePlayerPassing( self, playerPassingSel ):
      playerUrl = playerPassingSel.xpath( './/a/@href' ).extract()[ 0 ]
      try:
         player = Player.objects.get( espnId=re.match( '.*?([0-9]+)', playerUrl ).group( 1 ) )
      except Player.DoesNotExist:
         return
      m = re.match( '([0-9]+)\/([0-9]+)', playerPassingSel \
                                             .xpath( ".//td[ @class='c-att' ]/text()" ) \
                                             .extract()[ 0 ] )
      completions = m.group( 1 )
      attempts = m.group( 2 )
      passingYards = playerPassingSel.xpath( ".//td[ @class='yds' ]/text()" ).extract()[ 0 ]
      passingTD = playerPassingSel.xpath( ".//td[ @class='td' ]/text()" ).extract()[ 0 ]
      thrownInterceptions = playerPassingSel.xpath( ".//td[ @class='int' ]/text()" ).extract()[ 0 ]
      playerStat = PlayerStat.objects.get_or_create( player=player, week=self.week,
                      completions=completions, attempts=attempts, passingYards=passingYards,
                      passingTD=passingTD, thrownInterceptions=thrownInterceptions )
 
   def parsePlayerRushing( self, playerRushingSel ):
      playerUrl = playerRushingSel.xpath( './/a/@href' ).extract()[ 0 ]
      try:
         player = Player.objects.get( espnId=re.match( '.*?([0-9]+)', playerUrl ).group( 1 ) )
      except Player.DoesNotExist:
         return
      TD = playerRushingSel.xpath( ".//td[ @class='td' ]/text()" ).extract()[ 0 ]
      carries = playerRushingSel.xpath( ".//td[ @class='car' ]/text()" ).extract()[ 0 ]
      yards = playerRushingSel.xpath( ".//td[ @class='yds' ]/text()" ).extract()[ 0 ]
      playerStat = PlayerStat.objects.get_or_create( player=player, week=self.week, TD=TD,
                                                     carries=carries, yards=yards )

   def parsePlayerReceiving( self, playerReceivingSel ):
      playerUrl = playerReceivingSel.xpath( './/a/@href' ).extract()[ 0 ]
      try:
         player = Player.objects.get( espnId=re.match( '.*?([0-9]+)', playerUrl ).group( 1 ) )
      except Player.DoesNotExist:
         return
      TD = playerReceivingSel.xpath( ".//td[ @class='td' ]/text()" ).extract()[ 0 ]
      receptions = playerReceivingSel.xpath( ".//td[ @class='rec' ]/text()" ).extract()[ 0 ]
      yards = playerReceivingSel.xpath( ".//td[ @class='yds' ]/text()" ).extract()[ 0 ]
      playerStat = PlayerStat.objects.get_or_create( player=player, week=self.week, TD=TD,
                                                     receptions=receptions, yards=yards )
   
   def parsePlayerKicking( self, playerKickingSel ):
      playerUrl = playerKickingSel.xpath( './/a/@href' ).extract()[ 0 ]
      try:
         player = Player.objects.get( espnId=re.match( '.*?([0-9]+)', playerUrl ).group( 1 ) )
      except Player.DoesNotExist:
         return
      kickRegex = '([0-9]+)\/([0-9]+)'
      extraPoints = re.match( kickRegex, playerKickingSel.xpath( ".//td[ @class='xp' ]/text()" ).extract()[ 0 ] ).group( 1 )
      fieldGoals = re.match( kickRegex, playerKickingSel.xpath( ".//td[ @class='fg' ]/text()" ).extract()[ 0 ] ).group( 1 )
      playerStat = PlayerStat.objects.get_or_create( player=player, week=self.week, extraPoints=extraPoints,
                                                     fieldGoals=fieldGoals )
   
   def parseTeamPassing( self, teamPassingSel ):
      for playerPassingSel in teamPassingSel.xpath( ".//tr" )[ : -1 ]:
         self.parsePlayerPassing( playerPassingSel )

   def parseTeamRushing( self, teamRushingSel ):
      for playerRushingSel in teamRushingSel.xpath( ".//tr" )[ : -1 ]:
         self.parsePlayerRushing( playerRushingSel )
   
   def parseTeamReceiving( self, teamReceivingSel ):
      for playerReceivingSel in teamReceivingSel.xpath( ".//tr" )[ : -1 ]:
         self.parsePlayerReceiving( playerReceivingSel )

   def parseTeamKicking( self, teamKickingSel ):
      for playerKickingSel in teamKickingSel.xpath( ".//tr" )[ : -1 ]:
         self.parsePlayerKicking( playerKickingSel )
   
   def parseTeamInterceptions( self, idx, teamInterceptionsSel ):
      try:
         team = Team.objects.get( teamId=self.teamIds[ idx ] )
      except Team.DoesNotExist:
         return
      if len( teamInterceptionsSel.xpath( ".//tr" ) ) > 1: 
         sel = teamInterceptionsSel.xpath( ".//tr" )[ -1 ]
         interceptions = sel.xpath( ".//td[ @class='int' ]/text()" ).extract()[ 0 ]
         interceptionsTD = sel.xpath( ".//td[ @class='td' ]/text()" ).extract()[ 0 ]
         defenseStat = DefenseStat.objects.get_or_create( team=team, week=self.week, interceptions=interceptions, interceptionsTD=interceptionsTD )
   
   def parseTeamKickReturns( self, idx, teamKickReturnsSel):
      try:
         team = Team.objects.get( teamId=self.teamIds[ idx ] )
      except Team.DoesNotExist:
         return
      if len( teamKickReturnsSel.xpath( ".//tr" ) ) > 1:
         sel = teamKickReturnsSel.xpath( ".//tr" )[ -1 ]
         kickoffTD = sel.xpath( ".//td[ @class='td' ]/text()" ).extract()[ 0 ]
         defenseStat = DefenseStat.objects.get_or_create( team=team, week=self.week, kickoffTD=kickoffTD )
   
   def parseTeamPuntReturns( self, idx, teamPuntReturnsSel ):
      try:
         team = Team.objects.get( teamId=self.teamIds[ idx ] )
      except Team.DoesNotExist:
         return
      if len( teamPuntReturnsSel.xpath( ".//tr" ) ) > 1:
         sel = teamPuntReturnsSel.xpath( ".//tr" )[ -1 ]
         puntTD = sel.xpath( ".//td[ @class='td' ]/text()" ).extract()[ 0 ]
         defenseStat = DefenseStat.objects.get_or_create( team=team, week=self.week, puntTD=puntTD )
   
   def parse(self, response):
      boxscoresSel = response.xpath( "//article[ @data-behavior='boxscore_tabs' ]" )
      for teamPassingSel in boxscoresSel.xpath( ".//div[ @id='gamepackage-passing' ]//tbody" ):
         self.parseTeamPassing( teamPassingSel )
      for teamRushingSel in boxscoresSel.xpath( ".//div[ @id='gamepackage-rushing' ]//tbody" ):
         self.parseTeamRushing( teamRushingSel )
      for teamReceivingSel in boxscoresSel.xpath( ".//div[ @id='gamepackage-receiving' ]//tbody" ):
         self.parseTeamReceiving( teamReceivingSel )
      for teamKickingSel in boxscoresSel.xpath( ".//div[ @id='gamepackage-kicking' ]//tbody" ):
         self.parseTeamKicking( teamKickingSel )
      for idx, teamInterceptionsSel in enumerate( boxscoresSel.xpath( ".//div[ @id='gamepackage-interceptions' ]//tbody" ) ):
         self.parseTeamInterceptions( idx, teamInterceptionsSel )
      for idx, teamKickReturnsSel in enumerate( boxscoresSel.xpath( ".//div[ @id='gamepackage-kickReturns' ]//tbody" ) ):
         self.parseTeamKickReturns( idx, teamKickReturnsSel )
      for idx, teamPuntReturnsSel in enumerate( boxscoresSel.xpath( ".//div[ @id='gamepackage-puntReturns' ]//tbody" ) ):
         self.parseTeamPuntReturns( idx, teamPuntReturnsSel )
