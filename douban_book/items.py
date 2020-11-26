# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanBookItem(scrapy.Item):
    table = 'books'
    url = scrapy.Field()
    title = scrapy.Field()
    subtitle = scrapy.Field()
    author = scrapy.Field()
    publishing_year = scrapy.Field()
    publishing_house = scrapy.Field()
    page_number = scrapy.Field()
    price = scrapy.Field()
    isbn = scrapy.Field()
    rating = scrapy.Field()
    vote_number = scrapy.Field()
    image = scrapy.Field()
    content_intro = scrapy.Field(comment='内容简介')
    author_intro = scrapy.Field()
    directory = scrapy.Field()
    tags = scrapy.Field()

    # 需要进行数据处理存入不同表
    douban_recommends = scrapy.Field()  # tuple
    comments = scrapy.Field(comment='短评')   # list


class DoubanBookReview(scrapy.Item):
    table = 'comments'
    title = scrapy.Field()
    url = scrapy.Field()
    review = scrapy.Field()


