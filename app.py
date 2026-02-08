import streamlit as st
import google.generativeai as genai

st.title("🔍 接続テスト")

# APIキー設定
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    st.write("✅ APIキーは設定されています")
    
    try:
        st.write("📋 使えるモデルの一覧を取得中...")
        # 使えるモデルを全部リストアップして表示する
        models = genai.list_models()
        found_models = []
        for m in models:
            if 'generateContent' in m.supported_generation_methods:
                found_models.append(m.name)
        
        st.success("接続成功！以下のモデルが使えます：")
        st.json(found_models)
        
        # 試しに一番標準的なモデルで挨拶してみる
        st.write("---")
        st.write("🤖 テスト会話を実行中...")
        model = genai.GenerativeModel('gemini-1.5-flash') 
        response = model.generate_content("こんにちは！聞こえてますか？")
        st.write(f"AIからの返事: {response.text}")
        
    except Exception as e:
        st.error(f"エラー発生: {e}")
else:
    st.error("SecretsにAPIキーがありません")
