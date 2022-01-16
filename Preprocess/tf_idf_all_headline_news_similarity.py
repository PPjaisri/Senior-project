import numpy as np
import nltk
import re
import pandas as pd 
import json
import os
import pickle
import csv

from pythainlp import word_tokenize
from pythainlp.corpus import thai_stopwords
from nltk.stem.porter import PorterStemmer
from stop_words import get_stop_words
from string import punctuation

from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import TfidfVectorizer
from ast import literal_eval

from Preprocess.similarity_check import train_similarity_check_model

nltk.download('words')
th_stop = thai_stopwords()
en_stop = get_stop_words('en')
p_stemmer = PorterStemmer()

query_vector = []

def split_word(text):
    tokens = word_tokenize(text,engine='newmm')
    
    # Remove stop words ภาษาไทย และอักขระพิเศษ
    tokens = [i for i in tokens if (not i in th_stop) & (not i in en_stop) & (not i in punctuation) & (not i in ["'",'"','“','”','‘','’','\n',"None", ' '])] 
    
    # ลบตัวเลข
    tokens = [i for i in tokens if not i.isnumeric()]
    
    # ลบช่องว่าง
    tokens = [i for i in tokens if not ' ' in i]

    return tokens

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

def read_cofact_refer(): #สำหรับดึงข้อมูลของ cofact csv
    # Opening CSV file
    root_path = os.getcwd()
    path = os.path.join(root_path, 'Scrapy\\Scrapy_project\\spiders\\results\\cofact\\cofact_refer.csv')
    
    f = open(path, encoding="utf8")
    
    # returns CSV object as
    # a dictionary
    csvreader = csv.reader(f)

    # read header from CSV file
    header = []
    header = next(csvreader)
    
    rows = []
    for row in csvreader:
        tmp = []
        
        content_parts = []
        content = ''
        
        # เพิ่ม header
        tmp.append(row[1]) 

        # เพิ่ม content
        content_parts = literal_eval(row[2])
        content = ''.join(filter(None, content_parts))
        
        tmp.append(content)
        
        # เพิ่ม link (ข่าวต้นทางสุด)
        tmp.append(row[3])
        
        rows.append(tmp)

    # Closing file
    f.close()
    
    return rows

def read_anti_refer(): #สำหรับดึงข้อมูลของ anti fake news csv
    # Opening CSV file
    root_path = os.getcwd()
    path = os.path.join(root_path, 'Scrapy\\Scrapy_project\\spiders\\results\\anti\\anti_info.csv')
    f = open(path, encoding="utf8")
    
    # returns CSV object as
    # a dictionary
    csvreader = csv.reader(f)
    
    # read header from CSV file
    header = []
    header = next(csvreader)

    rows = []
    for row in csvreader:
        tmp = []
        
        content_parts = []
        content = ''
        
        # เพิ่ม header
        tmp.append(row[1])
        
        # เพิ่ม content
        content_parts = literal_eval(row[2])
        content = ''.join(filter(None, content_parts))
        tmp.append(content)
        
        # เพิ่ม link
        tmp.append(row[3])
        rows.append(tmp)

    # Closing file
    f.close()
    
    return rows

def read_sure_refer(): #สำหรับอ่านข้อมูลของ sure ก่อน share ***JSON***
    # Opening JSON file
    root_path = os.getcwd()
    path = os.path.join(root_path, 'Scrapy/Scrapy_project/spiders//fetch file/sure_info.json')
    f = open(path, encoding="utf8")
    
    # returns JSON object as
    # a dictionary
    sure_refer_text_data = json.load(f)

    # Closing file
    f.close()
    return sure_refer_text_data

def get_sure_refer_info(sure_refer_text_data): #สำหรับดึงหัวข้อข่าวอ้างอิง (header) และลิงของข่าวอ้างอิง (link)
    refer_text_list = []

    for refer_text in range(len(sure_refer_text_data)):
        tmp = []
        tmp.append(sure_refer_text_data[refer_text]['header'])
        tmp.append(''.join(filter(None, sure_refer_text_data[refer_text]['content'])))
        tmp.append(sure_refer_text_data[refer_text]['link'])
        refer_text_list.append(tmp)

    return refer_text_list

def combine_every_headline():
    refer_text_list = []
    cofact_refer_text_list = read_cofact_refer()

    anti_refer_text_list = read_anti_refer()

    sure_refer_text_data = read_sure_refer()
    sure_refer_text_list = get_sure_refer_info(sure_refer_text_data)

    refer_text_list = cofact_refer_text_list + anti_refer_text_list + sure_refer_text_list
    
    return refer_text_list

def create_df_for_backtrack(all_refer_text_list):
    global all_original_text_and_headline_news_df, all_refer_header, all_refer_content
    
    all_refer_content = []
    all_refer_url = []
    for i in range(len(all_refer_text_list)):
        all_refer_header.append(all_refer_text_list[i][0]) #list ของส่วนหัวข้อข่าว
        all_refer_content.append(all_refer_text_list[i][1]) #list ของส่วนเนื้อหาเท่านั้น
        all_refer_url.append(all_refer_text_list[i][2]) #list ของ url เท่านั้น
        
    #ทำ list ให้เป็น dataframe
    all_original_text_and_headline_news_df = pd.DataFrame(list(zip(all_refer_header, all_refer_content, all_refer_url)), columns=["All_headline_from_every_reference", "All_content_from_every_reference", "All_URL_from_every_reference"])
    
    start_train_similarity_check_model()    
        
    return all_original_text_and_headline_news_df, all_refer_header

