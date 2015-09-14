# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem
from stats.models import Game, Player, Team

class GameItem( DjangoItem ):
   django_model = Game

class PlayerItem( DjangoItem ):
   django_model = Player

class TeamItem( DjangoItem ):
   django_model = Team

