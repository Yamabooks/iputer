#!/usr/bin/env python
# coding: utf-8

pip install -r requirements.txt

import streamlit as st
import random
#import time
from PIL import Image
from similarities import get_response, high_sim
from Chatbot2 import get_category, get_question, get_keyword, get_answer, show_keywords
from transformers import AutoTokenizer, AutoModel

#🦖👤🤖 🎓

#ページbar
image = Image.open('data/image_IPuTer.png')
st.set_page_config(
    page_title="Chat_IPuTer",
    page_icon=image,
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
         'Get Help': 'https://www.google.com',
         'Report a bug': "https://www.google.com",
         'About': """
         # 対話式質問回答チャットボット
         このアプリは対話形式で、ユーザーの質問に回答するチャットボットを利用することが出来ます。
         """
     })


# 挨拶
def do_greet():    
    title = "Chat-IPuTer"
    st.markdown(f'<h1 style="text-align: center; color: aqua; font-size: 100px;">{title}</h1>', unsafe_allow_html=True)
    
    text = "はじめまして！<br>大阪国際工科専門職大学のことなら、<br>私になんでもに質問してください！"    
    st.markdown(f'<h2 style="text-align: center;">{text}</h2>', unsafe_allow_html=True)
    return


#userの回答を表示・保存
def do_user(prompt):
    #質問を表示
    st.chat_message("user", avatar="👤").markdown(prompt)
    st.session_state.qa.append({"role": "user", "content": prompt, "avatar": "👤"})
    return


#assistantの回答を表示・保存
def do_assistant(text):
    st.chat_message("assistant", avatar="🎓").markdown(text)
    st.session_state.qa.append({"role": "assistant", "content": text, "avatar": "🎓"})
    return
    
    
#Keywordの選択肢を取得
def do_keyword():
    tokenizer = AutoTokenizer.from_pretrained("cl-tohoku/bert-base-japanese-whole-word-masking")
    model = AutoModel.from_pretrained("cl-tohoku/bert-base-japanese-whole-word-masking")
    
    # パディング用のトークンを設定
    tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    
    # ユーザーの質問
    user_input = st.session_state.question.strip()

    # 類似度を計算
    keyword_dict,similarities = get_response(user_input,tokenizer,model)
    
    #類似度を画面に表示
    #st.text(high_sim(similarities))
    
    if high_sim(similarities) < 0.8:
        # 類似度の高いキーワードを出力
        key_dict = show_keywords(keyword_dict,similarities)
        st.session_state.key_dict = key_dict
        #keyをリスト化
        key_list = list(key_dict.keys())
        
        #for i, (key, value) in enumerate(key_dict.items(), start=1):
        #    st.write(f"{i}:{key}")
        
        #max_value = len(key_dict)
        
        with st.form("select_keyword"):
            st.radio("どれについて知りたい？", key_list, key="keyword")
            #statusを変更
            st.session_state.status = 1
            #ボタンで入力を確定
            submit_btn = st.form_submit_button("決定")


    else:
        # 最も類似度の高いキーワードを取得
        max_key = max(similarities, key=similarities.get)
        key_id = [key for key, value in keyword_dict.items() if value == max_key][0]
        st.session_state.key_id = key_id
        
        st.session_state.answer_id = st.session_state.answer_id + key_id*100
        
        do_category()
    return 


#質問からcategoryの選択肢を取得
def do_category():
    key_id = st.session_state.key_id
    #Categoryを取得
    selects = get_category(key_id)
    #cat_dictの初期化
    st.session_state.cat_dict = {}
    #辞書の作成
    for i, select in enumerate(selects, start=1):
        st.session_state.cat_dict[i] = select
        st.write(f"{i}: {select}")
    
    #Categoryの数を取得
    max_value= len(selects)
    #数字を入力
    with st.form("select category"):
        st.number_input("どれについて知りたい？", min_value=1, max_value=max_value, step=1, value=1, key="cat_id")
        #statusを変更
        st.session_state.status = 2
        #ボタンで入力を確定
        submit_btn = st.form_submit_button("決定")
    return 
 

