#!/usr/bin/env python
import django
import os
import subprocess
import sys

sys.path.append("../")
os.environ["DJANGO_SETTINGS_MODULE"] = "cfbc.settings"
django.setup()

from stats.models import Game

os.chdir( "../../cfbScraper" )
scrapyCmd = "scrapy crawl boxscore -a gameId=%s --logfile=scrapy_boxscore_crawl_game_%s.log"
games = Game.objects.all()
for game in games:
	if game.gameId is not None:
		subprocess.call( ( scrapyCmd % ( game.gameId, game.gameId ) ).split() )
		
