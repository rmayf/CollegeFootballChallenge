from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import User_

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class User_Inline( admin.StackedInline ):
   model = User_
   can_delete = False
   verbose_name_plural = 'users'

# Define a new User admin
class UserAdmin( UserAdmin ):
    inlines = ( User_Inline, )

# Re-register UserAdmin
admin.site.unregister( User )
admin.site.register( User, UserAdmin )
