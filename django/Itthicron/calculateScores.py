#!/usr/bin/env python
import Itthicron
from leaderboard.models import Picks
from stats.models import PlayerStat, DefenseStat
from django.core.exceptions import ObjectDoesNotExist
from stats.models import *

# Calculate scores for players and defenses
for player in PlayerStat.objects.all():
   score = 0
   #passing
   score += 4 * player.passingTD + 0.04 * player.passingYards - 2 * player.thrownInterceptions

   #rushing
   score += 6 * player.rushingTD + 0.1 * player.rushingYards

   #receiving
   score += 6 * player.receivingTD + 0.1 * player.receivingYards

   #kicking
   score += 1 * player.extraPoints + 3 * player.fieldGoals

   player.score = score
   player.save()

for d in DefenseStat.objects.all():
   score = 0
   #interceptions
   score += 2 * d.interceptions + 6 * d.interceptionsTD

   #kickReturnTD
   score += 6 * d.kickoffTD

   #puntReturnTD
   score += 6 * d.puntTD
   
   #pointsAgainst
   if d.pointsAgainst == 0:
      score += 10
   elif d.pointsAgainst < 7:
      score += 8
   elif d.pointsAgainst < 14:
      score += 6
   elif d.pointsAgainst < 21:
      score += 4
   elif d.pointsAgainst < 28:
      score += 2
   elif d.pointsAgainst < 35:
      score += 1
   elif d.pointsAgainst < 42:
      score += 0
   elif d.pointsAgainst < 49:
      score += -2
   else:
      score += -4

   d.score = score
   d.save()


# Sum score for users
for week in xrange( 0, Itthicron.currentWeek() + 1 ):
   for pick in Picks.objects.filter( week=week ):
           score = 0
           try:
                   score += PlayerStat.objects.get( player=pick.QB1, week=week ).score
           except ObjectDoesNotExist: 
                   pass
           try:
                   score += PlayerStat.objects.get( player=pick.QB2, week=week ).score
           except ObjectDoesNotExist: 
                   pass
           try:
                   score += PlayerStat.objects.get( player=pick.RB1, week=week ).score
           except ObjectDoesNotExist: 
                   pass
           try:
                   score += PlayerStat.objects.get( player=pick.RB2, week=week ).score
           except ObjectDoesNotExist: 
                   pass
           try:
                   score += PlayerStat.objects.get( player=pick.WR1, week=week ).score
           except ObjectDoesNotExist: 
                   pass
           try:
                   score += PlayerStat.objects.get( player=pick.WR2, week=week ).score
           except ObjectDoesNotExist: 
                   pass
           try:
                   score += PlayerStat.objects.get( player=pick.PK, week=week ).score
           except ObjectDoesNotExist: 
                   pass
           try:
                   score += DefenseStat.objects.get( team=pick.TD, week=week ).score
           except ObjectDoesNotExist:
                   pass

           pick.score = score
           pick.save()
