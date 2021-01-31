# -*- coding: utf-8 -*-
"""
@Time   : 2021/1/26 11:01 AM
@author : Yuan Tian
"""

import douban_book.database as db
from douban_book.items import BookReview
from scrapy import Request, Spider
from douban_book.utils import get_numbers, clean_text, handle_exception, get_col_from_table
import time

cursor = db.connection.cursor()


class BookReviewSpider(Spider):
    name = 'book_review'
    allowed_domains = ['book.douban.com']
    sql = 'SELECT url FROM books'
    cursor.execute(sql)
    book_urls = cursor.fetchall()
    start_urls = dict()
    for url in book_urls:
        douban_id = get_numbers(url[0])
        start_urls[douban_id] = f'https://book.douban.com/subject/{douban_id}/reviews?version=1'

    def start_requests(self):
        for (key, url) in self.start_urls.items():
            # 可添加headers,cookies
            yield Request(url)

    def parse(self, response, **kwargs):
        # 1：表示处理异常，0：表示没有异常
        if handle_exception(response) == 1:
            yield Request(response.url, callback=self.parse, dont_filter=True)
        else:
            douban_id = get_numbers(response.url)
            print(f"crawling reviews list: {douban_id}", flush=True)
            cid_list = response.xpath('//div[@class="review-list  "]/div/@data-cid').extract()
            if len(cid_list) > 0:
                for cid in cid_list:
                    url = f'https://book.douban.com/review/{cid}/'
                    if not get_col_from_table(table='reviews', table_col='douban_review_id', value=cid):
                        yield Request(url=url, callback=self.parse_review_page)

                # 下一页
                next_regx = "//span[@class='next']/a/@href"
                next_url_param_list = response.xpath(next_regx).extract()

                if len(next_url_param_list) > 0:
                    url = f"https://book.douban.com/subject/{douban_id}/reviews?version=1&" + next_url_param_list[0][0:]
                    yield Request(url, callback=self.parse, dont_filter=True)

    def parse_review_page(self, response):
        """
        解析评论页 https://book.douban.com/review/9702317/
        """
        if handle_exception(response) == 1:
            pass
        else:
            # 用户信息：头像、昵称、用户主页
            user_avatar_list = response.xpath("//a[@class='avatar author-avatar left']/img/@src").extract()
            user_name_list = response.xpath("//header[@class='main-hd']/a/span/text()").extract()
            user_url_list = response.xpath("//a[@class='avatar author-avatar left']/@href").extract()

            # 评论信息
            book_url_list = response.xpath("//div[@class='subject-title']/a/@href").extract()
            review_title_list = response.xpath("//span[@property='v:summary']/text()").extract()
            rating_list = response.xpath("//span[contains(@class,'allstar')]/@class").extract()
            review_time_list = response.xpath("//span[@class='main-meta']/@content").extract()
            useful_count_list = response.xpath("//button[@class='btn useful_count j a_show_login']/text()").extract()
            useless_count_list = response.xpath("//button[@class='btn useless_count j a_show_login']/text()").extract()
            content_list = response.xpath("//div[@class='review-content clearfix']").extract()

            # 存入items，交给pipeline处理
            review = BookReview()
            review['douban_user_avatar'] = user_avatar_list[0] if len(user_avatar_list) > 0 else ""
            review['douban_user_nickname'] = user_name_list[0] if len(user_name_list) > 0 else ""
            review['douban_user_url'] = user_url_list[0] if len(user_url_list) > 0 else ""

            review['douban_review_id'] = get_numbers(response.url)
            review['douban_id'] = get_numbers(book_url_list[0]) if len(review_title_list) > 0 else ""
            review['rating'] = rating_list[0] if len(rating_list) > 0 else ""
            review['douban_review_title'] = review_title_list[0] if len(review_title_list) > 0 else ""
            review['review_time'] = review_time_list[0] if len(review_time_list) > 0 else ""
            review['useful_count'] = get_numbers(useful_count_list[0]) if len(useful_count_list) > 0 else ""
            review['useless_count'] = get_numbers(useless_count_list[0]) if len(useless_count_list) > 0 else ""
            review['content'] = clean_text(content_list[0]) if len(content_list) > 0 else ""

            if review['douban_id'] == '':
                print(f'Cannot get data: {response.url}\n', flush=True)
                yield Request(response.url, callback=self.parse_review_page, dont_filter=True)
            else:
                print(f"Succeed yield: {review['douban_review_id']}", flush=True)
                yield review
