from scrapy.cmdline import execute
import os


if __name__ == '__main__':
    if not os.path.exists('log'):
        os.mkdir('log/')
    if not os.path.exists('images'):
        os.mkdir('images/')
    execute(['scrapy', 'crawl', 'book'])