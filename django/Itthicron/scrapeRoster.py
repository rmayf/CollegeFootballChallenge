#!/usr/bin/env python

# This script clears the stats_* tables in the database and runs the roster spider

import os
import subprocess

os.chdir( "../" )
sqlClearStatsInput = open( 'sql_clear_stats.txt' )
sqlClearStatsCmd = "sqlite3 db.sqlite3"
subprocess.call( sqlClearStatsCmd.split(), stdin=sqlClearStatsInput )
os.chdir( "../cfbScraper" )
scrapyCmd = "scrapy crawl roster --logfile=scrapy_roster_crawl.log"
subprocess.call( scrapyCmd.split() )

