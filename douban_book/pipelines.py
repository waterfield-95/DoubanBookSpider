# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from douban_book.items import DoubanBookItem, DoubanBookReview
from uuid import uuid1


class MysqlPipeline:
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8',
                                  port=self.port)
        self.cursor = self.db.cursor()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
        )

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        if isinstance(item, DoubanBookItem):
            print('book: ', item['title'])
            data = dict(item)
            douban_recommends = data.pop('douban_recommends')
            comments = data.pop('comments')
            # 存入books表中
            data['id'] = uuid1().hex
            self._store_dict_to_table(data, 'books')
            # 存入comments表中
            for comment in comments:
                comment_dict = {
                    'id': uuid1().hex,
                    'comment': comment.strip(),
                    'url': item['url'],
                    'title': item['title'],
                    'type': 'short',
                }
                self._store_dict_to_table(comment_dict, 'comments')
            # 存入douban_recommend表
            for book, url in douban_recommends:
                recommend_dict = {
                    'id': uuid1().hex,
                    'url': item['url'],
                    'title': item['title'],
                    'recommend_book': book,
                    'recommend_url': url,
                }
                self._store_dict_to_table(recommend_dict, 'douban_recommend')

        if isinstance(item, DoubanBookReview):
            print('comments: ', item['title'])
            data = {
                'id': uuid1().hex,
                'url': item['url'],
                'title': item['title'],
                'type': 'long',
                'comment': item['review'],
            }
            self._store_dict_to_table(data, 'comments')
        return item

    def _store_dict_to_table(self, data: dict, table):
        """
        存入字典数据进入mysql.db中给定table
        :param data: 字典数据
        :param table: 表名称
        """
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = f'insert into {table} ({keys}) values ({values})'
        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()
