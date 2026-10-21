import streamlit as st
import random
import pandas as pd
from streamlit_gsheets import GSheetsConnection

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
        "name_step": "Step 0: Player Identification 🎟️",
        "name_label": "Enter your name to begin the challenge:",
        "name_btn": "Start Challenge 🎬",
        "step1": "Phase 1: Noir Cinema Showdown 🍿",
        "caught": "🎉 Villain Defeated! Phase 1 completed!",
        "unlock_btn": "➡️ Proceed to Phase 2: Cinema Quiz! 🎥",
        "manual_skip": "🔓 Defeated Villain? Click to Unlock Phase 2",
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
        "name_step": "Fase 0: Identificazione Giocatore 🎟️",
        "name_label": "Inserisci il tuo nome per iniziare la sfida:",
        "name_btn": "Inizia la Sfida 🎬",
        "step1": "Fase 1: Scontro Film Noir 🍿",
        "caught": "🎉 Cattivo Sconfitto! Fase 1 completata!",
        "unlock_btn": "➡️ Passa alla Fase 2: Quiz Cinematografico! 🎥",
        "manual_skip": "🔓 Cattivo sconfitto? Clicca per sbloccare la Fase 2",
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

# Banner Image
st.image("https://m.media-amazon.com/images/M/MV5BMTkxMjQ4NzU5N15BMl5BanBnXkFtZTgwMTkwODkzMTE@._V1_FMjpg_UX1000_.jpg", use_container_width=True)

st.title(t["title"])
st.write(t["subtitle"])
st.markdown("---")

# Initialize Session State
if "player_name" not in st.session_state:
    st.session_state.player_name = ""
if "game_won" not in st.session_state:
    st.session_state.game_won = False
if "quiz_passed" not in st.session_state:
    st.session_state.quiz_passed = False
if "no_click_count" not in st.session_state:
    st.session_state.no_click_count = 0
if "accepted" not in st.session_state:
    st.session_state.accepted = False

# --- STEP 0: PLAYER NAME INPUT ---
if not st.session_state.player_name:
    st.subheader(t["name_step"])
    name_input = st.text_input(t["name_label"], key="input_name")
    if st.button(t["name_btn"], type="primary"):
        if name_input.strip():
            st.session_state.player_name = name_input.strip()
            st.rerun()
        else:
            st.warning("Please enter a valid name / Per favore inserisci un nome valido")
    st.stop()

# Welcome Banner
st.markdown(f"### 👋 Welcome / Benvenuta/o, **{st.session_state.player_name}**!")
st.markdown("---")

# --- STEP 1: RETRO NOIR GAME ---
st.subheader(t["step1"])

query_params = st.query_params
if query_params.get("game_status") == "won":
    st.session_state.game_won = True

