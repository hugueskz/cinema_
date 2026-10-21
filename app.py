import streamlit as st
import random

# Page configuration
st.set_page_config(
    page_title="Classic Cinema Challenge / Challenge Cinema Classico",
    page_icon="🎬",
    layout="centered"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
    }
    .ticket-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 25px;
        border-radius: 15px;
        color: #1f1f1f;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        border: 2px dashed #ff4b4b;
    }
    </style>
""", unsafe_allow_html=True)

# Language Selector in Sidebar
st.sidebar.title("🌍 Language / Lingua")
lang = st.sidebar.radio("Choose / Scegli:", ["English", "Italiano"])

# Translations dictionary
t = {
    "English": {
        "title": "🎬 The Great Classic Film Challenge",
        "subtitle": "Test your reflexes and classic 50s & 60s cinema knowledge to unlock your official score!",
        "step1": "Phase 1: Popcorn Reflex Test 🍿",
        "game_intro": "Before testing your cinema knowledge, let's test your focus! Find the hidden golden popcorn box.",
        "caught": "🎉 Perfect reflexes! Phase 1 completed!",
        "miss": "❌ Just empty kernels! Try another box.",
        "step2": "Phase 2: 50s & 60s French & Italian Cinema Quiz 🎥",
        "quiz_intro": "Answer these 3 classic movie questions to calculate your Film Critic Rank:",
        "q1": "1. Who directed the iconic 1960 Italian film 'La Dolce Vita'?",
        "q1_opts": ["Federico Fellini", "Jean-Luc Godard", "Vittorio De Sica"],
        "q2": "2. Which legendary French New Wave film features Antoine Doinel and was directed by François Truffaut in 1959?",
        "q2_opts": ["Breathless / À bout de souffle", "The 400 Blows / Les Quatre Cents Coups", "Hiroshima mon amour"],
        "q3": "3. Who was the iconic Italian actor starring alongside Anita Ekberg in the Trevi Fountain scene?",
        "q3_opts": ["Alain Delon", "Jean-Paul Belmondo", "Marcello Mastroianni"],
        "quiz_success": "🌟 100% Correct! You unlocked the secret reward...",
        "quiz_fail": "💡 Not quite! Review your classic cinema history and try again.",
        "step3": "🎁 Secret Reward Unlocked!",
        "invitation_title": "Surprise! 🎬❤️",
        "invitation_text": "Since you clearly know your movies and have great taste, would you do me the honor of going to the cinema with me?",
        "btn_yes": "YES! Absolutely! 🥰",
        "btn_no": [
            "No",
            "Are you sure? 🥺",
            "Think about the popcorn! 🍿",
            "Pretty please? 🥺",
            "The button is lying to you, click YES!",
            "Resistance is futile! 💖"
        ],
        "config_title": "🎟️ Configure Our Date Details",
        "genre_label": "Movie Vibe / Genre:",
        "genres": ["Classic Black & White 🎞️", "Romantic Drama ❤️", "Italian Comedy 😄", "Mystery & Suspense 🕵️‍♂️"],
        "snack_label": "Choose our theater snacks:",
        "snacks": ["Large Popcorn to share 🍿", "Sweet & Salty Mix 🥨", "Gummy Candies 🍬", "Nachos with extra cheese 🧀"],
        "date_label": "Pick our date:",
        "time_label": "Pick our time:",
        "confirm_btn": "Generate Our Ticket! 🎫",
        "ticket_header": "🎟️ OFFICIAL CINEMA TICKET 🎟️",
        "admit": "ADMIT TWO",
        "footer": "Can't wait to see you there! ✨"
    },
    "Italiano": {
        "title": "🎬 Il Grande Test sul Cinema Classico",
        "subtitle": "Metti alla prova i tuoi riflessi e le tue conoscenze sul cinema anni '50 e '60 per sbloccare il tuo punteggio!",
        "step1": "Fase 1: Test di Riflessi Popcorn 🍿",
        "game_intro": "Prima del quiz cinematografico, testiamo la tua concentrazione! Trova la scatola con il popcorn d'oro.",
        "caught": "🎉 Riflessi perfetti! Fase 1 completata!",
        "miss": "❌ Solo chicchi vuoti! Prova un'altra scatola.",
        "step2": "Fase 2: Quiz sul Cinema Francese e Italiano Anni '50 e '60 🎥",
        "quiz_intro": "Rispondi a queste 3 domande per scoprire il tuo livello di Critico Cinematografico:",
        "q1": "1. Chi ha diretto il celebre film italiano del 1960 'La Dolce Vita'?",
        "q1_opts": ["Federico Fellini", "Jean-Luc Godard", "Vittorio De Sica"],
        "q2": "2. Quale iconico film della Nouvelle Vague francese ha per protagonista Antoine Doinel (1959)?",
        "q2_opts": ["Fino all'ultimo respiro / À bout de souffle", "I 400 colpi / Les Quatre Cents Coups", "Hiroshima mon amour"],
        "q3": "3. Chi è il leggendario attore italiano accanto ad Anita Ekberg nella fontana di Trevi?",
        "q3_opts": ["Alain Delon", "Jean-Paul Belmondo", "Marcello Mastroianni"],
        "quiz_success": "🌟 100% Corretto! Hai sbloccato la ricompensa segreta...",
        "quiz_fail": "💡 Quasi! Ripassa un po' di cinema classico e riprova.",
        "step3": "🎁 Ricompensa Segreta Sbloccata!",
        "invitation_title": "Sorpresa! 🎬❤️",
        "invitation_text": "Visto che te ne intendi di cinema e hai un ottimo gusto, mi faresti l'onore di venire al cinema con me?",
        "btn_yes": "SI! Assolutamente! 🥰",
        "btn_no": [
            "No",
            "Sei sicura/o? 🥺",
            "Pensa ai popcorn! 🍿",
            "Per favore, per favore? 🥺",
            "Questo pulsante mente, clicca su SI!",
            "La resistenza è inutile! 💖"
        ],
        "config_title": "🎟️ Configura i Dettagli del Nostro Appuntamento",
        "genre_label": "Genere / Atmosfera del film:",
        "genres": ["Classico in Bianco e Nero 🎞️", "Dramma Romantico ❤️", "Commedia all'italiana 😄", "Giallo & Suspense 🕵️‍♂️"],
        "snack_label": "Scegli gli snack per il cinema:",
        "snacks": ["Grande Popcorn da condividere 🍿", "Mix Dolce e Salato 🥨", "Caramelle Gommose 🍬", "Nachos con extra formaggio 🧀"],
        "date_label": "Scegli la data:",
        "time_label": "Scegli l'orario:",
        "confirm_btn": "Genera il Nostro Biglietto! 🎫",
        "ticket_header": "🎟️ BIGLIETTO CINEMATOGRAFICO UFFICIALE 🎟️",
        "admit": "VALIDO PER DUE",
        "footer": "Non vedo l'ora di vederti! ✨"
    }
}[lang]

st.title(t["title"])
st.write(t["subtitle"])
st.markdown("---")

# Initialize Session State
if "game_won" not in st.session_state:
    st.session_state.game_won = False
if "winning_box" not in st.session_state:
    st.session_state.winning_box = random.randint(0, 2)
if "quiz_passed" not in st.session_state:
    st.session_state.quiz_passed = False
if "no_click_count" not in st.session_state:
    st.session_state.no_click_count = 0
if "accepted" not in st.session_state:
    st.session_state.accepted = False

# --- STEP 1: POPCORN MINI-GAME ---
st.subheader(t["step1"])
if not st.session_state.game_won:
    st.write(t["game_intro"])
    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            if st.button(f"📦 Box {i+1}", key=f"box_{i}"):
                if i == st.session_state.winning_box:
                    st.session_state.game_won = True
                    st.rerun()
                else:
                    st.warning(t["miss"])
                    st.session_state.winning_box = random.randint(0, 2)
else:
    st.success(t["caught"])

st.markdown("---")

# --- STEP 2: CINEMA QUIZ ---
st.subheader(t["step2"])
if st.session_state.game_won:
    if not st.session_state.quiz_passed:
        st.write(t["quiz_intro"])
        
        q1_ans = st.radio(t
