import pandas as pd
import umap
import umap.plot
import hdbscan
import numpy as np
import os

from sentence_transformers import SentenceTransformer, InputExample
from sentence_transformers import models, losses
from torch.utils.data import DataLoader

def train_similarity_check_model(all_original_text_and_headline_news_df):
    global all_headline, mapper
    
    for index in range(len(all_original_text_and_headline_news_df)):
        all_headline.append(all_original_text_and_headline_news_df["All_headline_from_every_reference"][index])
        
    for i in range(len(all_headline)):
        if type(all_headline[i]) != type("string"):
            all_headline[i] = str(all_headline[i])
    
    # หากต้องการ train model ใหม่ให้ uncomment code ส่วนล่าง
    # model_name = 'mrp/simcse-model-roberta-base-thai'

    # word_embedding_model = models.Transformer(model_name, max_seq_length=256)
    # pooling_model = models.Pooling(
    #     word_embedding_model.get_word_embedding_dimension(),
    #     pooling_mode_mean_tokens=True
    # )
    # train_model = SentenceTransformer(modules=[word_embedding_model, pooling_model])
    
    # # Convert train sentences to positive pairs
    # train_data = [InputExample(texts=[text, text]) for text in all_headline]

    # # DataLoader to batch your data
    # train_dataloader = DataLoader(train_data, batch_size=20, shuffle=True)

    # # Use the MultipleNegativesRankingLoss
    # train_loss = losses.MultipleNegativesRankingLoss(train_model)
    
    # # Call the fit method
    # train_model.fit(
    #     train_objectives=[(train_dataloader, train_loss)],
    #     epochs=2,
    #     show_progress_bar=True
    # )
    
    # # Save trained model
    # train_model.save('Preprocess/output/simcse-model')
    
    initialize_mapper()
    
    return None

def result_similarity_check(all_result_with_url):
    global model, mapper
    result_headline = []
    
    final_result_index = []
    final_result_with_url = pd.DataFrame()
    
    for index in range(len(all_result_with_url)):
        result_headline.append(all_result_with_url[index]["headline"])
    
    if len(result_headline) <= 10:
        result = final_result_with_url.to_dict('records')
        
        return result
    
    result_headline_encodings = model.encode(result_headline)
    
    umap_embs = mapper.transform(result_headline_encodings)
    
    clusterer = hdbscan.HDBSCAN(min_samples=2, min_cluster_size=10, prediction_data=True).fit(umap_embs)
    soft_clusters = hdbscan.all_points_membership_vectors(clusterer)
    cluster_labels = [np.argmax(x) for x in soft_clusters]
    
    for i in range(len(cluster_labels) - 1):
        if cluster_labels[i] == cluster_labels[-1]:
            final_result_index.append(i)
    
    for i in range(len(final_result_index)):
        final_result_with_url.loc[i,'index'] = all_result_with_url[final_result_index[i]]["index"]
        final_result_with_url.loc[i,'headline'] = all_result_with_url[final_result_index[i]]["headline"]
        final_result_with_url.loc[i,'url'] = all_result_with_url[final_result_index[i]]['url']
        final_result_with_url.loc[i,'content'] = all_result_with_url[final_result_index[i]]['content']
    
    result = final_result_with_url.to_dict('records')
        
    return result
    
    

def initialize_mapper():
    global model, mapper, all_headline
    
    # Opening CSV file
    root_path = os.getcwd()
    path = os.path.join(root_path, 'Preprocess\\output\\simcse-model')
    
    # load the trained SimCSE model
    model = SentenceTransformer(path)
    
    # encode all headline
    cse_review_encodings = model.encode(all_headline)
    mapper = umap.UMAP().fit(cse_review_encodings)
    
#Main
all_headline = []
