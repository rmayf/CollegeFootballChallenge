#!/usr/bin/env python
from stats.models import Season

season = Season.objects.all()[ 0 ]
season.currentWeek += 1
season.save()
