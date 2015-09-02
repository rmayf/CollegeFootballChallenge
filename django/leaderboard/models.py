from django.db import models
from django.contrib.auth.models import User
from stats.models import Player, Team, Week

class SeasonPicks( models.Model ):
   
class Picks( models.Model ):
   
   unique_together = ( ( 'week', 'user' ), )

   week = models.IntegerField( default=0 )
   user = models.ForeignKey( User )
   QB1 = models.ForeignKey( Player, related_name='qb1' )
   QB2 = models.ForeignKey( Player, related_name='qb2' )
   RB1 = models.ForeignKey( Player, related_name='rb1' )
   RB2 = models.ForeignKey( Player, related_name='rb2' )
   WR1 = models.ForeignKey( Player, related_name='wr1' )
   WR2 = models.ForeignKey( Player, related_name='wr2' )
   K = models.ForeignKey( Team, related_name='k' )
   D = models.ForeignKey( Team, related_name='d' )
   score = models.IntegerField( default=0 )

   def __str__( self ):
      return '%s%d' % ( self.user.username, self.week.index )

   # To fix django admin page plural problem
   class Meta:
      verbose_name_plural = 'picks'
