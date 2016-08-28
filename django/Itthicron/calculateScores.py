#!/usr/bin/env python
import Itthicron
from leaderboard.models import Picks
from stats.models import *

currentWeek = Itthicron.currentWeek()
picks = Picks.objects.filter( week=currentWeek )
for pick in picks:
	
	score = 0
	
	try:
		score += PlayerStat.objects.filter( player=pick.QB1, week=currentWeek )[ 0 ].score
	except Player.DoesNotExist:
		pass
	
	try:
 		score += PlayerStat.objects.filter( player=pick.QB2, week=currentWeek )[ 0 ].score
	except Player.DoesNotExist:
		pass
	
	try:
 		score += PlayerStat.objects.filter( player=pick.RB1, week=currentWeek )[ 0 ].score
	except Player.DoesNotExist:
		pass
	
	try:
 		score += PlayerStat.objects.filter( player=pick.RB2, week=currentWeek )[ 0 ].score
	except Player.DoesNotExist:
		pass
	
	try:
 		score += PlayerStat.objects.filter( player=pick.WR1, week=currentWeek )[ 0 ].score
	except Player.DoesNotExist:
		pass
	
	try:
 		score += PlayerStat.objects.filter( player=pick.WR2, week=currentWeek )[ 0 ].score
	except Player.DoesNotExist:
		pass
	
	try:
 		score += PlayerStat.objects.filter( player=pick.PK, week=currentWeek )[ 0 ].score
	except Player.DoesNotExist:
		pass

	try:
		score += DefenseStat.objects.filter( team=pick.TD, week=currentWeek )[ 0 ].score
	except Team.DoesNotExist:
		pass

	pick.score = score
	pick.save()
