!pip install sklearn

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModel
import torch
import sqlite3

# データベースからキーワードを取得
def get_data():
    keyword_dict = {}
    keyword_list = []
    # データベースに接続
    conn = sqlite3.connect('ChatIPuT.db')
    # カーソルを取得
    cur = conn.cursor()
    
    # データベースからキーワードを取得
    cur.execute('SELECT * FROM Keyword')
    for i,row in enumerate(cur):
        keyword_dict[i+1] = row[1]
        keyword_list.append(row[1])
    
    # データベースを閉じる
    cur.close()
    conn.close()
    return keyword_dict,keyword_list

# 質問をベクトル化する関数
def vectorize(text,tokenizer,model):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).detach().numpy()

# キーワードをベクトル化
def keyword_vectorize(keyword_list,tokenizer,model):
    keyword_vectors = {}
    for i,keyword in enumerate(keyword_list):
        inputs = tokenizer(keyword, return_tensors='pt', padding=True, truncation=True)
        outputs = model(**inputs)
        keyword_vectors[keyword] = outputs.last_hidden_state.mean(dim=1).detach().numpy()
    return keyword_vectors

def get_response(user_input,tokenizer,model):
    # ユーザーの入力をベクトル化
    user_input_vector = vectorize(user_input,tokenizer,model)
    # キーワードを取得
    keyword_dict,keyword_list = get_data()
    # キーワードをベクトル化
    keyword_vector = keyword_vectorize(keyword_list,tokenizer,model)
    
    # コサイン類似度を計算
    similarities = {q:cosine_similarity(user_input_vector, v) for q, v in keyword_vector.items()}
    
    # キーワードの辞書と類似度の辞書を返す
    return keyword_dict,similarities

# 最も高い類似度を出力
def high_sim(similarities):
    high_sim = 0
    for key, value in similarities.items():
        if value > high_sim:
            high_sim = value
    return high_sim
