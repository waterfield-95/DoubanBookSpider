import pymysql
from douban_book.items import DoubanBookItem, DoubanBookReview, BookComment
from uuid import uuid1
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from pymysql.err import DataError
import douban_book.database as db


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
        self.db.ping(reconnect=True)
        self.db.close()

    def process_item(self, item, spider):
        book_id = uuid1().hex
        if isinstance(item, DoubanBookItem):
            print('book: ', item.get('title'), item.get('url'))
            data = dict(item)
            douban_recommends = data.pop('douban_recommends')
            comments = data.pop('comments')
            # 存入books表中主键id
            data['id'] = book_id
            self._store_dict_to_table(data, 'books')
            # 存入comments表中
            for comment in comments:
                comment_dict = {
                    'id': uuid1().hex,
                    'book_id': book_id,
                    'comment': comment.strip(),
                    'url': item['url'],
                    'title': item['title'],
                    'type': 'short',
                }
                try:
                    self._store_dict_to_table(comment_dict, 'comments')
                except:
                    continue
            # 存入douban_recommend表
            for book, url in douban_recommends:
                recommend_dict = {
                    'id': uuid1().hex,
                    'book_id': book_id,
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
                'book_id': book_id,
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
        url = data['url']
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql =f'insert into {table} ({keys}) values ({values})'
        # 防止断开
        self.db.ping(reconnect=True)
        try:
            self.cursor.execute(sql, tuple(data.values()))
        except DataError as e:
            error = str(e)
            if 'directory' in error:
                del data['directory']
            elif 'content_intro' in error:
                del data['content_intro']
            self._store_dict_to_table(data, table)
        else:
            self.db.commit()


class ImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        url = request.url
        file_name = url.split('/')[-1]
        return file_name

    def item_completed(self, results, item, info):
        if isinstance(item, DoubanBookItem):
            image_paths = [x['path'] for ok, x in results if ok]
            # if not image_paths:
            #     raise DropItem('Image Downloaded Failed')
            return item

    def get_media_requests(self, item, info):
        if isinstance(item, DoubanBookItem) and item.get('image') is not None:
            yield Request(item['image'])


class DoubanPipeline:
    def __init__(self):
        self.cursor = db.connection.cursor()

    def db_reconnect(self):
        db.connection.ping(reconnect=True)
        self.cursor = db.connection.cursor()

    def close_spider(self, spider):
        self.cursor.close()

    def get_book_id(self, item):
        sql = f'SELECT id FROM books WHERE url="https://book.douban.com/subject/{item["douban_id"]}/"'
        self.cursor.execute(sql)
        return self.cursor.fetchone()[0]

    def get_comment(self, item):
        sql = f'SELECT * FROM  comments WHERE douban_comment_id={item["douban_comment_id"]}'
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def save_comment(self, item):
        keys = item.keys()
        values = tuple(item.values())
        fields = ','.join(keys)
        temp = ','.join(['%s'] * len(keys))
        sql = 'INSERT INTO comments (%s) VALUES (%s)' % (fields, temp)
        self.cursor.execute(sql, values)
        return db.connection.commit()

    def update_comment(self, item):
        douban_comment_id = item.pop('douban_comment_id')
        keys = item.keys()
        values = tuple(item.values())
        fields = [f'{i}=%s' for i in keys]
        sql = 'UPDATE comments SET %s WHERE douban_comment_id=%s' % (','.join(fields), douban_comment_id)
        self.cursor.execute(sql, tuple(i.strip() for i in values))
        return db.connection.commit()

    def process_item(self, item, spider):
        if isinstance(item, BookComment):
            """
            book_comment
            """
            self.db_reconnect()
            exist = self.get_comment(item)
            if not exist:
                try:
                    item['id'] = uuid1().hex
                    item['book_id'] = self.get_book_id(item)
                    self.save_comment(item)
                except Exception as e:
                    print(item)
                    print(e)
            # else:
            #     self.update_comment(item)
