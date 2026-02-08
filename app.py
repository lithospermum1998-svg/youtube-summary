import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# 見た目の設定
st.set_page_config(page_title="自分専用・要約くん", layout="centered")
st.title("📺 YouTube要約アプリ")

# 1. APIキーの設定（後でStreamlitの設定画面で入力します）
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.warning("APIキーが設定されていません。")

# 2. 入力エリア
url = st.text_input("動画のURLをペーストしてください:")

# 3. 実行ボタン
if st.button("要約を開始"):
    if url:
        try:
            # 動画IDを抽出
            video_id = url.split("v=")[1].split("&")[0] if "v=" in url else url.split("/")[-1]
            
            with st.spinner("文字起こしを取得中..."):
                # 日本語と英語の字幕を探す
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ja', 'en'])
                full_text = " ".join([i['text'] for i in transcript])
            
            with st.spinner("AIが内容を要約中..."):
                model = genai.GenerativeModel("gemini-1.5-flash")
                # あなた専用のプロンプト
                prompt = f"以下の動画の文字起こしを元に、内容を3つのポイントで日本語で要約してください:\n\n{full_text}"
                response = model.generate_content(prompt)
                
                st.subheader("📝 要約結果")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"エラーが発生しました。字幕がない動画かもしれません。")
    else:
        st.info("URLを入力してください。")
