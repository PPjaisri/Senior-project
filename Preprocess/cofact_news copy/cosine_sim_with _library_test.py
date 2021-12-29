#%%
import pythainlp
import numpy as np
import math
import nltk
import re
import pandas as pd 
import seaborn as sns
import random 
import json
import os

from pythainlp import word_tokenize
from pythainlp import corpus
from pythainlp.corpus import thai_stopwords
from pythainlp.corpus import wordnet
from nltk.stem.porter import PorterStemmer
from nltk.corpus import words
from stop_words import get_stop_words
from string import punctuation
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,mean_squared_error, r2_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn import preprocessing
from sklearn import svm

nltk.download('words')
th_stop = thai_stopwords()
p_stemmer = PorterStemmer()

def split_word(text):
    tokens = word_tokenize(text,engine='icu')
    
    # Remove stop words ภาษาไทย และอักขระพิเศษ
    tokens = [i for i in tokens if not i in th_stop and not i in punctuation and not i in ['“','”','‘','’']] 
    
    # Thai transform to root word
    # tokens_temp=[]
    # for i in tokens:
    #     w_syn = wordnet.synsets(i)
    #     if (len(w_syn)>0) and (len(w_syn[0].lemma_names('tha'))>0):
    #         tokens_temp.append(w_syn[0].lemma_names('tha')[0])
    #     else:
    #         tokens_temp.append(i)
    
    # tokens = tokens_temp
    
    # ลบตัวเลข
    tokens = [i for i in tokens if not i.isnumeric()]
    
    # ลบช่องว่าง
    tokens = [i for i in tokens if not ' ' in i]

    return tokens

# def find_cosine_similarity(original_text_vector, headline_news_vector, first_text_index, second_text_index):
#     sum = 0 #upper text of cosine similarity
#     sum_a = 0
#     sum_b = 0
#     total_words_number = original_text_and_headline_news_vector.shape[1]

#     for index in range(total_words_number):
#         if (original_text_vector[first_text_index, index] == 0) and (headline_news_vector[second_text_index, index] ==0):
#             continue
#         sum_a += original_text_vector[first_text_index, index]**2
#         sum_b += headline_news_vector[second_text_index, index]**2

#         sum += original_text_vector[first_text_index, index]*headline_news_vector[second_text_index, index]

#     # print('This is sum (upperpart) :',sum)
    
#     squareroot_sum_a = math.sqrt(sum_a)
#     squareroot_sum_b = math.sqrt(sum_b)
#     lowerpart = squareroot_sum_a * squareroot_sum_b

#     # print('This is lowerpart :',lowerpart)
#     return (sum/lowerpart)

def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)

def read_cofact_detail():
    # Opening JSON file
    root_path = os.getcwd()
    print("This is root_path :",root_path)
    path = root_path + '\Scrapy\Scrapy_project\spiders\\fetch file\cofact_detail.json'
    f = open(path, encoding="utf8")
    
    # returns JSON object as
    # a dictionary
    cofact_original_text_data = json.load(f)

    # Closing file
    f.close()
    return cofact_original_text_data

def get_cofact_original_text_info(original_text_data): #สำหรับดึงข้อความดั้งเดิม (header) และลิ้งของข้อความดั้งเดิม (reference) จากเว็บไซต์ cofact
    original_text_list = []

    for original_text in range(len(original_text_data)):
        tmp = []
        tmp.append(str(original_text_data[original_text]['header']) + str(original_text_data[original_text]['content']))
        tmp.append(original_text_data[original_text]['link'])
        original_text_list.append(tmp)

    return original_text_list

def read_cofact_refer():
    # Opening JSON file
    root_path = os.getcwd()
    path = root_path + '\Scrapy\Scrapy_project\spiders\\fetch file\cofact_refer.json'
    f = open(path, encoding="utf8")
    
    # returns JSON object as
    # a dictionary
    cofact_refer_text_data = json.load(f)

    # Closing file
    f.close()
    return cofact_refer_text_data

def get_cofact_refer_info(cofact_refer_text_data): #สำหรับดึงข้อความดั้งเดิม (header) และลิ้งของข้อความดั้งเดิม (reference) จากเว็บไซต์ cofact
    refer_text_list = []

    for refer_text in range(len(cofact_refer_text_data)):
        tmp = []
        tmp.append(cofact_refer_text_data[refer_text]['header'])
        tmp.append(cofact_refer_text_data[refer_text]['reference'])
        refer_text_list.append(tmp)

    return refer_text_list

