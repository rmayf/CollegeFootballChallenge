from django.db import models
from django.contrib.auth.models import User

class Message( models.Model ):
   text = models.CharField( max_length=500 )
   date = models.DateTimeField( 'date published' )
