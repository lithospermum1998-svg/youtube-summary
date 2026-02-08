import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# 画面の設定
st.set_page_config(page_title="最強YouTube要約", page_icon="🎬")
st.title("🎬 YouTube要約（字幕なし対応版）")

# 1. APIキーの設定（Secretsから読み込み）
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Secretsで APIキー (GEMINI_API_KEY) を設定してください")

# 2. 入力エリア
url = st.text_input("YouTube動画のURLを貼り付けてください:")

# 3. 実行ボタン
if st.button("要約を開始"):
    if url:
        with st.status("AIが動画を解析中...", expanded=True) as status:
            try:
                # --- ステップA: 字幕の取得を試みる ---
                st.write("字幕データを探しています...")
                # URLから動画IDを抽出
                video_id = url.split("v=")[1].split("&")[0] if "v=" in url else url.split("/")[-1]
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ja', 'en'])
                text_data = " ".join([i['text'] for i in transcript])
                
                # 字幕がある場合の指示
                prompt = f"以下の文字起こしデータを読み取り、内容を日本語で分かりやすく要約して:\n\n{text_data}"
                st.write("字幕が見つかりました。内容をまとめています...")
                
            except Exception:
                # --- ステップB: 字幕がない場合（動画を直接解析） ---
                st.write("字幕が見つかりませんでした。動画を直接読み取ります...")
                # URLを直接渡して、映像と音声から判断させる指示
                prompt = f"この動画の内容を、映像と音声の両方から判断して日本語で詳しく要約して。URL: {url}"

            try:
                # --- ステップC: AIモデルの呼び出し ---
                # 先ほどのテストで最も安定していた「2.0-flash-lite」を使用します
                model = genai.GenerativeModel("models/gemini-2.0-flash-lite")
                response = model.generate_content(prompt)
                
                # 結果表示
                status.update(label="解析完了！", state="complete", expanded=False)
                st.markdown("### 📝 要約結果")
                st.write(response.text)
                
            except Exception as e:
                # 万が一AI呼び出し自体でエラーが出た場合
                st.error(f"AI解析中にエラーが発生しました。時間を置いて試してください。\nエラー内容: {e}")
    else:
        st.warning("URLを入力してください")

# 使い方アドバイス
st.info("※字幕がない動画や長い動画の場合、解析に1分ほどかかることがあります。そのままお待ちください。")
