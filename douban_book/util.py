import re


def get_douban_id(url):
    book_id = re.search(r'\d+', url)
    # book_id = url.split('/')[-2]
    return book_id.group()
