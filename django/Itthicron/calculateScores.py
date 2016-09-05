#!/usr/bin/env python
import Itthicron
from leaderboard.models import Picks
from django.core.exceptions import ObjectDoesNotExist
from stats.models import *

for week in xrange( 0, Itthicron.currentWeek() + 1 ):
   for pick in Picks.objects.filter( week=week ):
           score = 0
           try:
                   score += PlayerStat.objects.get( player=pick.QB1, week=currentWeek ).score
           except ObjectDoesNotExist: 
                   pass
           try:
                   score += PlayerStat.objects.get( player=pick.QB2, week=currentWeek ).score
           except ObjectDoesNotExist: 
                   pass
           try:
                   score += PlayerStat.objects.get( player=pick.RB1, week=currentWeek ).score
           except ObjectDoesNotExist: 
                   pass
           try:
                   score += PlayerStat.objects.get( player=pick.RB2, week=currentWeek ).score
           except ObjectDoesNotExist: 
                   pass
           try:
                   score += PlayerStat.objects.get( player=pick.WR1, week=currentWeek ).score
           except ObjectDoesNotExist: 
                   pass
           try:
                   score += PlayerStat.objects.get( player=pick.WR2, week=currentWeek ).score
           except ObjectDoesNotExist: 
                   pass
           try:
                   score += PlayerStat.objects.get( player=pick.PK, week=currentWeek ).score
           except ObjectDoesNotExist: 
                   pass
           try:
                   score += DefenseStat.objects.get( team=pick.TD, week=currentWeek ).score
           except ObjectDoesNotExist:
                   pass

           pick.score = score
           pick.save()
