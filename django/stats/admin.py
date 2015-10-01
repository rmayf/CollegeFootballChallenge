from django.contrib import admin


from .models import *

admin.site.register( Team )
admin.site.register( Game )
admin.site.register( Week )
admin.site.register( Season )
admin.site.register( Player )
admin.site.register( PlayerStat)
admin.site.register( DefenseStat)
