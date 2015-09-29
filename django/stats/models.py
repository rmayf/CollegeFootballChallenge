from django.db import models


class Team( models.Model ):
   teamId = models.IntegerField( default=0, primary_key=True, unique=True )
   name = models.CharField( max_length=100 )
   conference = models.CharField( max_length=100 )

   def __unicode__( self ):
      return self.name

class Game( models.Model ):
   team = models.ForeignKey( Team, default=0 )
   opponent = models.ForeignKey( Team, related_name='opponent', default=0 )
   week = models.IntegerField( default=0 )
   date = models.DateTimeField()
   gameId = models.IntegerField( default=0 )

   def __unicode__( self ):
      return '%s@%s' % ( self.team.name, self.opponent.name )

class Week( models.Model ):
   index = models.IntegerField( default=0 )
   #games = models.ForeignKey( Game )

   def __unicode__( self ):
      return 'Week%d' % self.index
   
class Season( models.Model ):
   #weeks = models.ForeignKey( Week )
   currentWeek = models.IntegerField( default=0 )

class Player( models.Model ):
   name = models.CharField( max_length=100, unique=True )
   position = models.CharField( max_length=20 )
   team = models.ForeignKey( Team, default=0 )
   espnId = models.IntegerField( default=0, primary_key=True, unique=True )

   def __str__( self ):
      return self.name

class PlayerStat( models.Model ):
   player = models.ForeignKey( Player )
   week = models.IntegerField( default=0 )
   # QB-specific
   completions = models.IntegerField( default=0 )
   attempts = models.IntegerField( default=0 )
   passingYards = models.IntegerField( default=0 )
   passingTD = models.IntegerField( default=0 )
   thrownInterceptions = models.IntegerField( default=0 )
   # RB/WR-specific
   TD = models.IntegerField( default=0 )
   carries = models.IntegerField( default=0 )
   receptions = models.IntegerField( default=0 )
   yards = models.IntegerField( default=0 )
   # PK-specific
   extraPoints = models.IntegerField( default=0 )
   fieldGoals = models.IntegerField( default=0 )
   # Final calculted score
   score = models.IntegerField( default=0 )

class DefenseStat( models.Model ):
   team = models.ForeignKey( Team )
   week = models.IntegerField( default=0 )
   # DEF/ST-specific
   kickoffTD = models.IntegerField( default=0 )
   puntTD = models.IntegerField( default=0 )
   interceptionsTD = models.IntegerField( default=0 )
   interceptions = models.IntegerField( default=0 )
   # Final calculted score
   score = models.IntegerField( default=0 )

   def __unicode__( self ):
      return self.player.name