if not st.session_state.game_won:
    game_html = """
    <div style="text-align: center; background-color: #050508; padding: 12px; border-radius: 12px; border: 1px solid #333;">
        <canvas id="noirCanvas" width="600" height="350" style="border:2px solid #444; background: #000; max-width: 100%; border-radius: 8px;"></canvas>
        <div style="margin-top: 12px;">
            <button onclick="movePlayer(-20)" style="padding: 10px 18px; margin: 3px; font-weight: bold;">⬅️ Left</button>
            <button onclick="movePlayer(20)" style="padding: 10px 18px; margin: 3px; font-weight: bold;">➡️ Right</button>
            <button onclick="punch()" style="padding: 10px 18px; margin: 3px; background-color: #ff4b4b; color: white; font-weight: bold; border-radius: 6px;">🥊 Punch</button>
            <button onclick="flashAttack()" style="padding: 10px 18px; margin: 3px; background-color: #faca2b; font-weight: bold; border-radius: 6px;">📸 Flash</button>
        </div>
        <p style="color: #888; font-size: 12px; margin-top: 8px;">Controls: Buttons or Keyboard (A/D or Arrows to Move, Space to Punch, S for Flash)</p>
    </div>

    <script>
    const canvas = document.getElementById("noirCanvas");
    const ctx = canvas.getContext("2d");

    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    
    function playSound(type) {
        if (audioCtx.state === 'suspended') { audioCtx.resume(); }
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.connect(gain);
        gain.connect(audioCtx.destination);

        if (type === 'punch') {
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(150, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(30, audioCtx.currentTime + 0.15);
            gain.gain.setValueAtTime(0.5, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.15);
            osc.start();
            osc.stop(audioCtx.currentTime + 0.15);
        } else if (type === 'flash') {
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(800, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(200, audioCtx.currentTime + 0.3);
            gain.gain.setValueAtTime(0.6, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);
            osc.start();
            osc.stop(audioCtx.currentTime + 0.3);
        } else if (type === 'win') {
            osc.type = 'sine';
            osc.frequency.setValueAtTime(400, audioCtx.currentTime);
            osc.frequency.setValueAtTime(600, audioCtx.currentTime + 0.1);
            osc.frequency.setValueAtTime(800, audioCtx.currentTime + 0.2);
            gain.gain.setValueAtTime(0.5, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.4);
            osc.start();
            osc.stop(audioCtx.currentTime + 0.4);
        }
    }

    let player = { x: 90, y: 190, w: 55, h: 120, hp: 100, attacking: false };
    let boss = { x: 440, y: 180, w: 65, h: 130, hp: 30, state: 'idle' };
    let gameOver = false;
    let rain = [];

    for(let i=0; i<30; i++) {
        rain.push({ x: Math.random()*600, y: Math.random()*350, l: Math.random()*15+5, s: Math.random()*5+10 });
    }

    function drawRain() {
        ctx.strokeStyle = "rgba(200, 200, 220, 0.25)";
        ctx.lineWidth = 1;
        for(let r of rain) {
            ctx.beginPath();
            ctx.moveTo(r.x, r.y);
            ctx.lineTo(r.x - 2, r.y + r.l);
            ctx.stroke();
            r.y += r.s;
            r.x -= 1;
            if(r.y > 350) { r.y = 0; r.x = Math.random()*600; }
        }
    }

    function drawTexturePlayer() {
        ctx.fillStyle = "#2b2b36";
        ctx.fillRect(player.x, player.y + 35, player.w, 75);
        ctx.fillStyle = "#e6d7c3";
        ctx.fillRect(player.x + 20, player.y + 35, 15, 15);
        ctx.fillStyle = "#aa2222";
        ctx.fillRect(player.x + 26, player.y + 40, 4, 18);
        ctx.fillStyle = "#d1a884";
        ctx.fillRect(player.x + 15, player.y + 12, 25, 23);
        ctx.fillStyle = "#1a1a24";
        ctx.fillRect(player.x + 5, player.y + 10, 45, 7);
        ctx.fillRect(player.x + 12, player.y - 8, 31, 18);

        if (player.attacking) {
            ctx.fillStyle = "#d1a884";
            ctx.fillRect(player.x + player.w, player.y + 45, 30, 14);
        }
    }

    function drawTextureBoss() {
        let isHit = boss.state === 'hit';
        ctx.fillStyle = isHit ? "#881a1a" : "#181313";
        ctx.fillRect(boss.x, boss.y + 40, boss.w, 85);
        ctx.fillStyle = "#a8866b";
        ctx.fillRect(boss.x + 18, boss.y + 12, 28, 28);
        ctx.fillStyle = "#ff2222";
        ctx.fillRect(boss.x + 24, boss.y + 22, 5, 4);
        ctx.fillRect(boss.x + 36, boss.y + 22, 5, 4);
        ctx.fillStyle = "#0a0808";
        ctx.fillRect(boss.x + 8, boss.y + 10, 50, 7);
        ctx.fillRect(boss.x + 16, boss.y - 10, 34, 20);
    }

    function drawScene() {
        ctx.fillStyle = "#08080c";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = "#121218";
        ctx.fillRect(0, 290, canvas.width, 60);

        let grad = ctx.createRadialGradient(300, 40, 10, 300, 200, 280);
        grad.addColorStop(0, "rgba(255, 245, 200, 0.28)");
        grad.addColorStop(1, "rgba(0, 0, 0, 0.85)");
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        drawRain();
        drawTexturePlayer();
        drawTextureBoss();

        ctx.fillStyle = "#222";
        ctx.fillRect(20, 15, 160, 18);
        ctx.fillRect(420, 15, 160, 18);

        ctx.fillStyle = "#00e676";
        ctx.fillRect(22, 17, player.hp * 1.56, 14);
        ctx.fillStyle = "#ff1744";
        ctx.fillRect(422, 17, boss.hp * 5.2, 14);

        ctx.strokeStyle = "#fff";
        ctx.strokeRect(20, 15, 160, 18);
        ctx.strokeRect(420, 15, 160, 18);
    }

    function updateBoss() {
        if (gameOver) return;
        if (Math.abs(player.x - boss.x) > 65) {
            if (boss.x > player.x) boss.x -= 1.2;
            else boss.x += 1.2;
        }
    }

    function triggerWin() {
        gameOver = true;
        playSound('win');
        setTimeout(() => {
            const url = new URL(window.location.href);
            url.searchParams.set("game_status", "won");
            window.parent.location.href = url.href;
        }, 200);
    }

    function movePlayer(dx) {
        if (gameOver) return;
        player.x = Math.max(10, Math.min(canvas.width - 70, player.x + dx));
    }

    function punch() {
        if (gameOver) return;
        playSound('punch');
        player.attacking = true;
        setTimeout(() => { player.attacking = false; }, 150);

        if (Math.abs((player.x + player.w) - boss.x) < 55) {
            boss.hp -= 15;
            boss.state = 'hit';
            setTimeout(() => { boss.state = 'idle'; }, 150);
            if (boss.hp <= 0) {
                boss.hp = 0;
                triggerWin();
            }
        }
    }

    function flashAttack() {
        if (gameOver) return;
        playSound('flash');
        ctx.fillStyle = "#ffffff";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        boss.hp -= 30;
        if (boss.hp <= 0) {
            boss.hp = 0;
            triggerWin();
        }
    }

    window.addEventListener("keydown", (e) => {
        if (e.key === "a" || e.key === "ArrowLeft") movePlayer(-20);
        if (e.key === "d" || e.key === "ArrowRight") movePlayer(20);
        if (e.key === " ") punch();
        if (e.key === "s" || e.key === "S") flashAttack();
    });

    function gameLoop() {
        drawScene();
        updateBoss();
        requestAnimationFrame(gameLoop);
    }

    gameLoop();
    </script>
    """
    st.components.v1.html(game_html, height=430)
    
    # Manual bypass button directly visible under game
    if st.button(t["manual_skip"]):
        st.session_state.game_won = True
        st.rerun()

