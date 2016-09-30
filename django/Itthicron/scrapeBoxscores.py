#!/usr/bin/env python
import Itthicron
import subprocess
import os
from stats.models import Game
from sys import stderr

os.chdir( "../" )
sqlClearStatsInput = open( 'sql_clear_boxscore_stats.txt' )
sqlClearStatsCmd = "sqlite3 db.sqlite3"
subprocess.call( sqlClearStatsCmd.split(), stdin=sqlClearStatsInput )
os.chdir( "../cfbScraper" )
scrapyCmd = "scrapy crawl boxscore -a gameId=%s --logfile=scrapy_boxscore_crawl_game_%s.log"
games = Game.objects.all()
columns = "{0:^20}|{1:^20}|{2:^20}|{3:^20}"
seperator = "{:-^80}"
stderr.write( columns.format( "WEEK", "TEAM", "OPP", "ESPN_ID" ) + "\n" )
stderr.write( seperator.format( "" ) + "\n" )
for game in games:
	if game.gameId is not None:
                stderr.write( columns.format( game.week, game.team.name.encode( 'utf8' ),
                                              game.opponent.name.encode( 'utf8' ), game.gameId ) + "\n" )
		subprocess.call( ( scrapyCmd % ( game.gameId, game.gameId ) ).split() )
