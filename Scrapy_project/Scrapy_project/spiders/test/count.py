import json

temp = []

with open('C:/Coding/Senior project/Scrapy_project/sure.json', encoding='utf-8') as f:
    data = json.load(f)

    for obj in data:
        temp.append(list(obj.values()))

with open('link.json', 'a', encoding='utf-8') as f:
    for i in temp:
        f.write(i[1] + '\n')

# print(temp[0][1])

# f = open('C:/Coding/Senior project/Scrapy_project/sure_link.txt', 'r')
# f.read()

# for i in f:
#     print(i)
