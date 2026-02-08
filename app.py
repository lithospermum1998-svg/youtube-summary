import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# 画面設定
st.set_page_config(page_title="YouTube要約くん", page_icon="🎬")
st.title("🎬 YouTube要約（最新版）")

# APIキー設定
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("SecretsでAPIキーを設定してください")

url = st.text_input("YouTubeのURLを貼り付けてください:")

if st.button("要約を開始"):
    if url:
        with st.status("解析中...", expanded=True) as status:
            try:
                # 1. 字幕を探す
                video_id = url.split("v=")[1].split("&")[0] if "v=" in url else url.split("/")[-1]
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ja', 'en'])
                text_data = " ".join([i['text'] for i in transcript])
                prompt = f"以下の内容を日本語で要約して:\n\n{text_data}"
            except:
                # 2. 字幕がない場合は動画URLを直接投げる
                prompt = f"この動画の内容を日本語で要約して: {url}"

            try:
                # 【重要】models/ を付けないのが最新の正解です
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                
                status.update(label="完了！", state="complete", expanded=False)
                st.markdown("### 📝 要約結果")
                st.write(response.text)
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
    else:
        st.warning("URLを入力してください")
