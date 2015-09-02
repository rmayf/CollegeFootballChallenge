from django.db import models

class Team( models.Model ):
   name = models.CharField( max_length=100 )
   espnId = models.IntegerField( default=0 )

   def __str__( self ):
      return self.name

class Game( models.Model ):
   team = models.ForeignKey( Team, related_name='team' )
   opponent = models.ForeignKey( Team, related_name='opponent' )
   date = models.DateTimeField()

   def __str__( self ):
      return '%s@%s' % ( self.opponent, self.team )

class Week( models.Model ):
   index = models.IntegerField( default=0 )
   games = models.ForeignKey( Game )

   def __str__( self ):
      return 'Week%d' % self.index
   
class Season( models.Model ):
   weeks = models.ForeignKey( Week )
   currentWeek = IntegerField( default=0 )

class Player( models.Model ):
   name = models.CharField( max_length=100 )
   team = models.ForeignKey( Team )
   number = models.IntegerField( default=0 )
   position = models.CharField( max_length=20 )

   def __str__( self ):
      return self.name

class PlayerStat( models.Model ):
   player = models.ForeignKey( Player )
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

   def __str__( self ):
      return self.player.name

class TeamStat( models.Model ):
   team = models.ForeignKey( Team )
   FG = models.IntegerField( default=0 )
   FGAttempts = models.IntegerField( default=0 )
   PAT = models.IntegerField( default=0 )
   PATAttempts = models.IntegerField( default=0 )
   pointsAllowed = models.IntegerField( default=0 )

   def __str__( self ):
      return self.team.name
