from scrapy.cmdline import execute
import os


if __name__ == '__main__':
    if not os.path.exists('log'):
        os.mkdir('log/')
    execute(['scrapy', 'crawl', 'book_comment'])