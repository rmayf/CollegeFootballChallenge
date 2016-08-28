#!/usr/bin/env python
import Itthicron
from stats.models import Season

week = Itthicron.currentWeek()
week += 1
print "Updating current week to %d...." % week

Itthicron.currentWeekIs( week )
print "Success!"
