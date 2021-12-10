import os

# path = r'C:\\Users\\PPjaisri\\Coding\\Senior project'
path = os.getcwd()
path = os.path.dirname(path)
path = os.path.join(path, 'Scrapy\Scrapy_project')

# os.chdir(path)

# scrape_list = [
#     'anti_thread',
#     'anti_info',
#     'cofact_thread',
#     'cofact_info',
#     'cofact_refer'
#     ]

# for i in scrape_list:
#     os.system(f'scrapy crawl {i}')
