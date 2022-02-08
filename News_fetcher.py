import os
import logging
from msvcrt import getch

PATH = os.getcwd()
PATH = os.path.dirname(PATH)
# PATH = os.path.join(PATH, 'Scrapy\Scrapy_project')

logging.basicConfig(
    format='%(asctime)s - %(message)s',
    level=logging.INFO
    )

SCRAPE_LIST = [
    'anti_thread',
    'anti_info',
    'sure_thread',
    'sure_info',
    'cofact_thread',
    'cofact_info',
    'cofact_refer'
]

#! before compile to .exe need to compile at ~/exe first !!

def run_file():
    global PATH
    PATH = os.path.dirname(PATH)

    for i in SCRAPE_LIST:
        file_path = os.path.join(PATH, 'News_fetcher')
        file_path = os.path.join(file_path, i)
        logging.info(f'\n\nCrawling {i}.py\n')
        os.system(f'py -3.7 "{file_path}.py"')
        print(file_path)

    return None


if __name__ == '__main__':
    run_file()
    print('Crawl finished press any button to close')
    getch()
