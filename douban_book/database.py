import pymysql
from douban_book.settings import MYSQL_HOST, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD


connection = pymysql.connect(
    host=MYSQL_HOST,
    db=MYSQL_DATABASE,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    charset='utf8mb4'   # 兼容4字节，避免错误，例如emoji
)