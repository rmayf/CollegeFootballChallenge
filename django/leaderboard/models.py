from django.db import models
from django.contrib.auth.models import User

class User_( models.Model ):
   user = models.OneToOneField( User )
   displayName = models.CharField( max_length=150 )
