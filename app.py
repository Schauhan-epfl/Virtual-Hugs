import streamlit as st
import requests
import time
from datetime import date
import pandas as pd
import pydeck as pdk


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
    # This uses a transparent GIF of a floating heart
    st.markdown(
        """
        <div style="display: flex; justify-content: center;">
            <img src="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmdzeHhtbHJiaWp4bGFrZzNuc29hZnVteDhmcWZubWx6enZ6cnhmdyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/eawHU9reW91C9zIqd0/giphy.gif" width="150">
        </div>
        """, 
        unsafe_allow_html=True
    )
    # --- MAIN CONTENT 2 ---
    days_apart = (date.today() - START_DATE).days
    
    # Coordinates - Update these!
    LOC_B = [st.secrets["MY_LON"], st.secrets["MY_LAT"]]  # Pink Marker 
    LOC_A = [st.secrets["HER_LON"], st.secrets["HER_LAT"]] # Blue Marker 

    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("<h1>Virtual Hug</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='subtext'><b>{days_apart} Days</b> of loving you</p>", unsafe_allow_html=True)
    
    st.write("Tap the heart to send a hug across the map.")

    # State for animation
    if "pulse" not in st.session_state:
        st.session_state.pulse = False

    st.markdown('<div class="big-heart-btn">', unsafe_allow_html=True)
    if st.button("❤️"):
        st.session_state.pulse = True # Trigger map animation
        with st.status("Sending love...", expanded=True) as status:
            time.sleep(1)
            st.write("💖Connecting to my heart...")
            time.sleep(1)
            st.write("📱Making my phone buzz!")
            if send_telegram_hug(): 
                status.update(label="Hug Delivered! ❤️", state="complete")
                st.balloons()
            else:
                status.update(label="Connection error! 💔", state="error")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- THE ANIMATED MAP ---
    
    # Prepare data for the arc and points
    arc_data = pd.DataFrame([{
        "start": LOC_A,
        "end": LOC_B,
        "name": "Connection"
    }])

    # Define the layers
    layers = [
        # 1. The Curved Arc
        pdk.Layer(
            "ArcLayer",
            data=arc_data,
            get_source_position="start",
            get_target_position="end",
            get_source_color=[255, 77, 109, 200] if st.session_state.pulse else [255, 255, 255, 100],
            get_target_color=[0, 150, 255, 200] if st.session_state.pulse else [255, 255, 255, 100],
            width=5 if st.session_state.pulse else 2,
        ),
        # 2. Pink Marker (Location A)
        pdk.Layer(
            "ScatterplotLayer",
            data=pd.DataFrame([{"pos": LOC_A}]),
            get_position="pos",
            get_color=[255, 77, 109],
            get_radius=50000 if st.session_state.pulse else 20000, # Pulse effect
            pickable=True,
        ),
        # 3. Blue Marker (Location B)
        pdk.Layer(
            "ScatterplotLayer",
            data=pd.DataFrame([{"pos": LOC_B}]),
            get_position="pos",
            get_color=[0, 150, 255],
            get_radius=50000 if st.session_state.pulse else 20000, # Pulse effect
            pickable=True,
        ),
    ]

    # Create the map deck
    view_state = pdk.ViewState(
        latitude=(LOC_A[0] + LOC_B[0]) / 2,
        longitude=(LOC_A[1] + LOC_B[1]) / 2,
        zoom=2,
        pitch=45,
    )

    st.pydeck_chart(pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        map_style="satellite", # Clean, romantic look
    ))

    # Reset pulse after map renders
    if st.session_state.pulse:
        time.sleep(0.1)
        st.session_state.pulse = False

    st.caption("✨ Distance means nothing when someone means everything.")
    st.markdown('</div>', unsafe_allow_html=True)
