import streamlit as st
import random

# Page configuration
st.set_page_config(
    page_title="Special Cinema Invitation / Invito Speciale al Cinema",
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
        "title": "🎬 A Special Invitation Awaits...",
        "subtitle": "Before you can see what this is about, you need to pass a couple of quick, fun tests! 😉",
        "step1": "Step 1: The Popcorn Mini-Game 🍿",
        "game_intro": "Catch the golden popcorn to unlock the cinema date! Click the correct box where the popcorn is hiding.",
        "caught": "🎉 You caught the golden popcorn! Step 1 complete!",
        "miss": "❌ Oops, just regular kernels! Try another box.",
        "step2": "Step 2: Easy 50s & 60s Cinema Quiz 🎥",
        "quiz_intro": "Let's test your retro film knowledge (French & Italian masterpieces)!",
        "q1": "1. Who directed the iconic 1960 Italian film 'La Dolce Vita'?",
        "q1_opts": ["Federico Fellini", "Jean-Luc Godard", "Vittorio De Sica"],
        "q2": "2. Which legendary French New Wave film features Antoine Doinel and was directed by François Truffaut in 1959?",
        "q2_opts": ["Breathless / À bout de souffle", "The 400 Blows / Les Quatre Cents Coups", "Hiroshima mon amour"],
        "q3": "3. Who was the iconic Italian actor starring alongside Anita Ekberg in the Trevi Fountain scene?",
        "q3_opts": ["Alain Delon", "Jean-Paul Belmondo", "Marcello Mastroianni"],
        "quiz_success": "🌟 Amazing! You passed the film quiz with flying colors!",
        "quiz_fail": "💡 Not quite! Review your classic cinema history and try again.",
        "step3": "Step 3: The Big Question 🍿❤️",
        "invitation_title": "You've unlocked the ultimate invitation!",
        "invitation_text": "Would you do me the absolute honor of going to the cinema with me?",
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
        "title": "🎬 Un Invito Speciale Ti Aspetta...",
        "subtitle": "Prima di scoprire di cosa si tratta, devi superare due piccoli test divertenti! 😉",
        "step1": "Fase 1: Il Mini-Gioco dei Popcorn 🍿",
        "game_intro": "Prendi il popcorn d'oro per sbloccare l'invito al cinema! Clicca sulla scatola giusta.",
        "caught": "🎉 Hai preso il popcorn d'oro! Fase 1 completata!",
        "miss": "❌ Ops, solo normali chicchi! Prova un'altra scatola.",
        "step2": "Fase 2: Facile Quiz sul Cinema degli Anni '50 e '60 🎥",
        "quiz_intro": "Mettiamo alla prova la tua conoscenza dei capolavori francesi e italiani!",
        "q1": "1. Chi ha diretto il celebre film italiano del 1960 'La Dolce Vita'?",
        "q1_opts": ["Federico Fellini", "Jean-Luc Godard", "Vittorio De Sica"],
        "q2": "2. Quale iconico film della Nouvelle Vague francese ha per protagonista Antoine Doinel (1959)?",
        "q2_opts": ["Fino all'ultimo respiro / À bout de souffle", "I 400 colpi / Les Quatre Cents Coups", "Hiroshima mon amour"],
        "q3": "3. Chi è il leggendario attore italiano accanto ad Anita Ekberg nella fontana di Trevi?",
        "q3_opts": ["Alain Delon", "Jean-Paul Belmondo", "Marcello Mastroianni"],
        "quiz_success": "🌟 Fantastico! Hai superato il quiz cinematografico a pieni voti!",
        "quiz_fail": "💡 Quasi! Ripassa un po' di cinema classico e riprova.",
        "step3": "Fase 3: La Grande Domanda 🍿❤️",
        "invitation_title": "Hai sbloccato l'invito definitivo!",
        "invitation_text": "Mi faresti l'immenso piacere di venire al cinema con me?",
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
                    # Shuffle winning box slightly to keep it fun
                    st.session_state.winning_box = random.randint(0, 2)
else:
    st.success(t["caught"])

st.markdown("---")

# --- STEP 2: CINEMA QUIZ ---
st.subheader(t["step2"])
if st.session_state.game_won:
    if not st.session_state.quiz_passed:
        st.write(t["quiz_intro"])
        
        q1_ans = st.radio(t["q1"], t["q1_opts"], key="q1_ans")
        q2_ans = st.radio(t["q2"], t["q2_opts"], key="q2_ans")
        q3_ans = st.radio(t["q3"], t["q3_opts"], key="q3_ans")
        
        if st.button("Submit Quiz Answers / Invia Risposte"):
            # Correct answers check
            correct_1 = q1_ans.startswith("Federico Fellini")
            correct_2 = q2_ans.startswith("The 400 Blows") or q2_ans.startswith("I 400 colpi")
            correct_3 = q3_ans.startswith("Marcello Mastroianni")
            
            if correct_1 and correct_2 and correct_3:
                st.session_state.quiz_passed = True
                st.success(t["quiz_success"])
                st.rerun()
            else:
                st.error(t["quiz_fail"])
    else:
        st.success(t["quiz_success"])
else:
    st.info("🔒 Complete Step 1 to unlock the cinema quiz! / Completa la Fase 1 per sbloccare il quiz!")

st.markdown("---")

# --- STEP 3: THE INVITATION & CONFIGURATION ---
st.subheader(t["step3"])
if st.session_state.quiz_passed:
    if not st.session_state.accepted:
        st.markdown(f"### ✨ {t['invitation_title']}")
        st.write(t["invitation_text"])
        
        col_yes, col_no = st.columns(2)
        
        with col_yes:
            if st.button(t["btn_yes"], type="primary"):
                st.session_state.accepted = True
                st.rerun()
                
        with col_no:
            no_texts = t["btn_no"]
            current_idx = min(st.session_state.no_click_count, len(no_texts) - 1)
            if st.button(no_texts[current_idx]):
                st.session_state.no_click_count += 1
                st.rerun()
    else:
        st.balloons()
        st.success(t["invitation_title"])
        
        st.markdown(f"### {t['config_title']}")
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            chosen_genre = st.selectbox(t["genre_label"], t["genres"])
            chosen_snack = st.selectbox(t["snack_label"], t["snacks"])
        with col_c2:
            chosen_date = st.date_input(t["date_label"])
            chosen_time = st.time_input(t["time_label"])
            
        if st.button(t["confirm_btn"], type="primary"):
            st.markdown("---")
            st.markdown(f"""
            <div class="ticket-box">
                <h2>{t['ticket_header']}</h2>
                <hr style="border: 1px dashed #ccc;">
                <p><b>{t['admit']}</b></p>
                <p>🎬 <b>Vibe/Genre:</b> {chosen_genre}</p>
                <p>🍿 <b>Snack:</b> {chosen_snack}</p>
                <p>📅 <b>Date:</b> {chosen_date} at {chosen_time}</p>
                <br>
                <p><i>{t['footer']}</i></p>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("🔒 Complete Step 2 to unlock the final invitation! / Completa la Fase 2 per sbloccare l'invito finale!")
