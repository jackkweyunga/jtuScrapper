# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class TimetableItem(scrapy.Item):
    type_ = scrapy.Field()
    fro = scrapy.Field()
    to = scrapy.Field()
    courses = scrapy.Field()
    rooms = scrapy.Field()
    day = scrapy.Field()


