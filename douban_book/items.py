# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


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


class BookComment(Item):
    id = Field()
    book_id = Field()
    douban_id = Field()
    douban_comment_id = Field()
    douban_user_nickname = Field()
    douban_user_avatar = Field()
    douban_user_url = Field()
    content = Field()
    votes = Field()
    rating = Field()
    comment_time = Field()
