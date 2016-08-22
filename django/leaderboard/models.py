from django.db import models
from django.contrib.auth.models import User
from stats.models import Player, Team, Week
from django.contrib.auth.models import User

class UserStat(models.Model):
   user = models.OneToOneField(User)


class Picks( models.Model ):
   week = models.IntegerField( default=0 )
   user = models.ForeignKey( User )
   QB1 = models.ForeignKey( Player, related_name='qb1', null=True )
   QB2 = models.ForeignKey( Player, related_name='qb2', null=True )
   RB1 = models.ForeignKey( Player, related_name='rb1', null=True )
   RB2 = models.ForeignKey( Player, related_name='rb2', null=True )
   WR1 = models.ForeignKey( Player, related_name='wr1', null=True )
   WR2 = models.ForeignKey( Player, related_name='wr2', null=True )
   PK = models.ForeignKey( Player, related_name='pk', null=True )
   TD = models.ForeignKey( Team, related_name='td', null=True )
   score = models.IntegerField( default=0 )

   def __str__( self ):
      return '%s%d' % ( self.user.username, self.week )

   # To fix django admin page plural problem
   class Meta:
      verbose_name_plural = 'picks'

