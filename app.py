import streamlit as st
import random
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Shadows of Rome / Paris Noir - Cinema Challenge",
    page_icon="🎬",
    layout="centered"
)

# Optional Google Sheets connection check
try:
    from streamlit_gsheets import GSheetsConnection
    GSHEETS_AVAILABLE = True
except ImportError:
    GSHEETS_AVAILABLE = False

# Custom CSS for dark cinema aesthetic
st.markdown("""
    <style>
    .main {
        background-color: #0c0d10;
        color: #e0e0e0;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        background-color: #222;
        color: #d4af37;
        border: 1px solid #d4af37;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #d4af37;
        color: #111;
    }
    .ticket-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 25px;
        border-radius: 15px;
        color: #1f1f1f;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.6);
        border: 2px dashed #ff4b4b;
        margin-top: 20px;
    }
    .noir-card {
        border: 2px solid #444;
        border-radius: 12px;
        padding: 15px;
        background-color: #121318;
        box-shadow: 0 0 25px rgba(0, 0, 0, 0.8);
    }
    </style>
""", unsafe_allow_html=True)

# Language Selector in Sidebar
st.sidebar.title("🌍 Language / Lingua")
lang = st.sidebar.radio("Choose / Scegli:", ["English", "Italiano"])

# Translations dictionary
t = {
    "English": {
        "title": "🎬 Shadows of Rome / Paris Noir",
        "subtitle": "Battle 'The Shadow Critic' in this 1950s Film Noir Thriller to unlock your secret cinema invite!",
        "step1": "Phase 1: Defeat 'The Shadow Critic' 🕵️‍♂️",
        "game_intro": "Move with A/D or Arrow Keys. Press SPACE or CLICK to Punch / Flash Photo. Press S or Down Arrow to Dodge!",
        "caught": "🎉 You defeated The Shadow Critic! Secret Reward Unlocked!",
        "step2": "Phase 2: 50s & 60s French & Italian Cinema Quiz 🎥",
        "quiz_intro": "Answer these 3 classic movie questions to calculate your Film Critic Rank:",
        "q1": "1. Who directed the iconic 1960 Italian film 'La Dolce Vita'?",
        "q1_opts": ["Federico Fellini", "Jean-Luc Godard", "Vittorio De Sica"],
        "q2": "2. Which legendary French New Wave film features Antoine Doinel and was directed by François Truffaut in 1959?",
        "q2_opts": ["Breathless / À bout de souffle", "The 400 Blows / Les Quatre Cents Coups", "Hiroshima mon amour"],
        "q3": "3. Who was the iconic Italian actor starring alongside Anita Ekberg in the Trevi Fountain scene?",
        "q3_opts": ["Alain Delon", "Jean-Paul Belmondo", "Marcello Mastroianni"],
        "quiz_success": "🌟 100% Correct! You unlocked the official invitation...",
        "quiz_fail": "💡 Not quite! Review your classic cinema history and try again.",
        "step3": "🎁 Secret Reward Unlocked!",
        "invitation_title": "Surprise! 🎬❤️",
        "invitation_text": "Since you clearly have heroic reflexes and incredible taste in 50s & 60s cinema, would you do me the honor of going to the movies with me?",
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
        "title": "🎬 Ombre di Roma / Parigi Noir",
        "subtitle": "Sconfiggi 'Il Critico Mascherato' in questo thriller Noir anni '50 per sbloccare l'invito segreto!",
        "step1": "Fase 1: Sconfiggi 'Il Critico Mascherato' 🕵️‍♂️",
        "game_intro": "Usa A/D o Frecce per muoverti. Premi SPAZIO o CLICCA per Sferrare un Pugno / Flash. Premi S o Freccia Giù per Schivare!",
        "caught": "🎉 Hai sconfitto Il Critico Mascherato! Premio Segreto Sbloccato!",
        "step2": "Fase 2: Quiz sul Cinema Francese e Italiano Anni '50 e '60 🎥",
        "quiz_intro": "Rispondi a queste 3 domande per scoprire il tuo livello di Critico Cinematografico:",
        "q1": "1. Chi ha diretto il celebre film italiano del 1960 'La Dolce Vita'?",
        "q1_opts": ["Federico Fellini", "Jean-Luc Godard", "Vittorio De Sica"],
        "q2": "2. Quale iconico film della Nouvelle Vague francese ha per protagonista Antoine Doinel (1959)?",
        "q2_opts": ["Fino all'ultimo respiro / À bout de souffle", "I 400 colpi / Les Quatre Cents Coups", "Hiroshima mon amour"],
        "q3": "3. Chi è il leggendario attore italiano accanto ad Anita Ekberg nella fontana di Trevi?",
        "q3_opts": ["Alain Delon", "Jean-Paul Belmondo", "Marcello Mastroianni"],
        "quiz_success": "🌟 100% Corretto! Hai sbloccato l'invito ufficiale...",
        "quiz_fail": "💡 Quasi! Ripassa un po' di cinema classico e riprova.",
        "step3": "🎁 Ricompensa Segreta Sbloccata!",
        "invitation_title": "Sorpresa! 🎬❤️",
        "invitation_text": "Visto che hai riflessi eroici e un ottimo gusto per il cinema classico, mi faresti l'onore di venire al cinema con me?",
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

# Main Banner Photo (La Dolce Vita Poster)
st.image("https://m.media-amazon.com/images/M/MV5BMTkxMjQ4NzU5N15BMl5BanBnXkFtZTgwMTkwODkzMTE@._V1_FMjpg_UX1000_.jpg", use_container_width=True)

st.title(t["title"])
st.write(t["subtitle"])
st.markdown("---")

# Initialize Session State
if "game_won" not in st.session_state:
    st.session_state.game_won = False
if "quiz_passed" not in st.session_state:
    st.session_state.quiz_passed = False
if "no_click_count" not in st.session_state:
    st.session_state.no_click_count = 0
if "accepted" not in st.session_state:
    st.session_state.accepted = False

# --- STEP 1: RETRO FILM NOIR FIGHTER GAME WITH TEXTURED CHARACTERS ---
st.subheader(t["step1"])

if not st.session_state.game_won:
    st.write(t["game_intro"])
    
    # Fast Pass / Bypass Button
    col_a, col_b = st.columns([3, 1])
    with col_b:
        if st.button("⏩ Skip Fight"):
            st.session_state.game_won = True
            st.rerun()

    # Embedded HTML5 Retro Noir Game
    noir_game_html = """
    <div style="text-align: center;" class="noir-card">
        <canvas id="noirCanvas" width="640" height="360" style="background: #000; cursor: pointer; border: 3px solid #d4af37; max-width: 100%; height: auto; border-radius: 8px;"></canvas>
        
        <!-- Mobile / Touch Controls -->
        <div style="margin-top: 12px; display: flex; justify-content: center; gap: 8px; flex-wrap: wrap;">
            <button id="btnLeft" style="padding: 10px 18px; font-weight: bold; background: #222; color: #fff; border: 1px solid #666; border-radius: 6px;">👈 LEFT</button>
            <button id="btnPunch" style="padding: 10px 22px; font-weight: bold; background: #d4af37; color: #000; border: 1px solid #fff; border-radius: 6px;">🥊 PUNCH / FLASH</button>
            <button id="btnDodge" style="padding: 10px 18px; font-weight: bold; background: #444; color: #fff; border: 1px solid #888; border-radius: 6px;">🛡️ DODGE</button>
            <button id="btnRight" style="padding: 10px 18px; font-weight: bold; background: #222; color: #fff; border: 1px solid #666; border-radius: 6px;">RIGHT 👉</button>
            <button id="btnMusic" style="padding: 10px 14px; font-weight: bold; background: #111; color: #d4af37; border: 1px solid #d4af37; border-radius: 6px;">🎷 MUSIC ON/OFF</button>
        </div>
    </div>

    <script>
    const canvas = document.getElementById('noirCanvas');
    const ctx = canvas.getContext('2d');

    // Game Variables
    let gameLoopId = null;
    let gameWon = false;
    let musicPlaying = false;

    // Web Audio API Synthesizer
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    let audioCtx = null;

    function initAudio() {
        if (!audioCtx) {
            audioCtx = new AudioCtx();
        }
        if (audioCtx.state === 'suspended') {
            audioCtx.resume();
        }
    }

    function playSound(type) {
        if (!audioCtx) return;
        
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.connect(gain);
        gain.connect(audioCtx.destination);

        const now = audioCtx.currentTime;

        if (type === 'punch') {
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(140, now);
            osc.frequency.exponentialRampToValueAtTime(35, now + 0.12);
            gain.gain.setValueAtTime(0.4, now);
            gain.gain.linearRampToValueAtTime(0.01, now + 0.12);
            osc.start(now);
            osc.stop(now + 0.12);
        } else if (type === 'flash') {
            osc.type = 'square';
            osc.frequency.setValueAtTime(850, now);
            osc.frequency.exponentialRampToValueAtTime(180, now + 0.2);
            gain.gain.setValueAtTime(0.3, now);
            gain.gain.linearRampToValueAtTime(0.01, now + 0.2);
            osc.start(now);
            osc.stop(now + 0.2);
        } else if (type === 'hit') {
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(90, now);
            osc.frequency.linearRampToValueAtTime(25, now + 0.15);
            gain.gain.setValueAtTime(0.5, now);
            gain.gain.linearRampToValueAtTime(0.01, now + 0.15);
            osc.start(now);
            osc.stop(now + 0.15);
        } else if (type === 'victory') {
            [261.63, 329.63, 392.00, 523.25].forEach((freq, idx) => {
                const o = audioCtx.createOscillator();
                const g = audioCtx.createGain();
                o.connect(g);
                g.connect(audioCtx.destination);
                o.type = 'sine';
                o.frequency.setValueAtTime(freq, now + idx * 0.12);
                g.gain.setValueAtTime(0.3, now + idx * 0.12);
                g.gain.linearRampToValueAtTime(0.01, now + idx * 0.12 + 0.3);
                o.start(now + idx * 0.12);
                o.stop(now + idx * 0.12 + 0.3);
            });
        }
    }

    // Noir Jazz Synth Loop
    let synthTimer = null;
    function toggleMusic() {
        initAudio();
        musicPlaying = !musicPlaying;
        if (musicPlaying) {
            let noteIndex = 0;
            const notes = [110, 123.47, 130.81, 146.83, 164.81, 146.83, 130.81, 116.54];
            synthTimer = setInterval(() => {
                if (!musicPlaying) return;
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.type = 'sine';
                osc.frequency.setValueAtTime(notes[noteIndex % notes.length], audioCtx.currentTime);
                gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.4);
                osc.start();
                osc.stop(audioCtx.currentTime + 0.4);
                noteIndex++;
            }, 450);
        } else {
            if (synthTimer) clearInterval(synthTimer);
        }
    }

    // Entities
    const player = {
        x: 100,
        y: 200,
        width: 50,
        height: 110,
        vx: 0,
        speed: 4.5,
        hp: 100,
        maxHp: 100,
        isAttacking: false,
        isDodging: false,
        attackFrame: 0,
        dodgeCooldown: 0,
        combo: 0,
        walkCycle: 0
    };

    const villain = {
        x: 480,
        y: 195,
        width: 60,
        height: 115,
        hp: 100,
        maxHp: 100,
        state: 'idle', // idle, windup, attack, hit
        timer: 0,
        attackCooldown: 0
    };

    // Environmental Effects & Rain Particles
    const rain = [];
    for (let i = 0; i < 65; i++) {
        rain.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            speed: Math.random() * 8 + 10,
            len: Math.random() * 12 + 8
        });
    }

    const smokeParticles = [];
    const hitParticles = [];
    let flashOpacity = 0;
    let filmFrame = 0;

    // Controls Handling
    const keys = { left: false, right: false, attack: false, dodge: false };

    window.addEventListener('keydown', (e) => {
        initAudio();
        if (e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') keys.left = true;
        if (e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') keys.right = true;
        if (e.key === ' ' || e.key === 'Enter') triggerAttack();
        if (e.key === 'ArrowDown' || e.key === 's' || e.key === 'S') triggerDodge();
    });

    window.addEventListener('keyup', (e) => {
        if (e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') keys.left = false;
        if (e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') keys.right = false;
    });

    // Touch Controls
    document.getElementById('btnLeft').addEventListener('touchstart', (e) => { e.preventDefault(); keys.left = true; });
    document.getElementById('btnLeft').addEventListener('touchend', (e) => { e.preventDefault(); keys.left = false; });
    document.getElementById('btnRight').addEventListener('touchstart', (e) => { e.preventDefault(); keys.right = true; });
    document.getElementById('btnRight').addEventListener('touchend', (e) => { e.preventDefault(); keys.right = false; });
    
    document.getElementById('btnLeft').addEventListener('mousedown', () => keys.left = true);
    document.getElementById('btnLeft').addEventListener('mouseup', () => keys.left = false);
    document.getElementById('btnRight').addEventListener('mousedown', () => keys.right = true);
    document.getElementById('btnRight').addEventListener('mouseup', () => keys.right = false);

    document.getElementById('btnPunch').addEventListener('click', () => { initAudio(); triggerAttack(); });
    document.getElementById('btnDodge').addEventListener('click', () => { initAudio(); triggerDodge(); });
    document.getElementById('btnMusic').addEventListener('click', toggleMusic);
    canvas.addEventListener('click', () => { initAudio(); triggerAttack(); });

    function triggerAttack() {
        if (player.isAttacking || player.isDodging || gameWon) return;
        player.isAttacking = true;
        player.attackFrame = 12;
        flashOpacity = 0.55;
        playSound('flash');

        // Check Hit on Villain
        const dist = Math.abs((player.x + player.width/2) - (villain.x + villain.width/2));
        if (dist < 115) {
            villain.hp = Math.max(0, villain.hp - 12);
            villain.state = 'hit';
            villain.timer = 12;
            player.combo++;
            playSound('punch');

            // Hit Particles
            for (let i = 0; i < 10; i++) {
                hitParticles.push({
                    x: villain.x + 20,
                    y: villain.y + 35,
                    vx: (Math.random() - 0.5) * 9,
                    vy: (Math.random() - 0.5) * 9,
                    life: 15,
                    color: i % 2 === 0 ? '#ffffff' : '#d4af37'
                });
            }

            if (villain.hp <= 0 && !gameWon) {
                gameWon = true;
                playSound('victory');
                setTimeout(() => {
                    window.parent.postMessage({ type: 'VICTORY' }, '*');
                }, 1000);
            }
        } else {
            player.combo = 0;
        }
    }

    function triggerDodge() {
        if (player.isDodging || player.dodgeCooldown > 0 || gameWon) return;
        player.isDodging = true;
        player.dodgeCooldown = 38;
        setTimeout(() => { player.isDodging = false; }, 320);
    }

    // DRAW TEXTURED DETECTIVE CHARACTER
    function drawDetective(x, y, p) {
        ctx.save();
        ctx.translate(x, y);

        // Motion trail when dodging
        if (p.isDodging) {
            ctx.globalAlpha = 0.35;
            ctx.fillStyle = '#666';
            ctx.fillRect(-15, 0, p.width, p.height);
        }

        const sway = Math.sin(p.walkCycle) * 4;

        // Shadow under feet
        ctx.fillStyle = 'rgba(0, 0, 0, 0.6)';
        ctx.beginPath();
        ctx.ellipse(25, 108, 22, 6, 0, 0, Math.PI * 2);
        ctx.fill();

        // 1. Leather Shoes & Trousers
        ctx.fillStyle = '#111116';
        ctx.fillRect(12 + (p.vx < 0 ? sway : -sway), 85, 10, 22); // Left leg
        ctx.fillRect(28 + (p.vx > 0 ? sway : -sway), 85, 10, 22); // Right leg
        ctx.fillStyle = '#2b2b36'; // Shoe highlight
        ctx.fillRect(10 + (p.vx < 0 ? sway : -sway), 103, 13, 5);
        ctx.fillRect(26 + (p.vx > 0 ? sway : -sway), 103, 13, 5);

        // 2. Textured Trench Coat Body
        const coatGrad = ctx.createLinearGradient(0, 25, 45, 90);
        coatGrad.addColorStop(0, '#e2dfd5'); // Highlight tan
        coatGrad.addColorStop(0.5, '#b0ab99'); // Base coat
        coatGrad.addColorStop(1, '#615d50'); // Shadowed hem
        ctx.fillStyle = coatGrad;
        ctx.beginPath();
        ctx.moveTo(8, 28);
        ctx.lineTo(42, 28);
        ctx.lineTo(48 + sway * 0.5, 88); // Coat tail sway
        ctx.lineTo(2, 88);
        ctx.closePath();
        ctx.fill();

        // Coat lapels & folds shadow lines
        ctx.strokeStyle = '#444137';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(18, 28); ctx.lineTo(22, 52); // Lapel left
        ctx.moveTo(32, 28); ctx.lineTo(28, 52); // Lapel right
        ctx.moveTo(25, 52); ctx.lineTo(25, 88); // Center seam
        ctx.moveTo(10, 65); ctx.lineTo(20, 75); // Fold left
        ctx.moveTo(40, 65); ctx.lineTo(30, 75); // Fold right
        ctx.stroke();

        // Belt & Buckle
        ctx.fillStyle = '#222';
        ctx.fillRect(10, 52, 30, 5);
        ctx.fillStyle = '#ffd700'; // Gold buckle
        ctx.fillRect(22, 51, 6, 7);

        // Buttons
        ctx.fillStyle = '#333';
        ctx.beginPath();
        ctx.arc(19, 38, 2, 0, Math.PI * 2);
        ctx.arc(19, 46, 2, 0, Math.PI * 2);
        ctx.arc(31, 38, 2, 0, Math.PI * 2);
        ctx.arc(31, 46, 2, 0, Math.PI * 2);
        ctx.fill();

        // Collar & Tie
        ctx.fillStyle = '#ffffff'; // White shirt
        ctx.beginPath();
        ctx.moveTo(21, 20); ctx.lineTo(25, 28); ctx.lineTo(29, 20);
        ctx.fill();
        ctx.fillStyle = '#900000'; // Dark Red Tie
        ctx.beginPath();
        ctx.moveTo(24, 22); ctx.lineTo(26, 22); ctx.lineTo(27, 34); ctx.lineTo(25, 37); ctx.lineTo(23, 34);
        ctx.fill();

        // Head & Stubble Profile
        ctx.fillStyle = '#dcb18a'; // Skin tone
        ctx.fillRect(18, 12, 14, 15);
        ctx.fillStyle = 'rgba(60, 50, 40, 0.4)'; // Stubble / Shadow
        ctx.fillRect(24, 20, 8, 7);

        // Fedora Hat
        const hatGrad = ctx.createLinearGradient(10, 0, 40, 15);
        hatGrad.addColorStop(0, '#3a3830');
        hatGrad.addColorStop(1, '#1a1915');
        ctx.fillStyle = hatGrad;
        // Brim
        ctx.beginPath();
        ctx.ellipse(25, 12, 22, 5, -0.08, 0, Math.PI * 2);
        ctx.fill();
        // Crown
        ctx.fillRect(15, 0, 20, 12);
        // Ribbon Band
        ctx.fillStyle = '#111111';
        ctx.fillRect(15, 9, 20, 3);

        // Camera / Punch Arm Overlay
        if (p.isAttacking) {
            ctx.fillStyle = '#b0ab99';
            ctx.fillRect(32, 30, 28, 10); // Arm extended
            // Vintage Camera
            ctx.fillStyle = '#111';
            ctx.fillRect(55, 22, 18, 18);
            ctx.fillStyle = '#d4af37'; // Flash bulb
            ctx.beginPath();
            ctx.arc(73, 31, 11, 0, Math.PI * 2);
            ctx.fill();
        }

        ctx.restore();
    }

    // DRAW TEXTURED NOIR VILLAIN (THE SHADOW CRITIC)
    function drawVillain(x, y, v) {
        ctx.save();
        ctx.translate(x, y);

        // Hit Flash Outline
        if (v.state === 'hit') {
            ctx.shadowColor = '#ffffff';
            ctx.shadowBlur = 15;
        }

        // Shadow under feet
        ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        ctx.beginPath();
        ctx.ellipse(30, 112, 26, 7, 0, 0, Math.PI * 2);
        ctx.fill();

        // 1. Double Breasted Pinstripe Suit Body
        ctx.fillStyle = '#181820'; // Midnight charcoal
        ctx.fillRect(5, 22, 50, 68);

        // Procedural Pinstripes Texture
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
        ctx.lineWidth = 1;
        for (let p = 9; p <= 51; p += 6) {
            ctx.beginPath();
            ctx.moveTo(p, 22);
            ctx.lineTo(p, 90);
            ctx.stroke();
        }

        // Trousers
        ctx.fillStyle = '#121218';
        ctx.fillRect(12, 90, 14, 22);
        ctx.fillRect(34, 90, 14, 22);

        // Suit Lapels & Silk Pocket Square
        ctx.fillStyle = '#0d0d12'; // Satin lapel shadow
        ctx.beginPath();
        ctx.moveTo(12, 22); ctx.lineTo(25, 50); ctx.lineTo(5, 50); ctx.closePath(); ctx.fill();
        ctx.beginPath();
        ctx.moveTo(48, 22); ctx.lineTo(35, 50); ctx.lineTo(55, 50); ctx.closePath(); ctx.fill();

        // Silk Red Pocket Square
        ctx.fillStyle = '#b30000';
        ctx.beginPath();
        ctx.moveTo(42, 36); ctx.lineTo(46, 30); ctx.lineTo(50, 36); ctx.closePath(); ctx.fill();

        // Double Row Gold Suit Buttons
        ctx.fillStyle = '#d4af37';
        ctx.beginPath();
        ctx.arc(22, 45, 2.2, 0, Math.PI * 2);
        ctx.arc(22, 58, 2.2, 0, Math.PI * 2);
        ctx.arc(38, 45, 2.2, 0, Math.PI * 2);
        ctx.arc(38, 58, 2.2, 0, Math.PI * 2);
        ctx.fill();

        // Collar & Silk Tie
        ctx.fillStyle = '#e6e6e6'; // Crisp collar
        ctx.beginPath();
        ctx.moveTo(25, 22); ctx.lineTo(30, 30); ctx.lineTo(35, 22); ctx.fill();
        ctx.fillStyle = '#d4af37'; // Gold tie
        ctx.fillRect(28, 26, 4, 18);

        // Dramatic Flowing Noir Cape / Coat
        ctx.fillStyle = '#08080c';
        ctx.beginPath();
        ctx.moveTo(5, 25);
        ctx.quadraticCurveTo(-20, 60, -12, 98);
        ctx.lineTo(10, 90);
        ctx.closePath();
        ctx.fill();

        // Head & Fedora
        ctx.fillStyle = '#101015'; // Shadowed head
        ctx.fillRect(18, 5, 24, 18);

        // Fedora tilted down
        ctx.fillStyle = '#22222d';
        ctx.beginPath();
        ctx.ellipse(30, 8, 28, 6, 0.1, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillRect(18, -5, 24, 12);
        ctx.fillStyle = '#b30000'; // Red hatband
        ctx.fillRect(18, 4, 24, 3);

        // Intense Glowing Red Eyes underneath shadow
        ctx.fillStyle = v.state === 'windup' ? '#ff0000' : '#ff3333';
        ctx.shadowColor = '#ff0000';
        ctx.shadowBlur = 10;
        ctx.fillRect(22, 13, 6, 3);
        ctx.fillRect(32, 13, 6, 3);
        ctx.shadowBlur = 0; // Reset shadow

        // Evil Grin on Attack state
        if (v.state === 'attack' || v.state === 'windup') {
            ctx.strokeStyle = '#ffffff';
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.arc(30, 20, 6, 0.1, Math.PI - 0.1);
            ctx.stroke();
            // Attack fist extension
            ctx.fillStyle = '#181820';
            ctx.fillRect(-22, 38, 30, 12);
        }

        ctx.restore();
    }

    // Game Loop Update
    function update() {
        if (gameWon) return;

        filmFrame++;

        // Player Movement & Walk Animation
        if (keys.left) {
            player.x = Math.max(20, player.x - player.speed);
            player.vx = -1;
            player.walkCycle += 0.2;
        } else if (keys.right) {
            player.x = Math.min(canvas.width - 120, player.x + player.speed);
            player.vx = 1;
            player.walkCycle += 0.2;
        } else {
            player.vx = 0;
        }

        if (player.attackFrame > 0) player.attackFrame--;
        else player.isAttacking = false;

        if (player.dodgeCooldown > 0) player.dodgeCooldown--;

        // Villain AI Logic
        villain.attackCooldown++;
        if (villain.state === 'idle' && villain.attackCooldown > 55) {
            villain.state = 'windup';
            villain.timer = 22;
            villain.attackCooldown = 0;
        } else if (villain.state === 'windup') {
            villain.timer--;
            if (villain.timer <= 0) {
                villain.state = 'attack';
                villain.timer = 15;
                
                // Attack Player
                const dist = Math.abs((player.x + player.width/2) - (villain.x + villain.width/2));
                if (dist < 95 && !player.isDodging) {
                    player.hp = Math.max(0, player.hp - 15);
                    playSound('hit');
                    player.combo = 0;
                }
            }
        } else if (villain.state === 'attack') {
            villain.timer--;
            if (villain.timer <= 0) villain.state = 'idle';
        } else if (villain.state === 'hit') {
            villain.timer--;
            if (villain.timer <= 0) villain.state = 'idle';
        }

        // Villain Movement towards player
        if (villain.state === 'idle') {
            if (villain.x > player.x + 85) villain.x -= 1.3;
            else if (villain.x < player.x + 65) villain.x += 1.3;
        }

        // Smoke / Steam Breath Particles from Villain
        if (filmFrame % 10 === 0) {
            smokeParticles.push({
                x: villain.x + 15,
                y: villain.y + 15,
                vx: -Math.random() * 1.5 - 0.5,
                vy: -Math.random() * 0.8 - 0.2,
                size: Math.random() * 4 + 2,
                alpha: 0.4
            });
        }

        for (let i = smokeParticles.length - 1; i >= 0; i--) {
            smokeParticles[i].x += smokeParticles[i].vx;
            smokeParticles[i].y += smokeParticles[i].vy;
            smokeParticles[i].alpha -= 0.01;
            if (smokeParticles[i].alpha <= 0) smokeParticles.splice(i, 1);
        }

        // Update Hit Particles
        for (let i = hitParticles.length - 1; i >= 0; i--) {
            hitParticles[i].x += hitParticles[i].vx;
            hitParticles[i].y += hitParticles[i].vy;
            hitParticles[i].life--;
            if (hitParticles[i].life <= 0) hitParticles.splice(i, 1);
        }

        // Rain
        rain.forEach(r => {
            r.y += r.speed;
            if (r.y > canvas.height) {
                r.y = -10;
                r.x = Math.random() * canvas.width;
            }
        });

        if (flashOpacity > 0) flashOpacity -= 0.05;
    }

    // Render Loop
    function render() {
        // High Contrast Noir Background
        ctx.fillStyle = '#08080a';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Cobblestone Street
        ctx.fillStyle = '#121318';
        ctx.fillRect(0, 305, canvas.width, 55);
        ctx.strokeStyle = '#22232a';
        ctx.lineWidth = 1;
        for (let c = 0; c < canvas.width; c += 25) {
            ctx.beginPath(); ctx.moveTo(c, 305); ctx.lineTo(c - 10, 360); ctx.stroke();
        }

        // Streetlamp Spotlight Effect
        const spotGrad = ctx.createRadialGradient(500, 70, 10, 500, 240, 200);
        spotGrad.addColorStop(0, 'rgba(255, 245, 205, 0.38)');
        spotGrad.addColorStop(1, 'rgba(0, 0, 0, 0)');
        ctx.fillStyle = spotGrad;
        ctx.beginPath();
        ctx.arc(500, 200, 200, 0, Math.PI * 2);
        ctx.fill();

        // Render Rain
        ctx.strokeStyle = 'rgba(200, 220, 255, 0.22)';
        ctx.lineWidth = 1;
        rain.forEach(r => {
            ctx.beginPath();
            ctx.moveTo(r.x, r.y);
            ctx.lineTo(r.x - 2, r.y + r.len);
            ctx.stroke();
        });

        // Render Smoke Particles
        smokeParticles.forEach(s => {
            ctx.fillStyle = `rgba(200, 200, 200, ${s.alpha})`;
            ctx.beginPath();
            ctx.arc(s.x, s.y, s.size, 0, Math.PI * 2);
            ctx.fill();
        });

        // Render Characters with Textures
        drawDetective(player.x, player.y, player);
        drawVillain(villain.x, villain.y, villain);

        // Render Hit Impact Particles
        hitParticles.forEach(p => {
            ctx.fillStyle = p.color;
            ctx.fillRect(p.x, p.y, 4, 4);
        });

        // Photo Flash Screen Overlay
        if (flashOpacity > 0) {
            ctx.fillStyle = `rgba(255, 255, 255, ${flashOpacity})`;
            ctx.fillRect(0, 0, canvas.width, canvas.height);
        }

        // Film Grain & Scratches
        ctx.fillStyle = 'rgba(255, 255, 255, 0.03)';
        for (let i = 0; i < 28; i++) {
            let gx = (Math.sin(filmFrame * i) * 9999) % canvas.width;
            let gy = (Math.cos(filmFrame * i) * 9999) % canvas.height;
            ctx.fillRect(gx, gy, 2, 2);
        }

        // HUD - Health Bars
        ctx.fillStyle = '#111';
        ctx.fillRect(20, 20, 180, 16);
        ctx.fillStyle = '#d4af37';
        ctx.fillRect(20, 20, (player.hp / player.maxHp) * 180, 16);
        ctx.strokeStyle = '#fff';
        ctx.strokeRect(20, 20, 180, 16);
        ctx.fillStyle = '#fff';
        ctx.font = '12px monospace';
        ctx.fillText('DETECTIVE HP', 25, 33);

        ctx.fillStyle = '#111';
        ctx.fillRect(440, 20, 180, 16);
        ctx.fillStyle = '#ff4b4b';
        ctx.fillRect(440, 20, (villain.hp / villain.maxHp) * 180, 16);
        ctx.strokeStyle = '#fff';
        ctx.strokeRect(440, 20, 180, 16);
        ctx.fillText('SHADOW CRITIC', 445, 33);

        if (player.combo > 1) {
            ctx.fillStyle = '#ffd700';
            ctx.font = 'bold 16px monospace';
            ctx.fillText(`${player.combo}x COMBO!`, 20, 60);
        }

        // Victory Screen
        if (gameWon) {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.88)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.fillStyle = '#d4af37';
            ctx.font = 'bold 26px serif';
            ctx.textAlign = 'center';
            ctx.fillText('VICTORY - SECRET UNLOCKED!', canvas.width / 2, 160);

            ctx.fillStyle = '#ffffff';
            ctx.font = '16px monospace';
            ctx.fillText('The Shadow Critic has been silenced.', canvas.width / 2, 200);
            ctx.fillText('Click below to claim your reward!', canvas.width / 2, 230);
        }
    }

    function gameLoop() {
        update();
        render();
        gameLoopId = requestAnimationFrame(gameLoop);
    }

    gameLoop();
    </script>
    """
    
    st.components.v1.html(noir_game_html, height=480)

    # Secondary Manual Victory Trigger
    if st.button("🏆 I Won the Noir Fight! (Unlock Step 2)"):
        st.session_state.game_won = True
        st.rerun()

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
    st.info("🔒 Defeat The Shadow Critic in Phase 1 to unlock the quiz!")

st.markdown("---")

# --- STEP 3: THE SECRET REWARD (DATE INVITATION) ---
if st.session_state.quiz_passed:
    st.subheader(t["step3"])
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
        
        # Les Quatre Cents Coups (1959) Still Image
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
                <p><b>{t['admit']}</b></p>
                <p>🎬 <b>Vibe/Genre:</b> {chosen_genre}</p>
                <p>🍿 <b>Snack:</b> {chosen_snack}</p>
                <p>📅 <b>Date:</b> {chosen_date} at {chosen_time}</p>
                <br>
                <p><i>{t['footer']}</i></p>
            </div>
            """, unsafe_allow_html=True)
            
            # --- SAVE RESPONSES TO GOOGLE SHEETS ---
            if GSHEETS_AVAILABLE:
                try:
                    conn = st.connection("gsheets", type=GSheetsConnection)
                    existing_data = conn.read(worksheet="Sheet1", ttl=0)
                    
                    new_row = pd.DataFrame([{
                        "Status": "Accepted",
                        "Genre": chosen_genre,
                        "Snack": chosen_snack,
                        "Date": str(chosen_date),
                        "Time": str(chosen_time)
                    }])
                    
                    updated_df = pd.concat([existing_data, new_row], ignore_index=True)
                    conn.update(worksheet="Sheet1", data=updated_df)
                except Exception:
                    pass
