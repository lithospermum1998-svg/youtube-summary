import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

st.set_page_config(page_title="最強YouTube要約", page_icon="🎬")
st.title("YouTube要約")

# APIキー設定
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("SecretsでAPIキーを設定してください")

url = st.text_input("動画URLを貼り付け:")

if st.button("要約を実行"):
    if url:
        with st.status("解析中...", expanded=True) as status:
            try:
                # 1. まずは高速な「字幕取得」を試みる
                st.write("字幕を探しています...")
                video_id = url.split("v=")[1].split("&")[0] if "v=" in url else url.split("/")[-1]
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ja', 'en'])
                text_data = " ".join([i['text'] for i in transcript])
                prompt = f"以下の文字起こしを日本語で要約して:\n\n{text_data}"
                st.write("字幕が見つかりました。要約中...")
                
            except:
                # 2. 字幕がなければ、動画URLを直接AIに投げる（マルチモーダル）
                st.write("字幕がありません。動画を直接解析します（少し時間がかかります）...")
                prompt = f"この動画の内容を、映像と音声から判断して日本語で要約して: {url}"

            model = genai.GenerativeModel("models/gemini-1.5-flash")
            response = model.generate_content(prompt)
            
            status.update(label="完了！", state="complete", expanded=False)
            st.markdown("### 📝 要約結果")
            st.write(response.text)
    else:
        st.error("URLを入力してください")
