from django.db import models

class Team( models.Model ):
   name = models.CharField( max_length=100 )
   teamId = models.IntegerField( default=0 )

   def __str__( self ):
      return self.name

class Game( models.Model ):
   awayTeamId = models.IntegerField( default=0 )
   homeTeamId = models.IntegerField( default=0 )
   week = models.IntegerField( default=0 )
   date = models.DateTimeField()

   def __str__( self ):
      return '%s@%s' % ( self.awayTeamId, self.homeTeamId )

class Week( models.Model ):
   index = models.IntegerField( default=0 )
   #games = models.ForeignKey( Game )

   def __str__( self ):
      return 'Week%d' % self.index
   
class Season( models.Model ):
   #weeks = models.ForeignKey( Week )
   currentWeek = models.IntegerField( default=0 )

class Player( models.Model ):
   name = models.CharField( max_length=100 )
   position = models.CharField( max_length=20 )
   teamId = models.IntegerField( default=0 )
   espnId = models.IntegerField( default=0 )

   def __str__( self ):
      return self.name

class PlayerStat( models.Model ):
   player = models.ForeignKey( Player )
   week = models.IntegerField( default=0 )
   completions = models.IntegerField( default=0 )
   attempts = models.IntegerField( default=0 )
   passingYards = models.IntegerField( default=0 )
   passingTD = models.IntegerField( default=0 )
   thrownInterceptions = models.IntegerField( default=0 )
   TD = models.IntegerField( default=0 )
   carries = models.IntegerField( default=0 )
   yards = models.IntegerField( default=0 )
   kickoffTD = models.IntegerField( default=0 )
   puntTD = models.IntegerField( default=0 )
   interceptionsTD = models.IntegerField( default=0 )
   interceptions = models.IntegerField( default=0 )
   receptions = models.IntegerField( default=0 )
   score = models.IntegerField( default=0 )

   def __str__( self ):
      return self.player.name.encode( 'ascii', 'ignore' )

class TeamStat( models.Model ):
   team = models.ForeignKey( Team )
   week = models.IntegerField( default=0 )
   FG = models.IntegerField( default=0 )
   FGAttempts = models.IntegerField( default=0 )
   PAT = models.IntegerField( default=0 )
   PATAttempts = models.IntegerField( default=0 )
   pointsAllowed = models.IntegerField( default=0 )
   score = models.IntegerField( default=0 )

   def __str__( self ):
      return self.team.name.encode( 'ascii', 'ignore' )
