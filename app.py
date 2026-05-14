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

PROMPT 2 | [STYLE TAG]
[Detailed English prompt]
TEXT OVERLAY SUGGESTION (English): [text]
{"TEXT OVERLAY SUGGESTION (" + lang_cfg["label"] + "): [equivalent text]" if lang_cfg["code"] != "en" else ""}

PROMPT 3 | [STYLE TAG]
[Detailed English prompt]
TEXT OVERLAY SUGGESTION (English): [text]
{"TEXT OVERLAY SUGGESTION (" + lang_cfg["label"] + "): [equivalent text]" if lang_cfg["code"] != "en" else ""}

NEGATIVE PROMPTS (use for all three):
[List exclusions for clean thumbnails]

Each prompt must include:
- Specific facial expression (shock, excitement, curiosity)
- Exact color palette
- Lighting style
- Composition rule
- Quality tags (8K, hyperrealistic, professional photography)
- Platform-specific dimensions hint"""


def seo_prompt(topic: str, platform: str, niche: str, lang_cfg: dict) -> str:
    return f"""You are a viral SEO expert for short-form content platforms.

LANGUAGE REQUIREMENT (CRITICAL):
{lang_cfg['instruction']}
{lang_cfg['seo_note']}

Generate complete SEO package for:
Topic: "{topic}"
Platform: {platform}
Niche: {niche}
Output Language: {lang_cfg['label']}

Provide EXACTLY this structure (keep section header labels in English for parsing; content in required language):

VIDEO TITLE OPTIONS:
Title 1: [SEO-optimized title in required language, 60 chars max]
Title 2: [Alternative with different angle]
Title 3: [Question-based title]

OPTIMIZED DESCRIPTION:
[150-200 word description in required language with natural keyword integration and call to action]

HASHTAG STRATEGY:

MEGA TAGS (100M+ posts - use 3):
#tag1 #tag2 #tag3

VIRAL TAGS (10M-100M posts - use 5):
#tag1 #tag2 #tag3 #tag4 #tag5

NICHE TAGS (1M-10M posts - use 8):
#tag1 #tag2 #tag3 #tag4 #tag5 #tag6 #tag7 #tag8

MICRO TAGS (under 1M - use 4):
#tag1 #tag2 #tag3 #tag4

KEYWORD DENSITY TARGETS:
Primary keyword: [word] — use 3-5x
Secondary keywords: [word1], [word2], [word3]

BEST POSTING TIMES for {platform}:
[Day]: [Time range] — [reason in required language]
[Day]: [Time range] — [reason]
[Day]: [Time range] — [reason]

