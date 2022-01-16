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
    'anti_thread',
    'anti_info',
    # 'cofact_thread',
    # 'cofact_info',
    # 'cofact_refer'
]


def run_file():
    for i in SCRAPE_LIST:
        logging.info(f'Crawling {i}.py')
        file_path = os.path.join(PATH, 'AFNT')
        os.system(f'py -3.7 "{file_path}\{i}.py"')
        # print(f'py -3.7 {file_path}')

    return None


if __name__ == '__main__':
    run_file()
    getch()
