import streamlit as st
import google.generativeai as genai

# ── Page config (must be first Streamlit call) ──────────────────────────────
st.set_page_config(
    page_title="ViralFlow AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&family=Share+Tech+Mono&family=Noto+Nastaliq+Urdu:wght@400;700&display=swap');

:root {
    --bg-deep:      #050510;
    --bg-card:      #0d0d1f;
    --bg-input:     #0a0a1a;
    --neon-purple:  #b14fff;
    --neon-cyan:    #00e5ff;
    --neon-pink:    #ff2d78;
    --neon-gold:    #ffd700;
    --text-primary: #e8e8ff;
    --text-muted:   #7a7a9a;
    --border:       rgba(177,79,255,0.25);
    --glow-purple:  0 0 18px rgba(177,79,255,0.55);
    --glow-cyan:    0 0 18px rgba(0,229,255,0.55);
    --glow-gold:    0 0 18px rgba(255,215,0,0.45);
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg-deep) !important;
    color: var(--text-primary) !important;
    font-family: 'Rajdhani', sans-serif !important;
}

/* Starfield */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        radial-gradient(1px 1px at 10% 20%, rgba(177,79,255,0.6) 0%, transparent 100%),
        radial-gradient(1px 1px at 80% 10%, rgba(0,229,255,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 55% 75%, rgba(177,79,255,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 25% 85%, rgba(0,229,255,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 90% 60%, rgba(255,45,120,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 40% 40%, rgba(177,79,255,0.3) 0%, transparent 100%),
        radial-gradient(1px 1px at 70% 90%, rgba(0,229,255,0.3) 0%, transparent 100%),
        radial-gradient(2px 2px at 15% 50%, rgba(177,79,255,0.5) 0%, transparent 100%),
        radial-gradient(2px 2px at 65% 30%, rgba(0,229,255,0.4) 0%, transparent 100%);
    pointer-events: none;
    z-index: 0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #07071a 0%, #0d0d25 100%) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* Hero */
.hero-header {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    position: relative;
}
.hero-title {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(1.8rem, 5vw, 4rem);
    font-weight: 900;
    letter-spacing: 0.1em;
    background: linear-gradient(90deg, var(--neon-purple), var(--neon-cyan), var(--neon-purple));
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 3s linear infinite;
    margin: 0;
    line-height: 1.1;
}
@keyframes shimmer {
    0%   { background-position: 0% center; }
    100% { background-position: 200% center; }
}
.hero-sub {
    font-family: 'Share Tech Mono', monospace;
    color: var(--neon-cyan);
    font-size: clamp(0.6rem, 1.5vw, 0.85rem);
    letter-spacing: 0.25em;
    margin-top: 0.6rem;
    opacity: 0.8;
}
.hero-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--neon-purple), var(--neon-cyan), transparent);
    margin: 1.5rem auto;
    max-width: 600px;
    box-shadow: var(--glow-purple);
}

/* Language badge strip */
.lang-strip {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(255,215,0,0.07);
    border: 1px solid rgba(255,215,0,0.3);
    border-radius: 20px;
    padding: 0.3rem 1rem;
    margin: 0.5rem auto;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.72rem;
    color: var(--neon-gold);
    letter-spacing: 0.15em;
}
.lang-dot {
    width: 7px; height: 7px;
    background: var(--neon-gold);
    border-radius: 50%;
    display: inline-block;
    box-shadow: var(--glow-gold);
    animation: pulse-gold 2s ease-in-out infinite;
}
@keyframes pulse-gold {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.5; transform: scale(0.7); }
}

/* Neon cards */
.neon-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.6rem;
    margin: 0.8rem 0;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s, box-shadow 0.3s;
}
.neon-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--neon-purple), var(--neon-cyan));
}
.neon-card:hover {
    border-color: var(--neon-purple);
    box-shadow: var(--glow-purple);
}

/* Section titles */
.section-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--neon-cyan);
    letter-spacing: 0.08em;
    margin-bottom: 0.4rem;
    text-transform: uppercase;
}
.section-icon { font-size: 1.5rem; margin-right: 0.4rem; vertical-align: middle; }
.section-desc { color: var(--text-muted); font-size: 0.93rem; margin-bottom: 1rem; line-height: 1.5; }