ENGAGEMENT BAIT LINE:
[One sentence in required language that drives comments]"""


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:1rem 0 0.5rem;'>
        <div style='font-family:Orbitron,sans-serif; font-size:1.35rem; font-weight:900;
                    background:linear-gradient(90deg,#b14fff,#00e5ff);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text;'>⚡ VIRALFLOW</div>
        <div style='font-family:Share Tech Mono,monospace; font-size:0.62rem;
                    color:#00e5ff; letter-spacing:0.3em; margin-top:0.2rem; opacity:0.7;'>
            CONTENT ENGINE v2.1
        </div>
    </div>
    <hr style='border:none;height:1px;
               background:linear-gradient(90deg,transparent,rgba(177,79,255,0.5),transparent);
               margin:0.6rem 0 0.9rem;'/>
    """, unsafe_allow_html=True)

    # API Key
    st.markdown("""<div style='font-family:Share Tech Mono,monospace;font-size:0.7rem;
    color:#7a7a9a;letter-spacing:0.2em;text-transform:uppercase;margin-bottom:0.3rem;'>
    🔑 Gemini API Key</div>""", unsafe_allow_html=True)
    api_key = st.text_input("gemini_api_key", type="password",
                             placeholder="AIza...", label_visibility="collapsed")
    if api_key:
        st.markdown('<span class="badge-cyan">● CONNECTED</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge-purple">○ NOT SET</span>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Platform
    st.markdown("""<div style='font-family:Share Tech Mono,monospace;font-size:0.7rem;
    color:#7a7a9a;letter-spacing:0.2em;text-transform:uppercase;margin-bottom:0.3rem;'>
    🎯 Target Platform</div>""", unsafe_allow_html=True)
    platform = st.selectbox("platform", ["TikTok", "Instagram Reels", "YouTube Shorts"],
                             label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Language Selector ────────────────────────────────────────────────────
    st.markdown("""<div style='font-family:Share Tech Mono,monospace;font-size:0.7rem;
    color:#ffd700;letter-spacing:0.2em;text-transform:uppercase;margin-bottom:0.3rem;'>
    🌐 Output Language</div>""", unsafe_allow_html=True)

    lang_options = list(LANG_CONFIG.keys())
    selected_lang = st.selectbox(
        "output_language",
        lang_options,
        format_func=lambda x: f"{LANG_CONFIG[x]['flag']}  {x}",
        label_visibility="collapsed",
        key="selected_language",
    )
    lang_cfg = LANG_CONFIG[selected_lang]

    # Language info card
    lang_info = {
        "English":    "🌍 Universal — best for global reach",
        "Roman Urdu": "🔥 Pakistani/Indian TikTok slang style",
        "Pure Urdu":  "✍️ Professional Urdu script (نستعلیق)",
    }
    st.markdown(f"""
    <div style='background:rgba(255,215,0,0.06);border:1px solid rgba(255,215,0,0.2);
                border-radius:8px;padding:0.6rem 0.8rem;margin-top:0.4rem;'>
        <div style='font-family:Rajdhani,sans-serif;font-size:0.85rem;color:#ffd700;'>
            {lang_info[selected_lang]}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Navigation
    st.markdown("""<div style='font-family:Share Tech Mono,monospace;font-size:0.7rem;
    color:#7a7a9a;letter-spacing:0.22em;text-transform:uppercase;margin-bottom:0.5rem;'>
    NAVIGATION</div>""", unsafe_allow_html=True)

    pages = {
        "🏠  Home":              "Home",
        "🪝  Hook Architect":    "Hooks",
        "📜  Script Writer":     "Script",
        "🖼️  Thumbnail Engineer": "Thumbnail",
        "🔖  SEO & Tags":        "SEO",
    }
    if "page" not in st.session_state:
        st.session_state.page = "Home"

    for label, key in pages.items():
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-family:Share Tech Mono,monospace;font-size:0.62rem;
                color:#3a3a5a;text-align:center;line-height:1.7;'>
        Built with ⚡ ViralFlow AI<br>
        Powered by Gemini 1.5 Flash<br>
        v2.1 — Multilingual Edition
    </div>""", unsafe_allow_html=True)

page = st.session_state.page


# ── Helper: language indicator strip ─────────────────────────────────────────
def lang_badge():
    return (
        f'<span class="badge-gold">{lang_cfg["flag"]} {lang_cfg["label"]}</span>'
    )


# ── Helper: hero banner ───────────────────────────────────────────────────────
def render_hero(title: str, subtitle: str, badge: str):
    st.markdown(f"""
    <div class="hero-header">
        <div style='font-family:Share Tech Mono,monospace;font-size:0.7rem;
                    color:#b14fff;letter-spacing:0.38em;margin-bottom:0.5rem;'>{badge}</div>
        <h1 class="hero-title">{title}</h1>
        <div class="hero-sub">{subtitle}</div>
        <div style='margin:0.6rem 0;'>
            <span class="lang-strip">
                <span class="lang-dot"></span>
                OUTPUT LANGUAGE: {lang_cfg["flag"]} {lang_cfg["label"].upper()}
            </span>
        </div>
        <div class="hero-divider"></div>
    </div>
    """, unsafe_allow_html=True)


# ── Helper: styled output block ───────────────────────────────────────────────
def output_block(content: str, label: str = "", border_color: str = "#00e5ff"):
    extra_class = lang_cfg["font_class"]
    label_html = (
        f'<span class="hook-number" style="color:{border_color};">{label}</span>'
        if label else ""
    )
    st.markdown(f"""
    <div class="output-block {extra_class}" style="border-left-color:{border_color};">
        {label_html}{content}
    </div>
    """, unsafe_allow_html=True)


# ────────────────────────────────────────────────────────────────────────────
#  PAGE: HOME
# ────────────────────────────────────────────────────────────────────────────
if page == "Home":
    render_hero(
        "VIRALFLOW AI",
        "THE CONTENT ENGINE FOR CREATORS WHO DOMINATE",
        "⚡ SHORT-FORM VIDEO • AI-POWERED • MULTILINGUAL",
    )

    st.markdown("""
    <div class="metrics-row">
        <div class="metric-box">
            <div class="metric-val">5×</div>
            <div class="metric-label">Hook Variants</div>
        </div>
        <div class="metric-box">
            <div class="metric-val">60s</div>
            <div class="metric-label">Full Scripts</div>
        </div>
        <div class="metric-box">
            <div class="metric-val">3×</div>
            <div class="metric-label">Thumb Prompts</div>
        </div>
        <div class="metric-box">
            <div class="metric-val">20+</div>
            <div class="metric-label">SEO Tags</div>
        </div>
        <div class="metric-box">
            <div class="metric-val">3</div>
            <div class="metric-label">Languages</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="neon-card">
            <div class="section-title"><span class="section-icon">🪝</span>HOOK ARCHITECT</div>
            <div class="section-desc">5 psychology-driven hooks using Curiosity Gap, FOMO,
            Shock, Controversy & Relatability — now in your language of choice.</div>
            <span class="badge-purple">PSYCHOLOGY-DRIVEN</span>
        </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class="neon-card">
            <div class="section-title"><span class="section-icon">🖼️</span>THUMBNAIL ENGINEER</div>
            <div class="section-desc">3 Midjourney/DALL-E ready prompts with bilingual
            text overlay suggestions for local audience thumbnails.</div>
            <span class="badge-cyan">MIDJOURNEY READY</span>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="neon-card">
            <div class="section-title"><span class="section-icon">📜</span>60-SEC SCRIPTWRITER</div>
            <div class="section-desc">Full retention-optimized scripts with visual cues,
            B-roll directions, sound suggestions and CTA — delivered in your language.</div>
            <span class="badge-purple">VISUAL CUES INCLUDED</span>
        </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class="neon-card">
            <div class="section-title"><span class="section-icon">🔖</span>SMART SEO & TAGS</div>
            <div class="section-desc">Tiered hashtag strategy, SEO titles, keyword-rich
            descriptions and posting times — optimised for local and global reach.</div>
            <span class="badge-cyan">ALGORITHM OPTIMIZED</span>
        </div>""", unsafe_allow_html=True)

    # Language showcase card
    st.markdown("""
    <div class="neon-card" style="border-color:rgba(255,215,0,0.3); margin-top:0.5rem;">
        <div class="section-title" style="color:#ffd700;">
            <span class="section-icon">🌐</span>MULTILINGUAL ENGINE
        </div>
        <div style="display:flex; gap:1rem; flex-wrap:wrap; margin-top:0.8rem;">
            <div style="flex:1;min-width:160px;background:rgba(255,215,0,0.05);
                        border:1px solid rgba(255,215,0,0.2);border-radius:8px;padding:0.9rem;">
                <div style="font-family:Orbitron,sans-serif;font-size:0.75rem;
                            color:#ffd700;margin-bottom:0.4rem;">🇬🇧 ENGLISH</div>
                <div style="color:#b0b0c0;font-size:0.88rem;line-height:1.5;">
                    High-energy English for global viral reach.
                </div>
            </div>
            <div style="flex:1;min-width:160px;background:rgba(255,215,0,0.05);
                        border:1px solid rgba(255,215,0,0.2);border-radius:8px;padding:0.9rem;">
                <div style="font-family:Orbitron,sans-serif;font-size:0.75rem;
                            color:#ffd700;margin-bottom:0.4rem;">🇵🇰 ROMAN URDU</div>
                <div style="color:#b0b0c0;font-size:0.88rem;line-height:1.5;">
                    Doston-style Hinglish for Pakistani &amp; Indian TikTok.
                </div>
            </div>
            <div style="flex:1;min-width:160px;background:rgba(255,215,0,0.05);
                        border:1px solid rgba(255,215,0,0.2);border-radius:8px;padding:0.9rem;">
                <div style="font-family:'Noto Nastaliq Urdu',serif;font-size:1rem;
                            color:#ffd700;margin-bottom:0.4rem;direction:rtl;text-align:right;">
                    خالص اردو 🇵🇰
                </div>
                <div style="color:#b0b0c0;font-size:0.88rem;line-height:1.5;">
                    Professional Urdu script for native audiences.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="neon-card" style="border-color:rgba(0,229,255,0.2);margin-top:0.5rem;">
        <div class="section-title" style="color:#00e5ff;">
            <span class="section-icon">🚀</span>QUICK START
        </div>
        <div style="color:#b0b0c0;font-size:0.97rem;line-height:2;">
            <strong style="color:#00e5ff;">1.</strong> &nbsp;Enter your
            <strong style="color:#b14fff;">Gemini API Key</strong> in the sidebar
            → get free at <code style="color:#a0ffd0;">aistudio.google.com</code><br>
            <strong style="color:#00e5ff;">2.</strong> &nbsp;Pick your
            <strong style="color:#b14fff;">Platform</strong> &amp;
            <strong style="color:#ffd700;">Output Language</strong><br>
            <strong style="color:#00e5ff;">3.</strong> &nbsp;Navigate to any tool via the sidebar<br>
            <strong style="color:#00e5ff;">4.</strong> &nbsp;Enter your topic and hit
            <strong style="color:#b14fff;">GENERATE</strong><br>
            <strong style="color:#00e5ff;">5.</strong> &nbsp;Copy your content and
            <strong style="color:#b14fff;">dominate the algorithm</strong> ⚡
        </div>
    </div>
    """, unsafe_allow_html=True)


# ────────────────────────────────────────────────────────────────────────────
#  PAGE: HOOK ARCHITECT
# ────────────────────────────────────────────────────────────────────────────
elif page == "Hooks":
    render_hero(
        "HOOK ARCHITECT",
        "STOP THE SCROLL • TRIGGER PSYCHOLOGY • CAPTURE ATTENTION",
        "🪝 MODULE 01",
    )

    col1, col2 = st.columns([2, 1])
    with col1:
        topic = st.text_input(
            "VIDEO TOPIC",
            placeholder="e.g. How I made $10k in 30 days with AI tools",
            key="hook_topic",
        )
    with col2:
        style = st.selectbox(
            "HOOK STYLE",
            ["Aggressive & Bold", "Mysterious & Intriguing",
             "Relatable & Personal", "Controversial & Edgy",
             "Educational & Shocking"],
            key="hook_style",
        )

    # Language preview
    if selected_lang != "English":
        preview = {
            "Roman Urdu": "🔥 e.g. \"Doston, ye cheez sun ke aap ka dimaag chakkar kha jayega...\"",
            "Pure Urdu":  "✍️ e.g. \"دوستو، یہ بات سن کر آپ حیران رہ جائیں گے...\"",
        }
        st.markdown(f"""
        <div style='background:rgba(255,215,0,0.05);border:1px solid rgba(255,215,0,0.2);
                    border-radius:8px;padding:0.7rem 1rem;margin-bottom:0.8rem;'>
            <span style='font-family:Share Tech Mono,monospace;font-size:0.7rem;
                         color:#ffd700;'>LANGUAGE PREVIEW</span><br>
            <span style='color:#b0b0c0;font-size:0.9rem;'>{preview[selected_lang]}</span>
        </div>
        """, unsafe_allow_html=True)

    generate_btn = st.button("⚡  GENERATE 5 HOOKS", key="gen_hooks", use_container_width=True)

    if generate_btn:
        if not api_key:
            st.error("🔑 Please enter your Gemini API Key in the sidebar first.")
        elif not topic.strip():
            st.warning("📝 Please enter a video topic above.")
        else:
            spinner_msg = {
                "English":    "🧠 Engineering psychological triggers...",
                "Roman Urdu": "🔥 Zabardast hooks bana raha hai...",
                "Pure Urdu":  "✍️ اردو ہکس تیار ہو رہی ہیں...",
            }[selected_lang]

            with st.spinner(spinner_msg):
                result = get_gemini_response(api_key, hook_prompt(topic, platform, style, lang_cfg))

            st.markdown("---")
            st.markdown(f"""
            <div style='display:flex;gap:0.7rem;align-items:center;flex-wrap:wrap;margin-bottom:1rem;'>
                <span class="badge-cyan">✓ GENERATED</span>
                <span class="badge-purple">{platform.upper()}</span>
                {lang_badge()}
                <span style='font-family:Share Tech Mono,monospace;font-size:0.72rem;
                             color:#7a7a9a;'>{style.upper()}</span>
            </div>
            """, unsafe_allow_html=True)

            lines = result.strip().split("\n")
            current_hook = []
            hook_num = 0
            colors = ["#b14fff", "#00e5ff", "#ff2d78", "#b14fff", "#00e5ff"]

            for line in lines:
                if line.strip().startswith("HOOK "):
                    if current_hook:
                        body = "\n".join(current_hook).strip()
                        c = colors[(hook_num - 1) % len(colors)]
                        output_block(body, f"HOOK {hook_num}", c)
                        current_hook = []
                    hook_num += 1
                    current_hook.append(line)
                else:
                    current_hook.append(line)

            if current_hook:
                body = "\n".join(current_hook).strip()
                c = colors[(hook_num - 1) % len(colors)]
                output_block(body, f"HOOK {hook_num}", c)

            st.session_state["last_hooks"] = result
            st.session_state["last_topic"] = topic
            st.info("💡 Head to **Script Writer** to turn your best hook into a full script!")


# ────────────────────────────────────────────────────────────────────────────
#  PAGE: SCRIPT WRITER
# ────────────────────────────────────────────────────────────────────────────
elif page == "Script":
    render_hero(
        "60-SEC SCRIPTWRITER",
        "RETENTION OPTIMIZED • VISUAL CUES • MAXIMUM WATCH TIME",
        "📜 MODULE 02",
    )

    col1, col2 = st.columns([2, 1])
    with col1:
        saved_topic = st.session_state.get("last_topic", "")
        topic = st.text_input(
            "VIDEO TOPIC",
            value=saved_topic,
            placeholder="e.g. 5 AI tools that replaced my entire team",
            key="script_topic",
        )
    with col2:
        duration = st.selectbox(
            "VIDEO DURATION",
            ["30 seconds", "45 seconds", "60 seconds", "90 seconds"],
            index=2,
            key="script_duration",
        )

    hook_placeholder = {
        "English":    "e.g. 'I was $0 in my bank account — then I discovered this...'",
        "Roman Urdu": "e.g. 'Doston, mera account bilkul zero tha — phir ye hua...'",
        "Pure Urdu":  "e.g. 'دوستو، میرا اکاؤنٹ بالکل خالی تھا — پھر یہ ہوا...'",
    }[selected_lang]

    hook_input = st.text_area(
        "OPENING HOOK (from Hook Architect or write your own)",
        placeholder=hook_placeholder,
        height=80,
        key="script_hook",
    )

    if st.button("⚡  GENERATE FULL SCRIPT", key="gen_script", use_container_width=True):
        if not api_key:
            st.error("🔑 Please enter your Gemini API Key in the sidebar first.")
        elif not topic.strip():
            st.warning("📝 Please enter a video topic.")
        elif not hook_input.strip():
            st.warning("🪝 Please add an opening hook.")
        else:
            dur_seconds = int(duration.split()[0])
            spinner_msg = {
                "English":    "✍️ Writing your viral script with visual cues...",
                "Roman Urdu": "🔥 Zabardast script likh raha hai...",
                "Pure Urdu":  "✍️ اردو اسکرپٹ تیار ہو رہی ہے...",
            }[selected_lang]

            with st.spinner(spinner_msg):
                result = get_gemini_response(
                    api_key,
                    script_prompt(topic, hook_input, platform, dur_seconds, lang_cfg)
                )

            st.markdown("---")
            st.markdown(f"""
            <div style='display:flex;gap:0.7rem;align-items:center;flex-wrap:wrap;margin-bottom:1rem;'>
                <span class="badge-cyan">✓ SCRIPT READY</span>
                <span class="badge-purple">{duration.upper()}</span>
                <span class="badge-purple">{platform.upper()}</span>
                {lang_badge()}
            </div>
            """, unsafe_allow_html=True)

            # Color-code production markers (always English)
            formatted = result
            cue_map = {
                "[VISUAL CUE]":  ('<span style="color:#00e5ff;font-family:Share Tech Mono,'
                                  'monospace;font-size:0.78rem;">[VISUAL CUE]</span>'),
                "[SOUND CUE]":   ('<span style="color:#ff2d78;font-family:Share Tech Mono,'
                                  'monospace;font-size:0.78rem;">[SOUND CUE]</span>'),
                "[MUSIC]":       ('<span style="color:#ff2d78;font-family:Share Tech Mono,'
                                  'monospace;font-size:0.78rem;">[MUSIC]</span>'),
                "[TEXT OVERLAY]":('<span style="color:#b14fff;font-family:Share Tech Mono,'
                                  'monospace;font-size:0.78rem;">[TEXT OVERLAY]</span>'),
                "[TRANSITION]":  ('<span style="color:#ffd700;font-family:Share Tech Mono,'
                                  'monospace;font-size:0.78rem;">[TRANSITION]</span>'),
                "[HOOK":         ('<span style="color:#00e5ff;font-weight:600;'
                                  'font-family:Orbitron,sans-serif;font-size:0.78rem;">[HOOK</span>'),
                "[BODY":         ('<span style="color:#b14fff;font-weight:600;'
                                  'font-family:Orbitron,sans-serif;font-size:0.78rem;">[BODY</span>'),
                "[CTA":          ('<span style="color:#ff2d78;font-weight:600;'
                                  'font-family:Orbitron,sans-serif;font-size:0.78rem;">[CTA</span>'),
            }
            for k, v in cue_map.items():
                formatted = formatted.replace(k, v)

            extra_class = lang_cfg["font_class"]
            st.markdown(f"""
            <div class="output-block {extra_class}" style="font-size:0.95rem;line-height:2.1;">
                {formatted}
            </div>
            """, unsafe_allow_html=True)

            with st.expander("📋 Copy Raw Script"):
                copy_class = lang_cfg["font_class"]
                st.markdown(f'<div class="copy-area {copy_class}">{result}</div>',
                            unsafe_allow_html=True)


# ────────────────────────────────────────────────────────────────────────────
#  PAGE: THUMBNAIL ENGINEER
# ────────────────────────────────────────────────────────────────────────────
elif page == "Thumbnail":
    render_hero(
        "THUMBNAIL ENGINEER",
        "MIDJOURNEY-READY PROMPTS • HIGH CTR • VIRAL VISUALS",
        "🖼️ MODULE 03",
    )

    # Note about English prompts
    if selected_lang != "English":
        st.markdown(f"""
        <div style='background:rgba(0,229,255,0.05);border:1px solid rgba(0,229,255,0.2);
                    border-radius:8px;padding:0.8rem 1rem;margin-bottom:1rem;'>
            <span style='font-family:Share Tech Mono,monospace;font-size:0.72rem;
                         color:#00e5ff;'>ℹ️ THUMBNAIL NOTE</span><br>
            <span style='color:#b0b0c0;font-size:0.9rem;'>
                Image generation prompts are kept in <strong style="color:#00e5ff;">English</strong>
                for best AI results. Bilingual
                <strong style="color:#ffd700;">{lang_cfg['label']}</strong>
                text overlay suggestions are included so you can add local-language
                text in your video editor.
            </span>
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        saved_topic = st.session_state.get("last_topic", "")
        topic = st.text_input(
            "VIDEO TOPIC",
            value=saved_topic,
            placeholder="e.g. How I lost 20 pounds in 60 days",
            key="thumb_topic",
        )
    with col2:
        thumb_style = st.selectbox(
            "VISUAL STYLE",
            ["Hyper-Realistic Photography", "Cinematic & Dramatic",
             "Bold Graphic / Text-Heavy", "Minimalist & Clean",
             "Explosive & Action-Packed"],
            key="thumb_style",
        )

    if st.button("⚡  GENERATE THUMBNAIL PROMPTS", key="gen_thumb", use_container_width=True):
        if not api_key:
            st.error("🔑 Please enter your Gemini API Key in the sidebar first.")
        elif not topic.strip():
            st.warning("📝 Please enter a video topic.")
        else:
            with st.spinner("🎨 Engineering viral thumbnail concepts..."):
                result = get_gemini_response(
                    api_key, thumbnail_prompt(topic, platform, thumb_style, lang_cfg)
                )

            st.markdown("---")
            st.markdown(f"""
            <div style='display:flex;gap:0.7rem;align-items:center;flex-wrap:wrap;margin-bottom:1rem;'>
                <span class="badge-cyan">✓ 3 PROMPTS READY</span>
                <span class="badge-purple">{thumb_style.upper()}</span>
                {lang_badge()}
            </div>
            """, unsafe_allow_html=True)

            lines_list = result.split("\n")
            prompt_blocks = []
            negative_block = ""
            current = []

            for line in lines_list:
                if line.startswith("PROMPT ") and current:
                    prompt_blocks.append("\n".join(current))
                    current = [line]
                elif line.startswith("NEGATIVE"):
                    if current:
                        prompt_blocks.append("\n".join(current))
                        current = []
                    negative_block = line
                elif negative_block:
                    negative_block += "\n" + line
                else:
                    current.append(line)
            if current:
                prompt_blocks.append("\n".join(current))

            colors = ["#b14fff", "#00e5ff", "#ff2d78"]
            for i, block in enumerate(prompt_blocks[:3]):
                c = colors[i % 3]
                # Thumbnail prompts always English — no urdu-script class
                st.markdown(f"""
                <div class="output-block" style="border-left-color:{c};">
                    <span class="hook-number" style="color:{c};">THUMBNAIL PROMPT {i+1}</span>
                    {block.strip()}
                </div>
                """, unsafe_allow_html=True)

            if negative_block.strip():
                st.markdown(f"""
                <div class="output-block" style="border-left-color:#ff2d78;
                     background:rgba(255,45,120,0.04);">
                    <span class="hook-number" style="color:#ff2d78;">NEGATIVE PROMPTS</span>
                    {negative_block.strip()}
                </div>
                """, unsafe_allow_html=True)

            st.markdown("""
            <div style='margin-top:0.8rem;padding:0.8rem 1rem;
                        background:rgba(0,229,255,0.05);border-radius:8px;
                        border:1px solid rgba(0,229,255,0.15);'>
                <span style='font-family:Share Tech Mono,monospace;font-size:0.73rem;
                             color:#00e5ff;'>💡 PRO TIP</span><br>
                <span style='color:#7a7a9a;font-size:0.88rem;'>
                    Copy any prompt → paste into Midjourney with /imagine or DALL-E 3.
                    Recommended AR: <strong style="color:#e8e8ff;">16:9</strong> for thumbnails.
                    Use the bilingual text overlay suggestions in CapCut or Premiere.
                </span>
            </div>
            """, unsafe_allow_html=True)


# ────────────────────────────────────────────────────────────────────────────
#  PAGE: SEO & TAGS
# ────────────────────────────────────────────────────────────────────────────
elif page == "SEO":
    render_hero(
        "SMART SEO & TAGS",
        "ALGORITHM OPTIMIZED • HASHTAG STRATEGY • MAXIMUM REACH",
        "🔖 MODULE 04",
    )

    col1, col2 = st.columns([2, 1])
    with col1:
        saved_topic = st.session_state.get("last_topic", "")
        topic = st.text_input(
            "VIDEO TOPIC",
            value=saved_topic,
            placeholder="e.g. Passive income ideas for beginners 2025",
            key="seo_topic",
        )
    with col2:
        niche = st.selectbox(
            "CONTENT NICHE",
            ["Finance & Money", "Fitness & Health", "Tech & AI",
             "Business & Entrepreneurship", "Lifestyle & Vlogs",
             "Food & Cooking", "Fashion & Beauty", "Gaming",
             "Education & How-To", "Travel & Adventure"],
            key="seo_niche",
        )

    # Language note for Pure Urdu
    if selected_lang == "Pure Urdu":
        st.markdown("""
        <div style='background:rgba(255,215,0,0.05);border:1px solid rgba(255,215,0,0.2);
                    border-radius:8px;padding:0.7rem 1rem;margin-bottom:0.8rem;'>
            <span style='font-family:Share Tech Mono,monospace;font-size:0.7rem;color:#ffd700;'>
                ℹ️ HASHTAG NOTE</span><br>
            <span style='color:#b0b0c0;font-size:0.88rem;'>
                Hashtags will include Urdu script + Roman transliteration in brackets
                for platform compatibility (e.g. #وائرل (#Viral)).
            </span>
        </div>
        """, unsafe_allow_html=True)

    if st.button("⚡  GENERATE SEO PACKAGE", key="gen_seo", use_container_width=True):
        if not api_key:
            st.error("🔑 Please enter your Gemini API Key in the sidebar first.")
        elif not topic.strip():
            st.warning("📝 Please enter a video topic.")
        else:
            spinner_msg = {
                "English":    "📊 Analyzing algorithm patterns & generating SEO package...",
                "Roman Urdu": "🔥 Algorithm samajh raha hai, SEO bana raha hai...",
                "Pure Urdu":  "📊 الگورتھم تجزیہ اور SEO پیکج تیار ہو رہا ہے...",
            }[selected_lang]

            with st.spinner(spinner_msg):
                result = get_gemini_response(
                    api_key, seo_prompt(topic, platform, niche, lang_cfg)
                )

            st.markdown("---")
            st.markdown(f"""
            <div style='display:flex;gap:0.7rem;align-items:center;flex-wrap:wrap;margin-bottom:1.1rem;'>
                <span class="badge-cyan">✓ SEO PACKAGE READY</span>
                <span class="badge-purple">{niche.upper()}</span>
                <span class="badge-purple">{platform.upper()}</span>
                {lang_badge()}
            </div>
            """, unsafe_allow_html=True)

            # Parse sections
            sections: dict = {}
            current_section = "other"
            sections[current_section] = []

            section_map = {
                "VIDEO TITLE":         "titles",
                "OPTIMIZED DESCRIPTION": "description",
                "HASHTAG STRATEGY":    "hashtags",
                "KEYWORD DENSITY":     "keywords",
                "BEST POSTING TIMES":  "timing",
                "ENGAGEMENT BAIT":     "bait",
            }
            for line in result.split("\n"):
                upper = line.strip().upper()
                matched = False
                for key, sec in section_map.items():
                    if key in upper:
                        current_section = sec
                        sections[current_section] = []
                        matched = True
                        break
                if not matched:
                    sections.setdefault(current_section, []).append(line)

            extra_class = lang_cfg["font_class"]

            def render_section(title, content, border_color="#b14fff"):
                body = "\n".join(content).strip()
                if body:
                    st.markdown(f"""
                    <div class="output-block {extra_class}" style="border-left-color:{border_color};">
                        <span class="hook-number" style="color:{border_color};
                                                         direction:ltr;text-align:left;">
                            {title}
                        </span>
                        {body}
                    </div>
                    """, unsafe_allow_html=True)

            render_section("📌 VIDEO TITLE OPTIONS",   sections.get("titles", []),      "#00e5ff")
            render_section("📄 OPTIMIZED DESCRIPTION", sections.get("description", []), "#b14fff")
            render_section("🏷️ HASHTAG STRATEGY",      sections.get("hashtags", []),    "#b14fff")

            # Hashtag pills (always LTR)
            hashtag_lines = "\n".join(sections.get("hashtags", []))
            hashtags_found = [
                w for w in hashtag_lines.split()
                if w.startswith("#") and len(w) > 2
            ]
            if hashtags_found:
                pills_html = "".join(
                    f'<span class="tag-pill">{tag}</span>' for tag in hashtags_found
                )
                st.markdown(f"""
                <div style='margin:0.4rem 0 1rem;padding:1rem;background:var(--bg-card);
                            border-radius:8px;border:1px solid var(--border);'>
                    <div style='font-family:Share Tech Mono,monospace;font-size:0.7rem;
                                color:#7a7a9a;letter-spacing:0.18em;margin-bottom:0.7rem;
                                direction:ltr;text-align:left;'>
                        ALL HASHTAGS
                    </div>
                    <div style='direction:ltr;text-align:left;'>{pills_html}</div>
                </div>
                """, unsafe_allow_html=True)

            render_section("🔑 KEYWORD TARGETS",      sections.get("keywords", []), "#00e5ff")
            render_section("⏰ BEST POSTING TIMES",   sections.get("timing", []),   "#ff2d78")
            render_section("💬 ENGAGEMENT BAIT LINE", sections.get("bait", []),     "#b14fff")

            with st.expander("📋 Copy Full Raw Output"):
                copy_class = lang_cfg["font_class"]
                st.markdown(f'<div class="copy-area {copy_class}">{result}</div>',
                            unsafe_allow_html=True)
