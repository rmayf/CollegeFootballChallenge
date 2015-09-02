from rest_framework import mixins, generics, viewsets
from django.contrib.auth.models import User
from leaderboard.serializers import *
from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.authtoken import views as rest_views
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required, user_passes_test

# Generic class 
class CreateListRetrieveUpdateViewSet( mixins.CreateModelMixin,
                                       mixins.ListModelMixin,
                                       mixins.RetrieveModelMixin,
                                       mixins.UpdateModelMixin,
                                       viewsets.GenericViewSet ):
   pass       

class UserViewSet( CreateListRetrieveUpdateViewSet ):
   queryset = User.objects.all()

   def get_serializer_class( self ):
      if self.action == 'create':
         return CreateUserSerializer 
      elif self.action == 'update':
         return UpdateUserSerializer
      else:
         return PublicUserSerializer

   def create( self, request, *args, **kwargs ):
      username = request.POST.get( 'username', None ) 
      email = request.POST.get( 'email', None ) 
      password = request.POST.get( 'password', None ) 
      try:
         User.objects.get( username=username )
         # User already exists, throws and error
         body = { "err_message" : '%s is already taken... sorry :(' % username }
         return Response( body,
                          status=status.HTTP_400_BAD_REQUEST )
      except ObjectDoesNotExist:
         user = User.objects.create_user( username, email, password )
         return rest_views.obtain_auth_token( request )

   def update( self, request, *args, **kwargs ):
      user = request.user
      if not user.is_authenticated():
         body = { 'err', 'you shall not pass' }
         return Response( body, status=status.HTTP_403_FORBIDDEN )

      #import pdb
      #pdb.set_trace()

      id = int( request.path.split( '/' )[ -2 ] )
      if request.user.id == id:
         return CreateListRetrieveUpdateViewSet.update( self, request, *args, **kwargs )
      else:
         body = { 'err' : 'yo, you fukked up',
                  'id' : request.user.id,
                  'id_in_resp' : id }
         return Response( body, status=status.HTTP_403_FORBIDDEN )

      
class UserConfigViewSet( viewsets.ModelViewSet ):
   queryset = User.objects.all()
   serializer_class = PrivateUserSerializer
   permission_classes = ( IsAdminUser, )

#class PicksViewSet( viewsets.ReadOnlyModelViewSet ):
#   season = Season.objects.get( pk=1 )
#   queryset = Picks.objects.filter( week.index__lt=season.currentWeek )
#   serializer_class = PicksSerializer
