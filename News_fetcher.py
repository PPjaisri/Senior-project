import os
import logging
from msvcrt import getch

PATH = os.getcwd()
# PATH = os.path.dirname(PATH)
# PATH = os.path.join(PATH, 'Scrapy\Scrapy_project')
PATH = os.path.join(PATH, 'News_fetcher')

logging.basicConfig(
    format='%(asctime)s - %(message)s',
    level=logging.INFO
    )

SCRAPE_LIST = [
    'AFNT/anti_thread',
    'AFNT/anti_info',
    'Sure/sure_thread',
    'Sure/sure_info'
]


def run_file():
    for i in SCRAPE_LIST:
        logging.info(f'\nCrawling {i}.py\n')
        file_path = os.path.join(PATH, i)
        os.system(f'py -3.7 "{file_path}.py"')

    return None


if __name__ == '__main__':
    run_file()
    print('Crawl finished press any button to close')
    getch()