def tokenize_and_create_vocabulary(all_refer_header):
    all_headline_tokens_list = [split_word(txt) for txt in all_refer_header] #นำ list ของเนื้อหามาตัดคำ
    local_all_tokens_list_j = [','.join(tkn) for tkn in all_headline_tokens_list]
    
    ## Create Vocabulary
    tokens_list = []

    for words in local_all_tokens_list_j:
        # print(words)
        temp_list = words.split(",")
        # print(temp_list)
        for i in temp_list:
            tokens_list.append(i)

    local_vocabulary = set(tokens_list)
    local_vocabulary = list(local_vocabulary)
    
    ### Save Vacabulary
    root_path = os.getcwd()
    path = os.path.join(root_path, 'vocabulary_all.txt')
    with open(path, "w", encoding="utf-8") as file:
        file.write(str(local_vocabulary))

    ### load Vacabulary
    root_path = os.getcwd()
    path = os.path.join(root_path, 'vocabulary_all.txt')
    with open(path, "r", encoding="utf-8") as file:
        data2 = eval(file.readline())
    
    return local_vocabulary, local_all_tokens_list_j, data2

def create_tfidf_matrix(all_tokens_list_j):
    tvec = TfidfVectorizer(analyzer=lambda x:x.split(','),)
    local_original_c_feat = tvec.fit_transform(all_tokens_list_j)
    
    ### Save model
    root_path = os.getcwd()
    path = os.path.join(root_path, 'all-tfid.pkl')
    with open(path,'wb') as handle:
        pickle.dump(local_original_c_feat, handle)
    
    return local_original_c_feat, tvec

## Create vector for Query/search keywords
def gen_vector_T(tokens):
    global tvec
    
    Q = np.zeros((len(vocabulary)))
    
    x = tvec.transform(tokens)
    
    x = x.A[0]
    return x

def cosine_similarity_T(k, query):
    global tvec
    tokens = split_word(str(query))
    q_df = pd.DataFrame(columns=['q_clean'])
    q_df.loc[0,'q_clean'] =str(tokens)

    q_df=q_df.replace(to_replace ="\[.", value = '', regex = True)
    q_df=q_df.replace(to_replace ="'", value = '', regex = True)
    q_df=q_df.replace(to_replace =" ", value = '', regex = True)
    q_df=q_df.replace(to_replace ='\]', value = '', regex = True)
    
    d_cosines = []
    
    query_vector = gen_vector_T(q_df['q_clean'])
    query_vector = query_vector.reshape((1,-1))

    d_cosines = np.dot(normalize(query_vector), norm_original_c_feat)
    
    list_d_cosines = d_cosines[0].tolist()
    
    out = np.array(list_d_cosines).argsort()[-k:][::-1]

    list_d_cosines.sort()
    a = pd.DataFrame()
    for i in out:
        a.loc[i,'index'] = str(i)
        a.loc[i,'headline'] = all_original_text_and_headline_news_df['All_headline_from_every_reference'][i]
        
    list_d_cosines.sort(reverse=True)
    
    for j in range(k):
        a.loc[out[j],'Score'] = list_d_cosines[j]
        
    all_result = a
    all_result_with_url = pd.DataFrame()
    for i in range(len(all_result)):
        if float(all_result.iloc[i]["Score"]) != 0.0:
            all_result_with_url.loc[i,'index'] = all_result.iloc[i]["index"]
            all_result_with_url.loc[i,'headline'] = all_result.iloc[i]["headline"]
            all_result_with_url.loc[i,'url'] = all_original_text_and_headline_news_df["All_URL_from_every_reference"][int(all_result.iloc[i]["index"])]
            all_result_with_url.loc[i,'content'] = all_original_text_and_headline_news_df["All_content_from_every_reference"][int(all_result.iloc[i]["index"])]

    #append user input เข้าไปใน all_result_with_url ด้วย
    query_df = {'index': '-1', 'headline': query, 'url': '', 'content': ''}
    all_result_with_url = all_result_with_url.append(query_df, ignore_index = True)
    
    js = all_result_with_url.to_dict('records')
        
    return js
    

def preprocess():
    global original_c_feat, norm_original_c_feat, tvec, all_refer_text_list, vocabulary, all_original_text_and_headline_news_df, data2
    all_refer_text_list = combine_every_headline() #เก็บหัวข้อข่าวและ URL ใน list
    all_original_text_and_headline_news_df, all_refer_header = create_df_for_backtrack(all_refer_text_list) #สร้าง dataframe สำหรับอ้างถึงตอนค้นคืนข่าว
    vocabulary, all_tokens_list_j, data2 = tokenize_and_create_vocabulary(all_refer_header) #ตัดคำจากหัวข่าว (headline) และสร้าง list ของคำศัพท์ (vocabulary)
    original_c_feat, tvec = create_tfidf_matrix(all_tokens_list_j) #สร้าง vector tfidf สำหรับแต่ละข่าว

    #Pre-calculated original_c_feat (TFIDF matrix) for cosine similarity
    norm_original_c_feat = normalize(original_c_feat)
    norm_original_c_feat = norm_original_c_feat.toarray()
    norm_original_c_feat = norm_original_c_feat.T
    
    return None

def start_train_similarity_check_model():
    global all_original_text_and_headline_news_df
    #นำ dataframe ที่ได้ ไป train กับ model similarity check
    train_similarity_check_model(all_original_text_and_headline_news_df)

# Main
all_refer_text_list = []
all_refer_header = []

vocabulary = []
all_tokens_list_j = []
data2 = []
all_original_text_and_headline_news_df = pd.DataFrame()

original_c_feat = ""
norm_original_c_feat = ""
tvec = ""

preprocess()