
import streamlit as st
import google.generativeai as genai
import urllib.parse
import streamlit as st
import urllib.parse  # 

# ページの基本設定（ここを書き換える）
st.set_page_config(
    page_title="INFPメーカー | あなたの言葉をエモく変換",
    page_icon="🦋",
    # ↓ここにRaw URLを直接指定します
    menu_items={
        'About': "https://raw.githubusercontent.com/cotty2020/infp-maker/64fc2c83914eafdb02b6a5ee724a53a341eb60d7/ogp_infp.png"
    }
)

# 1. APIキーの設定
# ローカルでは secrets.toml、ネット公開後は Streamlit Cloud の Secrets を自動で見に行きます
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 2. ページ設定
st.set_page_config(page_title="INFPタイプ変換", page_icon="🦋")

# --- ダークモード用カスタムデザイン ---
st.markdown("""
    <style>
    /* GitHubリンクやメニューを隠す */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
        
            /* ヘッダー・フッター・ツールバーを根こそぎ消す */
    header, footer, .stDeployButton, [data-testid="stToolbar"], [data-testid="stDecoration"] {
        visibility: hidden !important;
        height: 0 !important;
        display: none !important;
    }
           
    
    /* 背景をダークグレーに、文字を白に固定 */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    
    /* 入力欄やボックスのラベルの色を調整 */
    label {
        color: #FFFD !important;
        font-weight: bold;
    }
    
    /* 成功メッセージ(結果)の背景色を少し濃く */
    .stAlert {
        background-color: #1E2E3E;
        color: #FFFFFF;
        border: 1px solid #4B9CD3;
    }
            
            # --- ダークモード用カスタムデザイン（追記・修正版） ---

   :root {
        --st-color-bg-secondary: #FFB300 !important; /* ボタンの背景色の元 */
    }

    /* 2. ボタンを特定して、あらゆる状態の色を固定 */
    div.stButton > button, 
    div.stButton > button:first-child,
    div.stButton > button:disabled,
    div.stButton > button[kind="secondary"] {
        background-color: #00E676;
        color: #000000;
        border: none !important;
        /* ここから下はデザイン */
        border-radius: 25px !important;
        height: 3.5em !important;
        width: 100% !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
        box-shadow: 0 4px 15px rgba(255, 179, 0, 0.4) !important;
    
    }

    /* マウスを乗せたとき（ホバー）の設定 */
    div.stButton > button:hover {
        background-color: #FFD54F; /* さらに明るい黄色に */
        color: #000000;
        transform: translateY(-2px); /* 少し浮き上がる演出 */
        box-shadow: 0 6px 20px rgba(255, 179, 0, 0.5);
    }
    
    /* クリックしたときの設定 */
    div.stButton > button:active {
        transform: translateY(0px);
    }
   
    </style>
    """, unsafe_allow_html=True)

# 3. モデル準備 (キャッシュして高速化)

@st.cache_resource
def get_model():
    return genai.GenerativeModel('gemini-2.0-flash')

model = get_model()


# 4. データ（INFP専用に絞る）
mbti_data = {
    "INFP (仲介者)": {
        "icon": "🍄", 
        "desc": "内省的で感受性豊か。幻想的な比喩を使い、自分の心に潜るような優しい日記風。", 
        "info": "独自の価値観を持ち、繊細な美しさと心の調和を愛するタイプです。"
    }
}

# 5. メイン画面
st.title("🦋 INFP変換メーカー")

st.markdown("""
入力した文章を、INFPになりきってリライトします。
INFPならどう表現するか、心の個性を楽しんでみてください。
""")

# 選択なしでINFPを固定
selected_type = "INFP (仲介者)"

# 特徴を表示
st.info(f"**【{selected_type}の特徴】**\n{mbti_data[selected_type]['info']}")

st.subheader("文章を入力")
user_input = st.text_area("書き換えたい文章を入力してください", "今日はいい天気ですね。")

if st.button("変換する！", use_container_width=True):
    with st.spinner("思考回路を書き換え中..."):
        instruction = mbti_data[selected_type]["desc"]
        prompt = f"以下の文章を、{instruction}\n\n文章：{user_input}"
        
        response = model.generate_content(prompt)
        
        st.markdown("### 🎁 変換結果")
        st.success(response.text)
        
        # SNSボタン
        tweet_text = f"【{selected_type}メーカー】で変換したよ！\n\n{response.text[:40]}..."
        tweet_url = f"https://twitter.com/intent/tweet?text={urllib.parse.quote(tweet_text)}"
        st.markdown(f'<center><a href="{tweet_url}" target="_blank" style="background-color:#1DA1F2;color:white;padding:10px 20px;border-radius:20px;text-decoration:none;">𝕏 でシェアする</a></center>', unsafe_allow_html=True)


        # --- アフィリエイトエリア ---
        st.markdown("<br><br>", unsafe_allow_html=True) 
        st.caption("【PR】本ページはアフィリエイト広告を利用しています")
        
        st.subheader("🌙 INFPの感性を守る、今夜のしおり")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("https://m.media-amazon.com/images/I/81XyLz8B39L._SL1500_.jpg", width=130)
        with col2:
            st.markdown("#### 「気がつきすぎて疲れる」が根こそぎなくなる本")
            st.link_button("Amazonで詳しく見る", "https://amzn.to/4d4E96I")




# 8. フッター（最下部）
st.markdown("---")
# あなたの𝕏ユーザーID（@以降の英数字）を 'your_screen_name' に入れてください
x_id = "cotty_personal" 
footer_html = f"""
    <div style="text-align: center; color: #888; font-size: 0.8rem;">
    <div style="max-width: 600px; margin: 0 auto 20px auto; font-size: 0.7rem; color: #666; text-align: left; border-top: 1px solid #333; padding-top: 15px;">
            ※ 本サイトは、Amazon.co.jpを宣伝しリンクすることによって紹介料を獲得できる手段を提供することを目的に設定されたアフィリエイトプログラムである、Amazonアソシエイト・プログラムの参加者です。
        </div>
        Created by 
        <a href="https://x.com/{x_id}" target="_blank" style="color: #4B9CD3; text-decoration: none;">
            @{x_id}
        </a> 2026
    </div>
"""
st.markdown(footer_html, unsafe_allow_html=True)