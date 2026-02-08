import streamlit as st
import google.generativeai as genai

st.title("テスト要約くん")

# APIキー設定
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

url = st.text_input("YouTube URLを入力")

if st.button("実行"):
    # 修正版のモデル指定
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    # 動画URLを直接解析する指示
    response = model.generate_content(f"この動画の内容を日本語で要約して: {url}")
    st.write(response.text)
