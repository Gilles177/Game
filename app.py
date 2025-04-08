import streamlit as st
from PIL import Image
import base64
import os

st.set_page_config(
    page_title="Pong + Tetris Mix",
    layout="centered",
    page_icon="🎮",
)

# --- Custom CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Orbitron', sans-serif;
        background-color: #0b0f1a;
        color: #f5f5f5;
    }

    .glow-button {
        background-color: #1f1f2e;
        border: none;
        color: white;
        padding: 12px 24px;
        text-align: center;
        font-size: 16px;
        margin: 10px auto;
        display: block;
        border-radius: 8px;
        box-shadow: 0 0 10px #00ffe5, 0 0 20px #00ffe5;
        transition: 0.3s ease-in-out;
    }

    .glow-button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px #00ffe5, 0 0 30px #00ffe5;
        cursor: pointer;
    }

    .title-glow {
        color: #00ffe5;
        text-shadow: 0 0 10px #00ffe5, 0 0 20px #00ffe5;
        font-size: 48px;
        text-align: center;
    }

    .subtitle {
        text-align: center;
        font-size: 20px;
        color: #c7f0ff;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Title Section ---
st.markdown('<div class="title-glow">Pong + Tetris Mix</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">by Gilles G. Yamdeu Youtebo</div>', unsafe_allow_html=True)

# --- Screenshot Preview ---
if os.path.exists("assets/screenshots/screenshot_0.png"):
    image = Image.open("assets/screenshots/screenshot_0.png")
    st.image(image, caption="🚀 Game Preview", use_column_width=True)

# --- Description ---
st.markdown("### 💡 About the Game")
st.markdown("""
This is a **neon-infused arcade mashup** of classic Pong and Tetris, where:
- Blocks fall like Tetris...
- You bounce a ball like Pong...
- Bosses appear at the end of every level...
- Germs invade starting from Level 3...

🧠 Built with **Python, Pygame**, and **love for retro sci-fi design**.
""")

# --- Download Button (Local) ---
st.markdown("### 🎮 Play the Game")

st.markdown('<a class="glow-button" href="https://github.com/Gilles177/Game" target="_blank">Download from GitHub</a>', unsafe_allow_html=True)

# --- Gameplay Instructions ---
st.markdown("### 🎯 How to Play")
st.markdown("""
- Use **←** and **→** arrow keys to move the paddle.
- Bounce the ball to destroy falling blocks.
- Avoid missing the ball!
- Germ enemies show up from level 3!
- End-of-level bosses await your challenge 💀
""")

# --- Credits / Footer ---
st.markdown("### 🌍 Share & Contribute")
st.markdown("""
Want to contribute or fork your own version? Visit the repo 👇
🔗 [GitHub: Gilles177/Game](https://github.com/Gilles177/Game)
""")

# Optional: Footer glow
st.markdown("""
<hr style="border: 1px solid #00ffe5;">
<div style="text-align:center; font-size:14px; color:#777;">Made with 💻 + 🎮 using Pygame & Streamlit</div>
""", unsafe_allow_html=True)
