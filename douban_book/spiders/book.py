import scrapy
from scrapy.cmdline import execute
from copy import deepcopy
import re
import json
from douban_book.items import DoubanBookItem, DoubanBookReview
import logging

logger = logging.getLogger(__name__)

class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['book.douban.com']
    start_urls = ['https://book.douban.com/tag/?view=type&icn=index-sorttags-all']

    def parse(self, response, **kwargs):
        category_list = response.xpath("//div[@class='article']//tbody//td/a/text()").extract()
        base_url = 'https://book.douban.com/tag/{}?start={}'
        # 遍历所有分类，每个分类下有1000条数据可爬取
        for category in category_list:
            for start in range(0, 1000, 20):
                url = f'https://book.douban.com/tag/{category}?start={start}'
                yield scrapy.Request(url=url, callback=self.parse_tag_page)

    def parse_tag_page(self, response):
        book_urls = response.xpath('//*[@id="subject_list"]/ul/li/div[2]/h2/a/@href').extract()
        for url in book_urls:
            yield scrapy.Request(url=url, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        item = DoubanBookItem()
        item['url'] = response.url
        schema = response.xpath("//script[@type='application/ld+json']/text()").extract_first()
        if schema is not None:
            d = eval(schema)
            item['title'] = d['name']
            item['author'] = d['author'][0].get('name')
            item['isbn'] = d['isbn']

        info = response.xpath("//div[@id='info']").extract_first()
        info_map = {
            '副标题': 'subtitle',
            '出版年': 'publishing_year',
            '出版社': 'publishing_house',
            '页数': 'page_number',
            '定价': 'price',
        }
        for name, item_name in info_map.items():
            temp = re.search(rf'{name}:</span>(.*?)<br>', info)
            if temp is not None:
                item[item_name] = temp.group(1).strip()

        rating = response.xpath("//strong[@class='ll rating_num ']/text()").extract_first()
        if rating is not None:
            item['rating'] = rating.strip()
        item['vote_number'] = response.xpath("//span[@property='v:votes']/text()").extract_first()
        item['image'] = response.xpath("//*[@id='mainpic']/a/img/@src").extract_first()

        content_list = response.xpath("//div[@id='link-report']//div[@class='intro']/p/text()").extract()
        item['content_intro'] = ' '.join(content_list)
        item['author_intro'] = response.xpath(
            "//span[text()='作者简介']/../following-sibling::div[1]//div[@class='intro']/p/text()").extract_first()
        if response.url is not None:
            book_id = re.search(r'(\d+)/$', response.url).group(1)
            directory_list = response.xpath(f"//div[@id='dir_{book_id}_full']/text()").extract()
            item['directory'] = ';'.join(directory_list)

        recommend_books = response.xpath("//*[@id='db-rec-section']/div/dl/dd/a/text()").extract()
        if len(recommend_books) != 0:
            recommend_books = [book.strip() for book in recommend_books]
        recommend_urls = response.xpath("//*[@id='db-rec-section']/div/dl/dd/a/@href").extract()
        item['douban_recommends'] = list(zip(recommend_books, recommend_urls))
        tags = response.xpath("//div[@id='db-tags-section']//a[@class='  tag']/text()").extract()
        item["tags"] = ' '.join(tags)
        # 短评和评论
        item['comments'] = response.xpath("//*[@id='new_score']/ul/li//span[@class='short']/text()").extract()
        # logger.warning(item)
        yield item

        m = {
            'url': response.url,
            'title': item['title'],
        }
        cid_list = response.xpath('//div[@class="review-list  "]/div/@data-cid').extract()
        for cid in cid_list:
            url = f'https://book.douban.com/j/review/{cid}/full'
            yield scrapy.Request(url=url, callback=self.parse_review_page,
                                 meta={'data': deepcopy(m)})

    def parse_review_page(self, response):
        review_item = DoubanBookReview()
        data = response.meta["data"]
        review_item['url'] = data['url']
        review_item['title'] = data['title']
        review = re.sub(r'<.*?>', ' ', json.loads(response.text)['html'])
        review_item['review'] = re.sub(r"--&gt;|\u3000|\n|\t|&nbsp;|&amp;|&quot;", " ", review).strip()
        yield review_item


if __name__ == '__main__':
    # cmd: scrapy crawl book
    execute(['scrapy', 'crawl', 'book'])
