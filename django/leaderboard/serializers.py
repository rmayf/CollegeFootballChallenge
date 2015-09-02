from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Picks

class PublicUserSerializer( serializers.ModelSerializer ):
   class Meta:
      model = User
      fields = ( 'id', 'username', 'first_name',
                 'last_name' )

class PrivateUserSerializer( serializers.ModelSerializer ):
   class Meta:
      model = User
      
class CreateUserSerializer( serializers.ModelSerializer ):
   class Meta:
      model = User
      fields = ( 'username', 'email', 'password' )

class UpdateUserSerializer( serializers.ModelSerializer ):
   class Meta:
      model = User
      fields = ( 'username', 'first_name', 'last_name', 'password',
                 'email', 'id' )

class PicksSerializer( serializers.ModelSerializer ):
   class Meta:
      model = Picks
