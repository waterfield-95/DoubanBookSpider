# -*- coding: utf-8 -*-
"""
@Time   : 2021/1/20 5:52 PM
@author : Yuan Tian
"""

import douban_book.database as db
from douban_book.items import BookComment
from scrapy import Request, Spider
from douban_book.util import get_douban_id
from lxml import etree

cursor = db.connection.cursor()


class BookCommentSpider(Spider):
    name = 'book_comment'
    allowed_domains = ['book.douban.com']
    sql = 'SELECT url FROM books'
    cursor.execute(sql)
    book_urls = cursor.fetchall()
    start_urls = dict()
    for url in book_urls:
        douban_id = get_douban_id(url[0])
        start_urls[douban_id] = f'https://book.douban.com/subject/{douban_id}/comments'

    def start_requests(self):
        for (key, url) in self.start_urls.items():
            # 可添加headers,cookies
            yield Request(url)

    def parse(self, response, **kwargs):
        # 403, 评论到220条后，请求不到数据
        if 403 == response.status:
            print("book.comment.response.403.url", response.url)
        elif 302 == response.status or 301 == response.status:
            print("book.comment.response.302.url", response.url)
        else:
            douban_id = get_douban_id(response.url)

            # 下一页
            next_regx = "//a[@data-page='next']/@href"
            next_url_param_list = response.xpath(next_regx).extract()

            # 获取当页所有评论item
            item_regx = "//li[@class='comment-item']"
            comment_list = response.xpath(item_regx).extract()

            if len(comment_list) > 1:
                for item in comment_list:
                    html = etree.HTML(item)

                    # 用户信息
                    user_url_list = html.xpath("//div[@class='avatar']/a/@href")
                    user_name_list = html.xpath("//div[@class='avatar']/a/@title")
                    user_avatar_list = html.xpath("//div[@class='avatar']/a/img/@src")
                    # 评论信息
                    comment_id_list = html.xpath("//li/@data-cid")
                    vote_list = html.xpath("//span[@class='vote-count']/text()")
                    rating_list = html.xpath("//span[contains(@class,'allstar')]/@class")
                    comment_time_list = html.xpath("//span[@class='comment-time']/text()")
                    comment_list = html.xpath("//span[@class='short']/text()")

                    # 写入Item，yield传入pipeline，存入数据库
                    comment = BookComment()
                    comment['douban_id'] = douban_id
                    comment['douban_comment_id'] = comment_id_list[0] if len(comment_id_list) > 0 else ""
                    comment['douban_user_nickname'] = user_name_list[0] if len(user_name_list) > 0 else ""
                    comment['douban_user_avatar'] = user_avatar_list[0] if len(user_avatar_list) > 0 else ""
                    comment['douban_user_url'] = user_url_list[0] if len(user_url_list) > 0 else ""
                    comment['content'] = comment_list[0] if len(comment_list) > 0 else ""
                    comment['votes'] = vote_list[0] if len(vote_list) > 0 else ""
                    comment['rating'] = rating_list[0] if len(rating_list) > 0 else ""
                    comment['comment_time'] = comment_time_list[0] if len(comment_time_list) > 0 else ""
                    print(comment['douban_comment_id'])
                    yield comment

            # 翻页
            if len(next_url_param_list) > 0:
                url = f"https://book.douban.com/subject/{douban_id}/comments/" + next_url_param_list[0]
                yield Request(url, callback=self.parse, dont_filter=True)
