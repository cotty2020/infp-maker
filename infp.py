
import streamlit as st
import google.generativeai as genai
import urllib.parse

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
            /* 右下の「Manage App」ボタンやGitHubへのリンクが含まれる要素を強制抹消 */
button[data-testid="stManageAppButton"],
.stAppDeployButton,
a[href*="streamlit"] {
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
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            return genai.GenerativeModel(m.name)
    return None

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

if st.button("INFP風に変換する！", use_container_width=True):
    with st.spinner("思考回路を書き換え中..."):
        instruction = mbti_data[selected_type]["desc"]
        prompt = f"以下の文章を、{instruction}\n\n文章：{user_input}"
        
        response = model.generate_content(prompt)
        
        st.markdown("### 🎁 変換結果")
        st.success(response.text)

       
        # --- 余白（結果とシェアボタンの間） ---
        st.write("") 
        st.write("")
        # SNSボタン
        # 1. あなたのアプリの新しいURL
        app_url = "https://infp-maker.streamlit.app/" 

        # 2. ツイート文面の構築
        tweet_text = (
           f"【#INFPメーカー】で文章を変換してみたよ！✨\n\n"
           f"「{response.text[:60]}...」\n\n" # 結果をチラ見せして興味を引く
           f"▼ ここで変換できるよ\n{app_url}\n\n"
           f"Created by @cotty_personal\n"
           f"#MBTI #INFP"
)

        # 3. URLエンコードしてシェア用URLを作成
        tweet_url = f"https://twitter.com/intent/tweet?text={urllib.parse.quote(tweet_text)}"
        
        # センター寄せ＆少し余裕を持たせたデザイン
        st.markdown(
            f'<div style="text-align: center; margin: 20px 0;">'
            f'<a href="{tweet_url}" target="_blank" style="background-color:#1DA1F2;color:white;padding:12px 30px;border-radius:25px;text-decoration:none;font-weight:bold;box-shadow: 0 4px 15px rgba(29, 161, 242, 0.3);">𝕏 で結果をシェアする</a>'
            f'</div>', 
            unsafe_allow_html=True
        )

        
        # ---------------------------------------------------------
        # ここから追記：アフィリエイトエリア
        # ---------------------------------------------------------
        # --- 大きめの余白（シェアと広告の間。ここが「心理的な区切り」になります） ---
        st.markdown("<br><br><br>", unsafe_allow_html=True) 

        # 3. アフィリエイトエリア（「おすすめ」として提示）
        st.caption("【PR】本ページはアフィリエイト広告を利用しています")
        
        # 境界線（うっすらと）
        st.markdown("---")
        
        st.subheader("🌙 INFPの感性を守る、今夜のしおり")
        st.write("このメーカーを気に入ってくれたあなたへ。私が救われた「自分を愛するための本」を紹介させてください。")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("https://m.media-amazon.com/images/I/81XyLz8B39L._SL1500_.jpg", width=130)
            
        with col2:
            st.markdown("#### 「気がつきすぎて疲れる」が根こそぎなくなる本")
            st.write("繊細さは、治すべき「弱さ」ではなく、守るべき「才能」です。もっと楽に呼吸するためのヒントがここにあります。")
            # Amazonカラー（オレンジ系）のボタンで視覚的に区別
            st.link_button("Amazonで詳しく見る", "https://amzn.to/4d4E96I")

        st.markdown("---")
        # ---------------------------------------------------------





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