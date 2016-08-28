#!/usr/bin/env python
# This depends on PYTHONPATH and DJANGO_SETTINGS_MODULE environment variables
import django
django.setup()

# Import CFBC models
from stats.models import Season

def currentWeek():
   return int( Season.objects.get().currentWeek )

def currentWeekIs( week ):
   season = Season.objects.get()
   season.currentWeek = week
   season.save()
