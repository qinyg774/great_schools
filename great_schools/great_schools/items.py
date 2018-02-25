# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GreatSchoolsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    gs_rating_overall = scrapy.Field()
    review_count = scrapy.Field()
    school_type = scrapy.Field()
    grades_served = scrapy.Field()
    gs_rating_academics = scrapy.Field()
    test_scores = scrapy.Field()
    info = scrapy.Field()