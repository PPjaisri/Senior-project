import os
from msvcrt import getch

PATH = os.getcwd()
PATH = os.path.dirname(PATH)
PATH = os.path.join(PATH, 'Scrapy\Scrapy_project')

SCRAPE_LIST = [
    'anti_thread',
    'anti_info',
    'cofact_thread',
    'cofact_info',
    'cofact_refer'
]


def run_file():
    os.chdir(PATH)
    for i in SCRAPE_LIST:
        os.system(f'scrapy crawl {i}')

    return None


if __name__ == '__main__':
    run_file()
    getch()