def match_cofact_news(cofact_refer_text_list, cofact_original_text_list):
    original_text_and_headline_news = []

    for refer_text in range(len(cofact_refer_text_list)):
        tmp = []
        for original_text in range(len(cofact_original_text_list)):
            if cofact_refer_text_list[refer_text][1] == cofact_original_text_list[original_text][1] and (cofact_original_text_list[original_text][0] != "NoneNone"):
                tmp.append(cofact_original_text_list[original_text][0])
                tmp.append(cofact_refer_text_list[refer_text][0])
                original_text_and_headline_news.append(tmp)
                break

    return original_text_and_headline_news

cofact_original_text_data = read_cofact_detail()
cofact_original_text_list = get_cofact_original_text_info(cofact_original_text_data)
cofact_refer_text_data = read_cofact_refer()
cofact_refer_text_list = get_cofact_refer_info(cofact_refer_text_data)

matched_cofact_news = match_cofact_news(cofact_refer_text_list, cofact_original_text_list)
original_text_and_headline_news = []
for news in matched_cofact_news:
    original_text_and_headline_news.append(news[0])
    original_text_and_headline_news.append(news[1])

original_and_headline_tokens_list = [split_word(txt) for txt in original_text_and_headline_news]
tokens_list_j = [','.join(tkn) for tkn in original_and_headline_tokens_list]
tvec = TfidfVectorizer(analyzer=lambda x:x.split(','),)
original_c_feat = tvec.fit_transform(tokens_list_j)
original_text_and_headline_news_vector = original_c_feat[:,:].todense()
original_text_vector = original_text_and_headline_news_vector[::2]
headline_news_vector = original_text_and_headline_news_vector[1::2]

######################## Calculate Cosine Similarity #######################
# similarity_matrix = []
# def create_similarity_matrix(original_text_vector, headline_news_vector):
#     for text in range(len(original_text_vector)):
#         tmp_array = []
#         for headline in range(len(headline_news_vector)):
#             tmp_array.append(find_cosine_similarity(original_text_vector, headline_news_vector, text, headline))
#         similarity_matrix.append(tmp_array)
    
#     df = pd.DataFrame(similarity_matrix, columns =[i for i in range(len(original_text_vector))], dtype = float)
#     return df

# df_similarity_matrix = create_similarity_matrix(original_text_vector, headline_news_vector)

from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
import matplotlib.pyplot as plt

A =  np.array(np.concatenate((original_text_vector[0], headline_news_vector)))
# print(len(headline_news_vector))
# print(A)
# print(A.shape)
A_sparse = sparse.csr_matrix(A)

similarity_matrix = []
for text in range(len(original_text_vector)):
        tmp_array = []
        for headline in range(len(headline_news_vector)):
            tmp_array.append(cosine_similarity(original_text_vector[text],headline_news_vector[headline]))
        similarity_matrix.append(tmp_array)
        print(text)
df_similarity_matrix = pd.DataFrame(similarity_matrix, columns =[i for i in range(len(original_text_vector))], dtype = float)
cm = sns.light_palette("green", as_cmap=True)
df_similarity_matrix.style.background_gradient(cmap=cm)
plt.show()

# print('pairwise dense output:\n {}\n'.format(similarities))

#also can output sparse matrices
# similarities_sparse = cosine_similarity(A_sparse,dense_output=False)
# print('pairwise sparse output:\n {}\n'.format(similarities_sparse))

def create_cosine_similarity_matrix(original_text_vector, headline_news_vector):

    A =  np.array([np.concatenate((original_text_vector[0], headline_news_vector))])
    # print(original_text_vector[0])
    # print(headline_news_vector[0::])
    print(A)
    # A_sparse = sparse.csr_matrix(A)

    # similarities = cosine_similarity(A_sparse)
    # print('pairwise dense output:\n {}\n'.format(similarities))

    # #also can output sparse matrices
    # similarities_sparse = cosine_similarity(A_sparse,dense_output=False)
    # print('pairwise sparse output:\n {}\n'.format(similarities_sparse))
    return 
# %%
