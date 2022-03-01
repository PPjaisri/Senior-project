import sys
import os
from time import perf_counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT_DIR = os.path.join(SCRIPT_DIR, 'News_fetcher')
sys.path.append(SCRIPT_DIR)

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
    start_time = perf_counter()
    run_file()
    end_time = perf_counter()
    total_time = '{:.2f}'.format(end_time - start_time)
    print(f'Total time {total_time} seconds')
    print('Crawl finished press any button to close')
    getch()
