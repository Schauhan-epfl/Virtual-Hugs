import streamlit as st
import requests
import time
from datetime import date

# --- ⚙️ CONFIGURATION ---
TOKEN = st.secrets["TOKEN"]
CHAT_ID = st.secrets["CHAT_ID"]
PASSWORD = st.secrets["APP_PASSWORD"]
START_DATE = date(2025, 6, 22)

# --- 🎨 UI STYLING ---
def apply_custom_styles():
    st.set_page_config(page_title="For You", page_icon="❤️", layout="centered")
    
    # Note: Double {{ }} are required because this is an f-string
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Dancing+Script:wght@700&display=swap');
        
        .stApp {{
            background: linear-gradient(135deg, #ffafbd 0%, #ffc3a0 100%);
        }}

        #MainMenu, footer, header {{ visibility: hidden; }}

        .main-card {{
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 30px;
            padding: 50px 40px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            text-align: center;
            margin: 20px auto;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            max-width: 450px;
        }}

        h1 {{
            font-family: 'Dancing Script', cursive;
            color: white;
            font-size: 4rem !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 5px;
        }}

        .subtext {{
            font-family: 'Inter', sans-serif;
            color: white;
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 30px;
        }}

        .stTextInput div[data-baseweb="input"] {{
            background-color: rgba(255, 255, 255, 0.9) !important;
            border-radius: 20px !important;
            border: 2px solid rgba(255, 77, 109, 0.2) !important;
        }}
        
        /* The Big Pulsing Heart Button */
        @keyframes heart-beat {{
            0% {{ transform: scale(1); box-shadow: 0 10px 30px rgba(214, 51, 132, 0.4); }}
            14% {{ transform: scale(1.15); }}
            28% {{ transform: scale(1); }}
            42% {{ transform: scale(1.3); box-shadow: 0 15px 50px rgba(214, 51, 132, 0.7); }}
            70% {{ transform: scale(1); box-shadow: 0 10px 30px rgba(214, 51, 132, 0.4); }}
        }}

        .big-heart-btn > div > button {{
            background: linear-gradient(145deg, #ff4d6d, #c9184a) !important;
            color: white !important;
            height: 200px !important; /* Increased size */
            width: 200px !important;  /* Increased size */
            border-radius: 50% !important;
            font-size: 80px !important; /* Bigger Emoji */
            border: 8px solid rgba(255, 255, 255, 0.6) !important;
            animation: heart-beat 1.5s infinite cubic-bezier(0.215, 0.61, 0.355, 1) !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            margin: 40px auto !important;
            transition: all 0.3s ease !important;
            line-height: 1 !important;
        }}

        .big-heart-btn > div > button:hover {{
            transform: scale(1.1) !important; /* Controlled hover so it doesn't clash with animation */
            border-color: white !important;
            filter: brightness(1.1);
        }}
        </style>
    """, unsafe_allow_html=True)

# --- 🛠️ HELPER FUNCTIONS ---
def send_telegram_hug():
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": "She sent you a hug! ❤️🫂"}
    try:
        response = requests.post(url, data=payload)
        return response.status_code == 200
    except Exception:
        return False

# --- 🚀 APP LOGIC ---
apply_custom_styles()

if "auth" not in st.session_state:
    st.session_state.auth = False

# --- LOGIN SCREEN ---
if not st.session_state.auth:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("<h1>Private Access</h1>", unsafe_allow_html=True)
    
    pwd = st.text_input("Password", placeholder="Our secret word...", type="password", label_visibility="collapsed")
    
    if st.button("Unlock 🔑", use_container_width=True):
        if pwd.lower() == PASSWORD.lower():
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("That's not it, try again! ❤️")
    st.markdown('</div>', unsafe_allow_html=True)
    
else:
    # --- MAIN CONTENT ---
    days_apart = (date.today() - START_DATE).days
    
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("<h1>Virtual Hug</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='subtext'><b>{days_apart} Days</b> of loving you</p>", unsafe_allow_html=True)
    
    st.write("Tap the heart to let me know you're thinking of me.")

    st.markdown('<div class="big-heart-btn">', unsafe_allow_html=True)
    
    if st.button("❤️"):
        with st.status("Sending love...", expanded=False) as status:
            st.write("Connecting to my heart...")
            time.sleep(1)
            st.write("Making my phone buzz!")
            time.sleep(1.5)
            st.write("I felt your hug!")
            
            if send_telegram_hug(): 
                status.update(label="Hug Delivered! ❤️", state="complete")
                st.balloons()
            else:
                status.update(label="Connection error! 💔", state="error")
                
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.caption("✨ Added to your Home Screen for easy access!")
    st.markdown('</div>', unsafe_allow_html=True)
