import re
import douban_book.database as db
import time

cursor = db.connection.cursor()


def get_numbers(url):
    result = re.search(r'\d+', url)
    return result.group() if result is not None else ''


def clean_text(text):
    # 正则删除html标签，保留文本
    res = re.sub(r'<.*?>', '', text).strip()
    return res


def store_dict_to_mysql(items, table):
    keys = items.keys()
    values = tuple(items.values())
    fields = ','.join(keys)
    temp = ','.join(['%s'] * len(keys))
    sql = f'INSERT INTO {table} ({fields}) VALUES ({temp})'
    cursor.execute(sql, values)
    db.connection.commit()


def get_col_from_table(table, table_col, value):
    sql = f'SELECT * FROM {table} WHERE {table_col}="{value}"'
    cursor.execute(sql)
    return cursor.fetchone()


def handle_exception(response):
    if response.status in [301, 302, 403]:
        print(f"{response.status}.book.review.response.url: {response.url}\n", flush=True)
        items = {
            'url': response.url,
            'status': response.status,
            'flag': '0'
        }
        db.connection.ping(reconnect=True)
        collie_table = 'review_exception'
        # if not get_col_from_table(table=collie_table, col='url', value=items['url']):
        #     store_dict_to_mysql(items, table=collie_table)
        if response.status == 403:
            time.sleep(5)
        return 1
    else:
        return 0