#Questionの選択肢を取得
def do_question():
    key_id = st.session_state.key_id
    cat_id = st.session_state.cat_id
        
    #Questionを取得
    selects = get_question(key_id, cat_id) #ここでデータベースからquestionのリストを取得
    
    #que_dictの初期化
    st.session_state.que_dict = {}
    #辞書の作成
    for i, select in enumerate(selects, start=1):
        st.session_state.que_dict[i] = select
        st.write(f"{i}: {select}")

    #Questionの数を取得
    max_value= len(selects)
    #数字を入力
    with st.form("select question"):
        st.number_input("どれについて知りたい？", min_value=1, max_value=max_value, step=1, value=1, key="que_id")
        #statusを変更
        st.session_state.status = 3
        #ボタンで入力を確定
        submit_btn = st.form_submit_button("決定")
    return 


#すべて初期化
def do_reset():
    st.session_state.key_id = 0
    st.session_state.cat_id = 0
    st.session_state.que_id = 0
    st.session_state.answer_id = 0
    return

#プログレスバー設定（未実装）
def do_progress():
    progress_bar = st.progress(0)  # プログレスバーの初期値を0%に設定

    for i in range(100):
        # 何らかの処理を実行する
        time.sleep(0.1)

        # プログレスバーの進捗を更新する
        progress_bar.progress(i + 1)

        
#main
def main():
    
    #セッションステートの"status"を初期化
    if "status" not in st.session_state:
        st.session_state.status = 0
    #セッションステートの"key_id"を初期化
    if "key_id" not in st.session_state:
        st.session_state.key_id = 0
    #セッションステートの"cat_id"を初期化
    if "cat_id" not in st.session_state:
        st.session_state.cat_id = 0
    #セッションステートの"que_id"を初期化
    if "que_id" not in st.session_state:
        st.session_state.que_id = 0
    #セッションステートの"answer_id"を初期化
    if "answer_id" not in st.session_state:
        st.session_state.answer_id = 0
    #セッションステートの"key_dict"リストを初期化
    if "key_dict" not in st.session_state:
        st.session_state.key_dict = []
    #セッションステートの"cat_dict"リストを初期化
    if "cat_dict" not in st.session_state:
        st.session_state.cat_dict = []
    #セッションステートの"que_dict"リストを初期化
    if "que_dict" not in st.session_state:
        st.session_state.que_dict = []
    #セッションステートの"qa"リストを初期化
    if "qa" not in st.session_state:
        st.session_state.qa = []
    
    #挨拶を呼び出す
    do_greet()
    
    #履歴を表示
    for message in st.session_state.qa:
        st.chat_message(message["role"], avatar=message.get("avatar", None)).markdown(message["content"])
    
    
    #keywordの結果をから、do_categoryの実行
    if st.session_state.status == 1:
        #辞書検索によってキーワードからkey_idを取得
        keyword = st.session_state.keyword
        key_id = st.session_state.key_dict[keyword]
        #key_idを登録
        st.session_state.key_id = key_id
        #answer_idを設定
        st.session_state.answer_id = st.session_state.answer_id + key_id*100
        do_category()
        
    
    #do_categoryの結果を表示&保存、do_quesitonの実行
    elif st.session_state.status == 2:
        cat_id = st.session_state.cat_id
        st.session_state.answer_id = st.session_state.answer_id + cat_id*10
        select = st.session_state.cat_dict[cat_id]
        
        do_user(select)
        
        if st.session_state.key_id == 2 or st.session_state.key_id == 3:
            st.session_state.que_id = 0
            que_id = st.session_state.que_id
            st.session_state.answer_id = st.session_state.answer_id + que_id
            #answer_idを設定、初期化
            answer_id = st.session_state.answer_id
            #Answerを表示
            answer = get_answer(answer_id)

            do_assistant(answer)

            do_reset()

            st.session_state.status = 0
        else:
            #Question_id取得
            do_question()
          
    #do_questionの結果を表示&保存、answerの表示
    elif st.session_state.status == 3:
        #que_idを設定
        que_id = st.session_state.que_id
        
        st.session_state.answer_id = st.session_state.answer_id + que_id
        #Questionを表示・保存
        select = st.session_state.que_dict[que_id]
        
        do_user(select)
        
        #answer_idを設定、初期化
        answer_id = st.session_state.answer_id
        #Answerを表示
        answer = get_answer(answer_id)
        
        do_assistant(answer)
        
        do_reset()
        
        st.session_state.status = 0
        
    
    #質問の入力
    if prompt := st.chat_input("Send a message...", key="question"):
            #質問を表示
            do_user(prompt)
            
            do_keyword()

    
if __name__ == "__main__":
    main()
