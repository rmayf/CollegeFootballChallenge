# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CfbscraperItem( scrapy.Item ):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class TeamItem( scrapy.Item ):
   teamId = scrapy.Field()
   name = scrapy.Field()

class PlayerItem( scrapy.Item ):
   playerId = scrapy.Field()
   teamId = scrapy.Field()
   name = scrapy.Field()
   position = scrapy.Field()
