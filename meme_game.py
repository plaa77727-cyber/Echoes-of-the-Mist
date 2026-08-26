#run >> streamlit run meme_game.py
import streamlit as st
import random
import os
import base64
from io import BytesIO

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Meme TCG",
    page_icon="🃏",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------- UTIL ----------------
def load_images(folder):
    if not os.path.exists(folder):
        return []
    return [
        os.path.join(folder, img)
        for img in os.listdir(folder)
        if img.lower().endswith((".jpg", ".png", ".jpeg", ".webp"))
    ]

def image_to_base64(path, max_width=None):
    """Return base64 data-uri for an image file path."""
    try:
        with open(path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            # Try to infer mime:
            ext = os.path.splitext(path)[1].lower()
            mime = "image/png"
            if ext in [".jpg", ".jpeg"]:
                mime = "image/jpeg"
            elif ext == ".webp":
                mime = "image/webp"
            return f"data:{mime};base64,{b64}"
    except Exception:
        return ""

# ---------------- DATA ----------------
COMMON = load_images("nanami/Common")
RARE = load_images("nanami/Rare")
EPIC = load_images("nanami/Epic")
LEGENDARY = load_images("nanami/Legendary")

MEME_POOL = [
    {"name":"Nine","desc":"ยินดีด้วย คุณได้ Legendary! 🤯","power":10,"rarity":"Legendary","color":"#FFD700","images":LEGENDARY},
    {"name":"Good","desc":"ถือว่ายังดีนะ! 😒👌","power":9,"rarity":"Epic","color":"#A335EE","images":EPIC},
    {"name":"Good_boy","desc":"คราวหน้า Legendary แน่ๆ 😶","power":8,"rarity":"Epic","color":"#A335EE","images":EPIC},
    {"name":"bad","desc":"ต้องไปทำบุญบ้างแล้ว 🙏😔","power":7,"rarity":"Rare","color":"#0070DD","images":RARE},
    {"name":"So_bad","desc":"นี่มันเกลือชัดๆ 🤮😡","power":3,"rarity":"Common","color":"#FFFFFF","images":COMMON},
]

DROP_RATE = {
    "Legendary": 5,
    "Epic": 15,
    "Rare": 30,
    "Common": 50
}

def draw_card():
    rarity = random.choices(
        list(DROP_RATE.keys()),
        weights=list(DROP_RATE.values()),
        k=1
    )[0]

    pool = [c for c in MEME_POOL if c["rarity"] == rarity]
    card = random.choice(pool).copy()
    card["img"] = random.choice(card["images"]) if card["images"] else None
    return card

# ---------------- SESSION ----------------
if "collection" not in st.session_state:
    st.session_state.collection = []

if "last_card" not in st.session_state:
    st.session_state.last_card = None

if "show_collection" not in st.session_state:
    st.session_state.show_collection = False

# ---------------- STYLES / THEME ----------------
st.markdown(
    """
    <style>
    /* Full-page dark galaxy background with subtle animated stars */
    :root{
      --bg-color-1: #0b0714;
      --bg-color-2: #120822;
    }
    html, body, [data-testid="stAppViewContainer"] > .main {
      height: 100%;
    }
    .stApp {
      background: radial-gradient(ellipse at bottom left, rgba(46, 17, 66, 0.6), transparent 20%),
                  radial-gradient(ellipse at top right, rgba(11, 8, 40, 0.6), transparent 10%),
                  linear-gradient(180deg, var(--bg-color-1) 0%, var(--bg-color-2) 100%);
      color: #eae6ff;
      background-attachment: fixed;
      overflow-x: hidden;
    }

    /* animated twinkling stars layer */
    .stars, .twinkle {
      position: fixed;
      top: 0; left: 0; right:0; bottom:0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 0;
    }
    .stars::before {
      content: "";
      position: absolute;
      width: 3px; height: 3px;
      background: transparent;
      box-shadow:
        100px 200px #ffffff33,
        200px 120px #ffffff22,
        400px 320px #ffffff22,
        800px 20px #ffffff28,
        600px 420px #ffffff22,
        50px 60px #ffffff22,
        220px 520px #ffffff33,
        1200px 120px #ffffff22;
      animation: twinkle 6s linear infinite;
      opacity: 0.9;
    }
    @keyframes twinkle {
      0% {transform: translateY(0) scale(1); opacity: 0.9;}
      50% {transform: translateY(-10px) scale(1.05); opacity: 0.6;}
      100% {transform: translateY(0) scale(1); opacity: 0.9;}
    }

    /* Big animated title */
    .big-title {
      font-size: 4.2rem;
      font-weight: 900;
      text-align: center;
      margin: 28px 0 6px 0;
      color: #fff;
      letter-spacing: 1px;
      z-index: 10;
      text-shadow:
        0 0 8px rgba(168,85,247,0.9),
        0 0 20px rgba(168,85,247,0.6),
        0 0 40px rgba(147,112,219,0.5);
      background: linear-gradient(90deg, #ffffff, #c8a0ff 40%, #ffb3c9 70%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      animation: glow 2.6s ease-in-out infinite;
    }
    @keyframes glow {
      0% {filter: drop-shadow(0 0 8px rgba(147,112,219,0.6)); transform: translateY(0);}
      50% {filter: drop-shadow(0 0 20px rgba(236,72,153,0.55)); transform: translateY(-4px);}
      100% {filter: drop-shadow(0 0 8px rgba(147,112,219,0.6)); transform: translateY(0);}
    }

    /* Style the first (main) stButton to be the big Random Card CTA */
    div.stButton > button {
      background: linear-gradient(90deg, rgba(116,60,255,0.14), rgba(147,112,219,0.14));
      border: 2px solid rgba(168,85,247,0.35);
      color: #fff;
      padding: 18px 28px;
      font-size: 1.15rem;
      font-weight: 700;
      border-radius: 14px;
      box-shadow: 0 8px 30px rgba(147,112,219,0.15);
      transition: transform 0.18s ease, box-shadow 0.18s ease;
      backdrop-filter: blur(6px);
    }
    div.stButton > button:hover {
      transform: translateY(-4px) scale(1.02);
      box-shadow: 0 12px 40px rgba(147,112,219,0.28);
    }

    /* Small top-right collection button override (we place this separately) */
    .collection-btn {
      position: absolute;
      right: 28px;
      top: 22px;
      z-index: 20;
    }
    .collection-btn .stButton > button {
      background: rgba(66, 12, 79, 0.35);
      border: 2px solid rgba(168,85,247,0.35);
      padding: 10px 14px;
      font-weight: 700;
      border-radius: 10px;
      color: #fff;
    }

    /* Modal-like overlay for collection (rendered via HTML below) */
    .ang-modal-backdrop {
      position: fixed;
      inset: 0;
      background: rgba(3,2,10,0.6);
      backdrop-filter: blur(6px) saturate(120%);
      z-index: 2000;
      display:flex;
      align-items:center;
      justify-content:center;
      padding: 28px;
    }
    .ang-modal {
      width: min(1100px, 96%);
      max-height: 90vh;
      overflow-y: auto;
      background: linear-gradient(180deg, rgba(18,6,36,0.7), rgba(6,3,20,0.9));
      border-radius: 16px;
      border: 2px solid rgba(168,85,247,0.18);
      padding: 18px;
      box-shadow: 0 20px 60px rgba(2,1,5,0.6);
      color: #fff;
      position: relative;
    }
    .ang-modal .modal-header {
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap: 16px;
      margin-bottom: 8px;
    }
    .ang-modal .modal-grid {
      display:grid;
      grid-template-columns: repeat(auto-fill,minmax(200px,1fr));
      gap: 14px;
    }
    .ang-card {
      border-radius: 12px;
      overflow:hidden;
      padding:8px;
      background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
      border: 1px solid rgba(255,255,255,0.04);
    }
    .ang-card img {
      width: 100%;
      height: 230px;
      object-fit: cover;
      border-radius: 8px;
      display:block;
      background: #1b1030;
    }
    .ang-card .meta {
      margin-top:8px;
      display:flex;
      justify-content:space-between;
      align-items:center;
      font-weight:600;
      color:#eae6ff;
    }
    .ang-close {
      background: transparent;
      border: none;
      color: #fff;
      font-size: 1.1rem;
      padding: 8px 12px;
      cursor:pointer;
      border-radius:8px;
    }

    /* Responsive tweaks */
    @media (max-width: 600px) {
      .big-title { font-size: 2.6rem; margin-top: 18px; }
      div.stButton > button { padding: 14px 20px; font-size: 1rem; }
      .ang-card img { height: 160px; }
    }
    </style>

    <!-- star layers -->
    <div class="stars"></div>
    """,
    unsafe_allow_html=True,
)

# ---------------- HEADER / TITLE / CTA ----------------

# small top-right "ANG Collection" trigger (Streamlit button rendered in a container so it's separate)
col_top_left, col_top_right = st.columns([1, 6])
with col_top_left:
    st.write("")  # spacer
with col_top_right:
    # render nothing here, keep layout balanced
    st.write("")

# Place the collection button in a container positioned by CSS
st.markdown(
    """
    <div class="collection-btn">
    </div>
    """,
    unsafe_allow_html=True,
)

# Big animated title
st.markdown('<div class="big-title">MeMe Card ANG</div>', unsafe_allow_html=True)

# Subtitle / status
total_cards = sum(c["count"] for c in st.session_state.collection)
status_text = f"{total_cards} cards collected" if total_cards > 0 else "No cards yet. Start collecting!"
st.markdown(f'<p style="text-align:center; color: #cfc0ff96; margin-top:6px;">{status_text}</p>', unsafe_allow_html=True)

st.write("")  # spacing

# Random Card button (the first st.button on the page receives the big CTA styles)
if st.button("Random Card!", use_container_width=True):
    card = draw_card()
    st.session_state.last_card = card

    img = card["img"]
    matched = None

    for c in st.session_state.collection:
        if img and img in c["imgs"]:
            matched = c
            break

    if matched:
        matched["count"] += 1
    else:
        st.session_state.collection.append({
            "name": card["name"],
            "rarity": card["rarity"],
            "color": card["color"],
            "desc": card["desc"],
            "power": card["power"],
            "imgs": [img] if img else [],
            "count": 1
        })



st.divider()

# ---------------- LAST DRAW ----------------
if st.session_state.last_card:
    card = st.session_state.last_card
    # Card display box styled similar to React reference
    st.markdown(
        f"""
        <div style="
            border: 3px solid {card['color']};
            border-radius: 2px;
            padding: 6px;
            background: linear-gradient(180deg, rgba(26,11,46,0.6), rgba(6,3,20,0.6));
            color: white;
            text-align: center;
            max-width:500px;
            margin-left:auto;
            margin-right:auto;
            box-shadow: 0 8px 40px rgba(47,20,90,0.45);
        ">
            <p style="color:{card['color']}; font-weight:800; margin:0;">⭐ {card['rarity']}</p>
            <h2 style="margin:6px 0 6px 0; font-weight:900; font-size:1.5rem;">{card['name']}</h2>
            <p style="color:#aaa; margin:0 0 10px 0;">{card['desc']}</p>
            <div style="
                background:{card['color']};
                color:black;
                border-radius:8px;
                font-weight:1000;
                padding:4px 8px;
                display:inline-block;
                margin-top:8px;
            ">
                Power: {card['power']}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if card["img"]:
        st.image(card["img"], width=2500)

st.divider()

# ---------------- ANG COLLECTION (modal-like HTML overlay) ----------------
# Build modal HTML only when show_collection True and there are cards
if st.session_state.show_collection and len(st.session_state.collection) > 0:
    # Build gallery HTML with base64 images (so overlay works without Streamlit interactive elements)
    cards_html = ""
    for c in st.session_state.collection:
        # take first image if available, otherwise placeholder gradient
        img_html = ""
        if c.get("imgs"):
            first_img = c["imgs"][0]
            b64 = image_to_base64(first_img)
            if b64:
                img_html = f'<img src="{b64}" alt="{c["name"]}" />'
            else:
                img_html = f'<div style="height:230px;background:linear-gradient(180deg,#1b1030,#2a1138);border-radius:8px;"></div>'
        else:
            img_html = f'<div style="height:230px;background:linear-gradient(180deg,#1b1030,#2a1138);border-radius:8px;"></div>'

        cards_html += f"""
        <div class="ang-card">
          {img_html}
          <div class="meta">
            <div style="display:flex;flex-direction:column;">
              <span style="font-weight:800">{c['name']}</span>
              <small style="color:#cfc0ff99;">{c['rarity']}</small>
            </div>
            <div style="text-align:right;">
              <div style="font-weight:800; color:#ffd; font-size:0.95rem;">x{c['count']}</div>
            </div>
          </div>
        </div>
        """

    modal_html = f"""
    <div class="ang-modal-backdrop" id="angModal">
      <div class="ang-modal" role="dialog" aria-modal="true">
        <div class="modal-header">
          <div>
            <h2 style="margin:0 0 4px 0; font-size:1.25rem;">ANG Collection</h2>
            <div style="color:#cfc0ff99;">You have {total_cards} total cards</div>
          </div>
          <div>
            <button class="ang-close" onclick="document.getElementById('angModal').style.display='none'">✕ Close</button>
          </div>
        </div>

        <div style="margin-bottom:10px; color:#e6def9;">Tip: Close with the ✕ or the Streamlit "Close Collection" button.</div>

        <div class="modal-grid">
          {cards_html}
        </div>

        <div style="height:14px"></div>
      </div>
    </div>
    """

    st.markdown(modal_html, unsafe_allow_html=True)

    # Provide a Streamlit close button that clears the server-side flag on rerun
    if st.button("Close Collection"):
        st.session_state.show_collection = False

else:
    # If there are no cards or the modal is not requested, show a compact grid/expander for quick browsing
    with st.expander(f"ANG Collection ({total_cards} ใบ)"):
        if total_cards == 0:
            st.markdown('<div style="color:#cfc0ff99">Your collection is empty. Draw some cards!</div>', unsafe_allow_html=True)
        else:
            # render simple grid using st.columns
            per_row = 3
            for i in range(0, len(st.session_state.collection), per_row):
                row = st.columns(per_row)
                for j, card in enumerate(st.session_state.collection[i:i+per_row]):
                    with row[j]:
                        if card["imgs"]:
                            try:
                                st.image(card["imgs"][0], width=150)
                            except Exception:
                                st.write("")  # ignore if image fails
                        st.markdown(f"**{card['name']}**")
                        st.caption(f"{card['rarity']} • มี {card['count']} ใบ")