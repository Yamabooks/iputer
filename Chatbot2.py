!pip install -r requirements.txt

import numpy as np
from numpy import argmin
import sqlite3

#データベースから指定されたKeywordを取得
def get_keyword(key_id):
    keywords = []
    # データベースに接続
    conn = sqlite3.connect('ChatIPuT.db')
    # カーソルを取得
    cur = conn.cursor()
    
    # データベースからQuestionを取得
    cur.execute('SELECT * FROM keyword WHERE key_id = ?', (key_id,))
    for row in cur:
        keywords.append(row[1])
    
    # データベースを閉じる
    cur.close()
    conn.close()
    return keywords

# データベースから指定されたCategoryを取得
def get_category(key_id):
    categories = []
    # データベースに接続
    conn = sqlite3.connect('ChatIPuT.db')
    # カーソルを取得
    cur = conn.cursor()
    
    # データベースからQuestionを取得
    cur.execute('SELECT * FROM category WHERE key_id = ?', (key_id,))
    for row in cur:
        categories.append(row[2])
    
    # データベースを閉じる
    cur.close()
    conn.close()
    return categories

# データベースから指定されたQuestionを取得
def get_question(key_id, cat_id):
    questions = []
    # データベースに接続
    conn = sqlite3.connect('ChatIPuT.db')
    # カーソルを取得
    cur = conn.cursor()
    
    # データベースからQuestionを取得
    cur.execute('SELECT * FROM question WHERE key_id = ? AND cat_id = ?', (key_id, cat_id,))
    for row in cur:
        questions.append(row[3])
    
    # データベースを閉じる
    cur.close()
    conn.close()
    return questions

# データベースから指定されたAnswerを取得
def get_answer(answer_id):
    
    # データベースに接続
    conn = sqlite3.connect('ChatIPuT.db')
    # カーソルを取得
    cur = conn.cursor()
    
    # データベースからAnswerを取得
    cur.execute('SELECT * FROM answer WHERE answer_id = ?', (answer_id,))
    answer = cur.fetchone()[1]
    
    # データベースを閉じる
    cur.close()
    conn.close()
    return answer


# Answerを出力
def show_answer(key_id, cat_id, que_id):
    # Answerを取得
    answer_id = key_id*100 + cat_id*10 + que_id
    answer = get_answer(answer_id)
    
    # Answerを出力
    #print(answer)
    #st.text(answer)
    
    return answer


# Questionリストを出力
def show_questions(key_id):
    # Questionを取得
    questions = get_question(key_id)
    
    # Questionを出力
    #for i in range(len(questions)):
        #質問を表示
        #print(str(i+1) + " : " + questions[i])
        #st.text(str(i+1) + " : " + questions[i])
    
    return questions


# チャットボットの起動
def start_bot():
    # 起動時のメッセージ
    print("ChatIPuTへようこそ！")
    print("あなたの質問にお答えします！")
    
    # ユーザーの質問を受け付ける
    user_input = input("質問を入力してください：")
    
    return user_input

# 類似度の高い3つのキーワードを出力
def show_keywords(keyword_dict,similarities):
    
    key_dict = {}
    
    for i in range(3):
        # 最も類似度の高いキーワードを取得
        max_key = max(similarities, key=similarities.get)
        key_id = [key for key, value in keyword_dict.items() if value == max_key][0]
        
        # 最も類似度の高いキーワードを出力
        #print(key_id, " : " + max_key)
        
        #辞書に保存
        key_dict[max_key] = key_id 
        
        # 類似度の高いキーワードを辞書から削除
        del similarities[max_key]
        
    #return key_id, max_key
    return key_dict

# 終了判定
def is_finish():
    # 終了するかどうかの入力を受け付ける
    print("他に質問はありますか？")
    
    while True:
        input_finish = input("はい or いいえ：")
        
        if input_finish == "はい":
            return 0
        elif input_finish == "いいえ":
            return 1
        else:
            print("はい または いいえ で答えてください")