else:
    st.success(t["caught"])
    if st.button(t["unlock_btn"], type="primary"):
        st.session_state.game_won = True
        st.rerun()

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
    st.info("🔒 Defeat the Villain in Phase 1 to unlock the quiz!")

st.markdown("---")

# --- STEP 3: THE SECRET REWARD (DATE INVITATION) ---
if st.session_state.quiz_passed:
    st.subheader(t["step3"])
    if not st.session_state.accepted:
        st.markdown(f"### ✨ {t['invitation_title']}")
        st.write(f"Dear **{st.session_state.player_name}**, {t['invitation_text']}")
        
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
        
        # Les Quatre Cents Coups Still Image
        st.image("https://m.media-amazon.com/images/M/MV5BODZiZjAzYzUtMDUwNS00Y2UwLWIwNDUtNTJjOTZkNzU3NGY1XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg", caption="Les Quatre Cents Coups (1959) 🎞️", use_container_width=True)
        
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
                <p><b>Guest: {st.session_state.player_name}</b></p>
                <p><b>{t['admit']}</b></p>
                <p>🎬 <b>Vibe/Genre:</b> {chosen_genre}</p>
                <p>🍿 <b>Snack:</b> {chosen_snack}</p>
                <p>📅 <b>Date:</b> {chosen_date} at {chosen_time}</p>
                <br>
                <p><i>{t['footer']}</i></p>
            </div>
            """, unsafe_allow_html=True)
            
            # --- SAVE RESPONSES TO GOOGLE SHEETS ---
            try:
                conn = st.connection("gsheets", type=GSheetsConnection)
                existing_data = conn.read(worksheet="Sheet1", ttl=0)
                
                new_row = pd.DataFrame([{
                    "Name": st.session_state.player_name,
                    "Status": "Accepted",
                    "Genre": chosen_genre,
                    "Snack": chosen_snack,
                    "Date": str(chosen_date),
                    "Time": str(chosen_time)
                }])
                
                updated_df = pd.concat([existing_data, new_row], ignore_index=True)
                conn.update(worksheet="Sheet1", data=updated_df)
                st.toast("Saved to Google Sheet! 📊", icon="✅")
            except Exception as e:
                pass