/* Inputs */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 8px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem !important;
    transition: border-color 0.3s, box-shadow 0.3s !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--neon-cyan) !important;
    box-shadow: var(--glow-cyan) !important;
    outline: none !important;
}
[data-testid="stTextInput"] label,
[data-testid="stTextArea"] label,
[data-testid="stSelectbox"] label {
    color: var(--text-muted) !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
}

/* Buttons */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, var(--neon-purple) 0%, #6a00cc 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Orbitron', sans-serif !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.14em !important;
    padding: 0.65rem 1.6rem !important;
    text-transform: uppercase !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 0 20px rgba(177,79,255,0.4) !important;
    cursor: pointer !important;
    width: 100%;
}
[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 0 35px rgba(177,79,255,0.75) !important;
    background: linear-gradient(135deg, #c96fff 0%, var(--neon-purple) 100%) !important;
}
[data-testid="stButton"] > button:active { transform: translateY(0px) !important; }

/* Output blocks */
.output-block {
    background: #08081c;
    border: 1px solid rgba(0,229,255,0.2);
    border-left: 3px solid var(--neon-cyan);
    border-radius: 8px;
    padding: 1.2rem 1.4rem;
    margin: 0.7rem 0;
    font-size: 1rem;
    color: var(--text-primary);
    line-height: 1.8;
    white-space: pre-wrap;
    word-break: break-word;
}
/* Urdu script output — Noto Nastaliq for beautiful rendering */
.output-block.urdu-script {
    font-family: 'Noto Nastaliq Urdu', serif !important;
    font-size: 1.15rem !important;
    direction: rtl;
    text-align: right;
    line-height: 2.2 !important;
}
.output-block .hook-number {
    font-family: 'Orbitron', sans-serif;
    color: var(--neon-purple);
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    display: block;
    margin-bottom: 0.4rem;
    opacity: 0.8;
    direction: ltr;
    text-align: left;
}

/* Tag pills */
.tag-pill {
    display: inline-block;
    background: rgba(177,79,255,0.12);
    border: 1px solid rgba(177,79,255,0.35);
    color: var(--neon-purple);
    border-radius: 20px;
    padding: 0.22rem 0.8rem;
    margin: 0.22rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.76rem;
    letter-spacing: 0.04em;
    transition: all 0.2s;
}
.tag-pill:hover { background: rgba(177,79,255,0.25); box-shadow: var(--glow-purple); }

/* Badges */
.badge-purple {
    display: inline-block;
    background: rgba(177,79,255,0.15);
    border: 1px solid var(--neon-purple);
    color: var(--neon-purple);
    border-radius: 4px;
    padding: 0.14rem 0.65rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
}
.badge-cyan {
    display: inline-block;
    background: rgba(0,229,255,0.1);
    border: 1px solid var(--neon-cyan);
    color: var(--neon-cyan);
    border-radius: 4px;
    padding: 0.14rem 0.65rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
}
.badge-gold {
    display: inline-block;
    background: rgba(255,215,0,0.1);
    border: 1px solid var(--neon-gold);
    color: var(--neon-gold);
    border-radius: 4px;
    padding: 0.14rem 0.65rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
}

/* Metrics */
.metrics-row { display: flex; gap: 0.8rem; flex-wrap: wrap; margin: 1rem 0; }
.metric-box {
    flex: 1;
    min-width: 100px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.9rem;
    text-align: center;
}
.metric-val {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    background: linear-gradient(90deg, var(--neon-purple), var(--neon-cyan));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.metric-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    color: var(--text-muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 0.2rem;
}

/* Copy area */
.copy-area {
    background: #06060f;
    border: 1px dashed rgba(0,229,255,0.3);
    border-radius: 8px;
    padding: 1rem 1.2rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.82rem;
    color: #a0ffd0;
    white-space: pre-wrap;
    line-height: 1.65;
    overflow-x: auto;
    word-break: break-word;
}
.copy-area.urdu-script {
    font-family: 'Noto Nastaliq Urdu', serif !important;
    font-size: 1.05rem !important;
    direction: rtl;
    text-align: right;
    line-height: 2.1 !important;
    color: #e8e8ff !important;
}

hr { border: none; height: 1px; background: linear-gradient(90deg, transparent, var(--border), transparent); margin: 1.3rem 0; }

[data-testid="column"] { padding: 0 0.4rem !important; }

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb { background: var(--neon-purple); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--neon-cyan); }

[data-testid="stRadio"] label { color: var(--text-primary) !important; font-family: 'Rajdhani', sans-serif !important; }
[data-testid="stSlider"] label { color: var(--text-muted) !important; font-family: 'Share Tech Mono', monospace !important; font-size: 0.75rem !important; }
[data-testid="stExpander"] { border: 1px solid var(--border) !important; border-radius: 8px !important; background: var(--bg-card) !important; }
[data-testid="stExpander"] summary { color: var(--neon-cyan) !important; font-family: 'Rajdhani', sans-serif !important; font-weight: 600 !important; }

/* Mobile tweaks */
@media (max-width: 768px) {
    .hero-title { font-size: 1.7rem !important; letter-spacing: 0.06em !important; }
    .hero-sub   { font-size: 0.6rem !important; letter-spacing: 0.15em !important; }
    .metrics-row { gap: 0.5rem; }
    .metric-box  { min-width: 80px; padding: 0.7rem 0.4rem; }
    .metric-val  { font-size: 1.3rem; }
    .neon-card   { padding: 1.1rem; }
}
</style>
""", unsafe_allow_html=True)


# ── Language config ──────────────────────────────────────────────────────────
LANG_CONFIG = {
    "English": {
        "code": "en",
        "flag": "🇬🇧",
        "label": "ENGLISH",
        "font_class": "",
        "instruction": (
            "Write all output in clear, high-energy English suited for viral short-form content."
        ),
        "hook_flavour": (
            "Use powerful English words, action verbs, and punchy sentences."
        ),
        "seo_note": (
            "All titles, descriptions, and hashtag captions should be in English."
        ),
    },
    "Roman Urdu": {
        "code": "roman_urdu",
        "flag": "🇵🇰",
        "label": "ROMAN URDU",
        "font_class": "",
        "instruction": (
            "Write all output in ROMAN URDU — the trendy conversational style used by Pakistani "
            "and Indian creators on TikTok, Instagram Reels, and YouTube Shorts. "
            "This means Urdu/Hindi words written in English alphabet (NOT Urdu script). "
            "Use high-energy street language common on Pakistani social media. "
            "Freely mix in power words like: Doston, Zabardast, Kamaal, Yaar, Bhai, "
            "Sun lo, Sach bolunga, Bilkul sach, Kya scene hai, Bata do, Suno zara, "
            "Ekdum fire, Viral ho gaya, Game changer, Puri duniya dekh rahi hai, "
            "Ye cheez, Bas karo, Mast cheez, Itna important, Seedha baat. "
            "Keep the energy HIGH and the language punchy — like a charismatic Pakistani creator "
            "talking directly to the camera."
        ),
        "hook_flavour": (
            "Start with phrases like 'Doston,', 'Yaar sun lo,', 'Bhai ek second ruko', "
            "'Sach bolunga,', 'Aaj ki baat zabardast hai —'. Mix Urdu and English words naturally."
        ),
        "seo_note": (
            "Titles and descriptions should be in Roman Urdu mixed with English (Hinglish style). "
            "Hashtags must remain in English/Roman characters (no Urdu script in hashtags)."
        ),
    },
    "Pure Urdu": {
        "code": "urdu",
        "flag": "🇵🇰",
        "label": "خالص اردو",
        "font_class": "urdu-script",
        "instruction": (
            "Write ALL output in PURE URDU SCRIPT (not Roman Urdu, not English). "
            "Use grammatically correct, professionally written Urdu that is also energetic "
            "and engaging for social media content. The script should flow naturally in Urdu "
            "and feel native, not translated. Use proper Urdu grammar and vocabulary. "
            "Ensure every sentence is in authentic Urdu script (نستعلیق)."
        ),
        "hook_flavour": (
            "Use classic Urdu rhetorical devices — address the audience with 'دوستو،' or 'یارو،', "
            "build curiosity with Urdu idioms, and keep sentences short and punchy."
        ),
        "seo_note": (
            "Titles and descriptions should be in Urdu script. "
            "For hashtags — write the Urdu concept but also provide English/Roman transliteration "
            "in brackets for platform compatibility, e.g.  #وائرل (#Viral)."
        ),
    },
}


# ── Gemini helper ────────────────────────────────────────────────────────────
def get_gemini_response(api_key: str, prompt: str) -> str:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        resp = model.generate_content(prompt)
        return resp.text
    except Exception as e:
        return f"⚠️ API Error: {e}"


# ── Prompt builders ──────────────────────────────────────────────────────────
def hook_prompt(topic: str, platform: str, style: str, lang_cfg: dict) -> str:
    return f"""You are a viral content strategist specialized in short-form video psychology.

LANGUAGE REQUIREMENT (CRITICAL — follow exactly):
{lang_cfg['instruction']}
{lang_cfg['hook_flavour']}

Create EXACTLY 5 powerful video hooks for the topic: "{topic}"
Platform: {platform} | Style: {style}

Each hook must use a DIFFERENT psychological trigger:
1. Curiosity Gap  2. Shock/Surprise  3. Controversy  4. FOMO  5. Relatability

Format EXACTLY like this (keep the section labels in English for parsing, but the hook TEXT in the required language):

HOOK 1 | [PSYCHOLOGICAL TRIGGER NAME]
[Hook text in the required language — max 2 sentences]

HOOK 2 | [PSYCHOLOGICAL TRIGGER NAME]
[Hook text]

HOOK 3 | [PSYCHOLOGICAL TRIGGER NAME]
[Hook text]

HOOK 4 | [PSYCHOLOGICAL TRIGGER NAME]
[Hook text]

HOOK 5 | [PSYCHOLOGICAL TRIGGER NAME]
[Hook text]

Rules:
- Hook text must strictly follow the language instruction above
- Grab attention in the FIRST 3 seconds
- Use strong action verbs and power words (in the target language)
- Be specific, not vague
- No hashtags inside hook text"""


def script_prompt(topic: str, hook: str, platform: str, duration: int, lang_cfg: dict) -> str:
    return f"""You are a viral short-form video scriptwriter who has written content with 100M+ views.

LANGUAGE REQUIREMENT (CRITICAL — follow exactly):
{lang_cfg['instruction']}

Write a {duration}-second retention-optimized script for:
Topic: "{topic}"
Opening Hook: "{hook}"
Platform: {platform}

IMPORTANT: All SPOKEN dialogue and narration must be in the required language.
Keep structural markers (like [VISUAL CUE], [SOUND CUE], etc.) in English — these are production notes.

SCRIPT STRUCTURE:

[HOOK - 0-3s]
{{opening hook — spoken in required language}}

[VISUAL CUE]: {{Describe what's on screen — can be in English or the target language}}
[SOUND CUE]: {{Background music/sound effect suggestion}}

[BODY - 3-{duration - 10}s]
{{Script in punchy sentences. EACH sentence on its own line. All in required language.}}

[VISUAL CUE]: {{Relevant B-roll, graphic, or on-screen text}}
[TRANSITION]: {{Cut type}}

{{Continue body content in required language...}}

[VISUAL CUE]: {{Another visual direction}}

[CTA - {duration - 10}s-{duration}s]
{{Strong call to action in required language}}

[VISUAL CUE]: {{Final frame description}}
[TEXT OVERLAY]: {{On-screen text — in required language}}

Rules:
- Spoken content strictly in the required language
- At least 4 [VISUAL CUE] markers
- At least 2 [SOUND CUE] or [MUSIC] markers
- At least 1 [TEXT OVERLAY]
- Every 5-7 seconds = new scene
- Strong specific CTA at the end"""


def thumbnail_prompt(topic: str, platform: str, style: str, lang_cfg: dict) -> str:
    # Thumbnail image prompts always in English for best AI image generation
    # but the context description respects language
    lang_note = ""
    if lang_cfg["code"] != "en":
        lang_note = (
            f"\nNote: The creator's audience is {lang_cfg['label']} speaking. "
            "If including text overlays in the thumbnail concept, suggest both an "
            f"English version AND a {lang_cfg['label']} version of the text."
        )

    return f"""You are a professional thumbnail designer and AI image prompt engineer.
Topic: "{topic}" for {platform}.
Thumbnail style: {style}
{lang_note}

Generate 3 HIGHLY DETAILED image generation prompts for viral thumbnails.
Each prompt must be in ENGLISH (for best AI image generation results).

Format EXACTLY like this:

PROMPT 1 | [STYLE TAG]
[Detailed English prompt — subject, expression, colors, lighting, composition, quality modifiers]
TEXT OVERLAY SUGGESTION (English): [text]
{"TEXT OVERLAY SUGGESTION (" + lang_cfg["label"] + "): [equivalent text in " + lang_cfg["label"] + "]" if lang_cfg["code"] != "en" else ""}

PROMPT 2 | [STYLE TAG
