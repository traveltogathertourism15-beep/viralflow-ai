import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="ViralFlow AI", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&family=Share+Tech+Mono&family=Noto+Nastaliq+Urdu:wght@400;700&display=swap');
:root{--bg-deep:#050510;--bg-card:#0d0d1f;--bg-input:#0a0a1a;--neon-purple:#b14fff;--neon-cyan:#00e5ff;--neon-pink:#ff2d78;--neon-gold:#ffd700;--text-primary:#e8e8ff;--text-muted:#7a7a9a;--border:rgba(177,79,255,0.25);}
html,body,[data-testid="stAppViewContainer"]{background:#050510!important;color:#e8e8ff!important;font-family:'Rajdhani',sans-serif!important;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#07071a,#0d0d25)!important;border-right:1px solid rgba(177,79,255,0.25)!important;}
[data-testid="stSidebar"] *{color:#ffffff!important;font-size:1rem!important;}
[data-testid="stSidebar"] [data-testid="stSelectbox"] div{background:#12122a!important;color:#ffffff!important;border:1px solid rgba(177,79,255,0.4)!important;}
[data-baseweb="popover"] ul li{background:#12122a!important;color:#ffffff!important;padding:0.6rem 1rem!important;}
[data-baseweb="popover"] ul li:hover{background:rgba(177,79,255,0.25)!important;color:#00e5ff!important;}
[data-testid="stSidebar"] [data-testid="stButton"]>button{background:rgba(177,79,255,0.12)!important;color:#ffffff!important;border:1px solid rgba(177,79,255,0.3)!important;font-size:0.95rem!important;}
[data-testid="stSidebar"] [data-testid="stButton"]>button:hover{background:rgba(0,229,255,0.15)!important;color:#00e5ff!important;}
#MainMenu,footer,header{visibility:hidden;}
.hero-header{text-align:center;padding:2.5rem 1rem 1.5rem;}
.hero-title{font-family:'Orbitron',sans-serif;font-size:clamp(1.8rem,5vw,4rem);font-weight:900;background:linear-gradient(90deg,#b14fff,#00e5ff,#b14fff);background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;animation:shimmer 3s linear infinite;margin:0;}
@keyframes shimmer{0%{background-position:0% center;}100%{background-position:200% center;}}
.hero-sub{font-family:'Share Tech Mono',monospace;color:#00e5ff;font-size:clamp(0.6rem,1.5vw,0.85rem);letter-spacing:0.25em;margin-top:0.6rem;opacity:0.8;}
.hero-divider{height:2px;background:linear-gradient(90deg,transparent,#b14fff,#00e5ff,transparent);margin:1.5rem auto;max-width:600px;}
.lang-strip{display:inline-flex;align-items:center;gap:0.5rem;background:rgba(255,215,0,0.07);border:1px solid rgba(255,215,0,0.3);border-radius:20px;padding:0.3rem 1rem;font-family:'Share Tech Mono',monospace;font-size:0.72rem;color:#ffd700;letter-spacing:0.15em;}
.lang-dot{width:7px;height:7px;background:#ffd700;border-radius:50%;display:inline-block;animation:pulse-gold 2s ease-in-out infinite;}
@keyframes pulse-gold{0%,100%{opacity:1;}50%{opacity:0.4;}}
.neon-card{background:#0d0d1f;border:1px solid rgba(177,79,255,0.25);border-radius:12px;padding:1.6rem;margin:0.8rem 0;position:relative;overflow:hidden;}
.neon-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#b14fff,#00e5ff);}
.section-title{font-family:'Orbitron',sans-serif;font-size:1.1rem;font-weight:700;color:#00e5ff;letter-spacing:0.08em;margin-bottom:0.4rem;text-transform:uppercase;}
.section-desc{color:#7a7a9a;font-size:0.93rem;margin-bottom:1rem;line-height:1.5;}
[data-testid="stTextInput"] input,[data-testid="stTextArea"] textarea{background:#0a0a1a!important;border:1px solid rgba(177,79,255,0.25)!important;color:#e8e8ff!important;border-radius:8px!important;font-family:'Rajdhani',sans-serif!important;font-size:1rem!important;}
[data-testid="stTextInput"] input:focus,[data-testid="stTextArea"] textarea:focus{border-color:#00e5ff!important;box-shadow:0 0 18px rgba(0,229,255,0.4)!important;}
[data-testid="stTextInput"] label,[data-testid="stTextArea"] label,[data-testid="stSelectbox"] label{color:#7a7a9a!important;font-family:'Share Tech Mono',monospace!important;font-size:0.75rem!important;letter-spacing:0.18em!important;text-transform:uppercase!important;}
[data-testid="stButton"]>button{background:linear-gradient(135deg,#b14fff,#6a00cc)!important;color:#fff!important;border:none!important;border-radius:8px!important;font-family:'Orbitron',sans-serif!important;font-size:0.75rem!important;font-weight:700!important;letter-spacing:0.14em!important;padding:0.65rem 1.6rem!important;text-transform:uppercase!important;box-shadow:0 0 20px rgba(177,79,255,0.4)!important;width:100%;}
[data-testid="stButton"]>button:hover{transform:translateY(-2px)!important;box-shadow:0 0 35px rgba(177,79,255,0.75)!important;}
.output-block{background:#08081c;border:1px solid rgba(0,229,255,0.2);border-left:3px solid #00e5ff;border-radius:8px;padding:1.2rem 1.4rem;margin:0.7rem 0;font-size:1rem;color:#e8e8ff;line-height:1.8;white-space:pre-wrap;word-break:break-word;}
.output-block.urdu-script{font-family:'Noto Nastaliq Urdu',serif!important;font-size:1.15rem!important;direction:rtl;text-align:right;line-height:2.2!important;}
.hook-number{font-family:'Orbitron',sans-serif;font-size:0.68rem;letter-spacing:0.2em;display:block;margin-bottom:0.4rem;opacity:0.8;direction:ltr;text-align:left;}
.tag-pill{display:inline-block;background:rgba(177,79,255,0.12);border:1px solid rgba(177,79,255,0.35);color:#b14fff;border-radius:20px;padding:0.22rem 0.8rem;margin:0.22rem;font-family:'Share Tech Mono',monospace;font-size:0.76rem;}
.badge-purple{display:inline-block;background:rgba(177,79,255,0.15);border:1px solid #b14fff;color:#b14fff;border-radius:4px;padding:0.14rem 0.65rem;font-family:'Share Tech Mono',monospace;font-size:0.7rem;text-transform:uppercase;}
.badge-cyan{display:inline-block;background:rgba(0,229,255,0.1);border:1px solid #00e5ff;color:#00e5ff;border-radius:4px;padding:0.14rem 0.65rem;font-family:'Share Tech Mono',monospace;font-size:0.7rem;text-transform:uppercase;}
.badge-gold{display:inline-block;background:rgba(255,215,0,0.1);border:1px solid #ffd700;color:#ffd700;border-radius:4px;padding:0.14rem 0.65rem;font-family:'Share Tech Mono',monospace;font-size:0.7rem;text-transform:uppercase;}
.metrics-row{display:flex;gap:0.8rem;flex-wrap:wrap;margin:1rem 0;}
.metric-box{flex:1;min-width:80px;background:#0d0d1f;border:1px solid rgba(177,79,255,0.25);border-radius:10px;padding:0.9rem;text-align:center;}
.metric-val{font-family:'Orbitron',sans-serif;font-size:1.6rem;font-weight:700;background:linear-gradient(90deg,#b14fff,#00e5ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.metric-label{font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:#7a7a9a;letter-spacing:0.12em;text-transform:uppercase;margin-top:0.2rem;}
.copy-area{background:#06060f;border:1px dashed rgba(0,229,255,0.3);border-radius:8px;padding:1rem 1.2rem;font-family:'Share Tech Mono',monospace;font-size:0.82rem;color:#a0ffd0;white-space:pre-wrap;line-height:1.65;word-break:break-word;}
.copy-area.urdu-script{font-family:'Noto Nastaliq Urdu',serif!important;direction:rtl;text-align:right;color:#e8e8ff!important;}
hr{border:none;height:1px;background:linear-gradient(90deg,transparent,rgba(177,79,255,0.25),transparent);margin:1.3rem 0;}
::-webkit-scrollbar{width:6px;} ::-webkit-scrollbar-track{background:#050510;} ::-webkit-scrollbar-thumb{background:#b14fff;border-radius:3px;}
[data-testid="stExpander"]{border:1px solid rgba(177,79,255,0.25)!important;border-radius:8px!important;background:#0d0d1f!important;}
[data-testid="stExpander"] summary{color:#00e5ff!important;font-weight:600!important;}
@media(max-width:768px){.hero-title{font-size:1.7rem!important;}.metric-val{font-size:1.3rem;}.neon-card{padding:1.1rem;}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

LANG_CONFIG = {
    "English": {
        "code": "en", "flag": "GB", "label": "ENGLISH", "font_class": "",
        "instruction": "Write all output in clear, high-energy English for viral short-form content.",
        "hook_flavour": "Use powerful English words, action verbs, and punchy sentences.",
        "seo_note": "All titles, descriptions, and hashtags in English.",
    },
    "Roman Urdu": {
        "code": "roman_urdu", "flag": "PK", "label": "ROMAN URDU", "font_class": "",
        "instruction": "Write all output in ROMAN URDU - trendy conversational style used by Pakistani and Indian TikTok creators. Urdu words in English alphabet. Mix words like: Doston, Zabardast, Kamaal, Yaar, Bhai, Sun lo, Sach bolunga, Ekdum fire, Viral ho gaya, Game changer, Seedha baat.",
        "hook_flavour": "Start with: Doston, or Yaar sun lo, or Bhai ek second ruko, or Sach bolunga,",
        "seo_note": "Titles and descriptions in Roman Urdu mixed with English. Hashtags in English characters only.",
    },
    "Pure Urdu": {
        "code": "urdu", "flag": "PK", "label": "URDU", "font_class": "urdu-script",
        "instruction": "Write ALL output in PURE URDU SCRIPT only. Grammatically correct professional Urdu. Every sentence in authentic Urdu script.",
        "hook_flavour": "Address audience with dosto or yaaro, use Urdu idioms, short punchy sentences.",
        "seo_note": "Titles and descriptions in Urdu script. Hashtags include Urdu plus Roman transliteration in brackets.",
    },
}

def get_gemini_response(api_key, prompt):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        resp = model.generate_content(prompt)
        return resp.text
    except Exception as e:
        return "API Error: " + str(e)

def build_hook_prompt(topic, platform, style, lang_cfg):
    lines = [
        "You are a viral content strategist.",
        "",
        "LANGUAGE REQUIREMENT:",
        lang_cfg["instruction"],
        lang_cfg["hook_flavour"],
        "",
        "Create EXACTLY 5 video hooks for: " + topic,
        "Platform: " + platform + " | Style: " + style,
        "",
        "Triggers to use: 1.Curiosity Gap 2.Shock 3.Controversy 4.FOMO 5.Relatability",
        "",
        "Format exactly like this:",
        "HOOK 1 | [TRIGGER NAME]",
        "[Hook text in required language]",
        "",
        "HOOK 2 | [TRIGGER NAME]",
        "[Hook text]",
        "",
        "HOOK 3 | [TRIGGER NAME]",
        "[Hook text]",
        "",
        "HOOK 4 | [TRIGGER NAME]",
        "[Hook text]",
        "",
        "HOOK 5 | [TRIGGER NAME]",
        "[Hook text]",
        "",
        "Rules: Max 2 sentences each. No hashtags. Hook text strictly in required language.",
    ]
    return "\n".join(lines)

def build_script_prompt(topic, hook, platform, duration, lang_cfg):
    d = str(duration)
    d2 = str(duration - 10)
    lines = [
        "You are a viral short-form video scriptwriter.",
        "",
        "LANGUAGE REQUIREMENT:",
        lang_cfg["instruction"],
        "",
        "Write a " + d + "-second script for:",
        "Topic: " + topic,
        "Hook: " + hook,
        "Platform: " + platform,
        "",
        "All spoken dialogue in required language. Keep [VISUAL CUE] [SOUND CUE] markers in English.",
        "",
        "[HOOK - 0-3s]",
        "{opening hook in required language}",
        "",
        "[VISUAL CUE]: {screen description}",
        "[SOUND CUE]: {music suggestion}",
        "",
        "[BODY - 3-" + d2 + "s]",
        "{punchy sentences in required language}",
        "",
        "[VISUAL CUE]: {b-roll description}",
        "[TRANSITION]: {cut type}",
        "",
        "[CTA - " + d2 + "s-" + d + "s]",
        "{call to action in required language}",
        "",
        "[TEXT OVERLAY]: {on screen text}",
        "",
        "Rules: Min 4 visual cues, 2 sound cues, 1 text overlay. Strong CTA.",
    ]
    return "\n".join(lines)

def build_thumbnail_prompt(topic, platform, style, lang_cfg):
    lines = [
        "You are a thumbnail designer and AI image prompt engineer.",
        "Topic: " + topic + " for " + platform + ". Style: " + style,
        "",
        "Generate 3 detailed image generation prompts in ENGLISH only.",
        "",
        "Format:",
        "PROMPT 1 | [STYLE TAG]",
        "[Detailed English prompt: subject, expression, colors, lighting, composition, quality tags]",
        "",
        "PROMPT 2 | [STYLE TAG]",
        "[Detailed prompt]",
        "",
        "PROMPT 3 | [STYLE TAG]",
        "[Detailed prompt]",
        "",
        "NEGATIVE PROMPTS:",
        "[What to exclude for clean results]",
        "",
        "Each prompt must include: facial expression, color palette, lighting style, composition rule, 8K quality tags.",
    ]
    if lang_cfg["code"] != "en":
        lines.insert(2, "Also add TEXT OVERLAY suggestion in " + lang_cfg["label"] + " for each prompt.")
    return "\n".join(lines)

def build_seo_prompt(topic, platform, niche, lang_cfg):
    lines = [
        "You are a viral SEO expert.",
        "",
        "LANGUAGE REQUIREMENT:",
        lang_cfg["instruction"],
        lang_cfg["seo_note"],
        "",
        "Topic: " + topic + " | Platform: " + platform + " | Niche: " + niche,
        "",
        "VIDEO TITLE OPTIONS:",
        "Title 1: [SEO title]",
        "Title 2: [Alternative title]",
        "Title 3: [Question title]",
        "",
        "OPTIMIZED DESCRIPTION:",
        "[150-200 word description in required language]",
        "",
        "HASHTAG STRATEGY:",
        "",
        "MEGA TAGS (use 3):",
        "#tag1 #tag2 #tag3",
        "",
        "VIRAL TAGS (use 5):",
        "#tag1 #tag2 #tag3 #tag4 #tag5",
        "",
        "NICHE TAGS (use 8):",
        "#tag1 #tag2 #tag3 #tag4 #tag5 #tag6 #tag7 #tag8",
        "",
        "MICRO TAGS (use 4):",
        "#tag1 #tag2 #tag3 #tag4",
        "",
        "KEYWORD DENSITY TARGETS:",
        "Primary: [keyword]",
        "Secondary: [kw1], [kw2], [kw3]",
        "",
        "BEST POSTING TIMES for " + platform + ":",
        "[Day]: [Time] - [reason]",
        "[Day]: [Time] - [reason]",
        "",
        "ENGAGEMENT BAIT LINE:",
        "[One sentence to drive comments]",
    ]
    return "\n".join(lines)

with st.sidebar:
    st.markdown("<div style='text-align:center;padding:1rem 0 0.5rem;'><div style='font-family:Orbitron,sans-serif;font-size:1.35rem;font-weight:900;background:linear-gradient(90deg,#b14fff,#00e5ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;'>VIRALFLOW</div><div style='font-family:Share Tech Mono,monospace;font-size:0.62rem;color:#00e5ff;letter-spacing:0.3em;margin-top:0.2rem;opacity:0.7;'>CONTENT ENGINE v2.1</div></div><hr style='border:none;height:1px;background:linear-gradient(90deg,transparent,rgba(177,79,255,0.5),transparent);margin:0.6rem 0 0.9rem;'/>", unsafe_allow_html=True)

    st.markdown("<div style='font-family:Share Tech Mono,monospace;font-size:0.7rem;color:#ffd700;letter-spacing:0.2em;text-transform:uppercase;margin-bottom:0.3rem;'>GEMINI API KEY</div>", unsafe_allow_html=True)
    api_key = st.text_input("k", type="password", placeholder="AIza...", label_visibility="collapsed")
    if api_key:
        st.markdown('<span class="badge-cyan">CONNECTED</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge-purple">NOT SET</span>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='font-family:Share Tech Mono,monospace;font-size:0.7rem;color:#ffd700;letter-spacing:0.2em;text-transform:uppercase;margin-bottom:0.3rem;'>TARGET PLATFORM</div>", unsafe_allow_html=True)
    platform = st.selectbox("p", ["TikTok", "Instagram Reels", "YouTube Shorts"], label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='font-family:Share Tech Mono,monospace;font-size:0.7rem;color:#ffd700;letter-spacing:0.2em;text-transform:uppercase;margin-bottom:0.3rem;'>OUTPUT LANGUAGE</div>", unsafe_allow_html=True)
    selected_lang = st.selectbox("l", list(LANG_CONFIG.keys()), label_visibility="collapsed", key="selected_language")
    lang_cfg = LANG_CONFIG[selected_lang]

    lang_info = {"English": "Global reach - High energy English", "Roman Urdu": "Pakistani/Indian TikTok style", "Pure Urdu": "Professional Urdu script"}
    st.markdown("<div style='background:rgba(255,215,0,0.06);border:1px solid rgba(255,215,0,0.2);border-radius:8px;padding:0.6rem 0.8rem;margin-top:0.4rem;'><div style='font-size:0.9rem;color:#ffd700;'>" + lang_info[selected_lang] + "</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='font-family:Share Tech Mono,monospace;font-size:0.7rem;color:#ffd700;letter-spacing:0.22em;text-transform:uppercase;margin-bottom:0.5rem;'>NAVIGATION</div>", unsafe_allow_html=True)

    pages = {"HOME": "Home", "HOOK ARCHITECT": "Hooks", "SCRIPT WRITER": "Script", "THUMBNAIL ENGINEER": "Thumbnail", "SEO AND TAGS": "SEO"}
    if "page" not in st.session_state:
        st.session_state.page = "Home"
    for label, key in pages.items():
        if st.button(label, key="nav_" + key, use_container_width=True):
            st.session_state.page = key

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='font-family:Share Tech Mono,monospace;font-size:0.62rem;color:#3a3a5a;text-align:center;line-height:1.7;'>ViralFlow AI v2.1<br>Gemini 1.5 Flash</div>", unsafe_allow_html=True)

page = st.session_state.page

def lang_badge():
    return '<span class="badge-gold">' + lang_cfg["flag"] + " " + lang_cfg["label"] + "</span>"

def render_hero(title, subtitle, badge):
    st.markdown("<div class='hero-header'><div style='font-family:Share Tech Mono,monospace;font-size:0.7rem;color:#b14fff;letter-spacing:0.38em;margin-bottom:0.5rem;'>" + badge + "</div><h1 class='hero-title'>" + title + "</h1><div class='hero-sub'>" + subtitle + "</div><div style='margin:0.6rem 0;'><span class='lang-strip'><span class='lang-dot'></span>LANGUAGE: " + lang_cfg["flag"] + " " + lang_cfg["label"].upper() + "</span></div><div class='hero-divider'></div></div>", unsafe_allow_html=True)

def show_output(content, label="", border_color="#00e5ff"):
    extra = lang_cfg["font_class"]
    lbl = "<span class='hook-number' style='color:" + border_color + ";'>" + label + "</span>" if label else ""
    st.markdown("<div class='output-block " + extra + "' style='border-left-color:" + border_color + ";'>" + lbl + content + "</div>", unsafe_allow_html=True)

if page == "Home":
    render_hero("VIRALFLOW AI", "THE CONTENT ENGINE FOR CREATORS WHO DOMINATE", "SHORT-FORM VIDEO - AI-POWERED - MULTILINGUAL")
    st.markdown("<div class='metrics-row'><div class='metric-box'><div class='metric-val'>5x</div><div class='metric-label'>Hooks</div></div><div class='metric-box'><div class='metric-val'>60s</div><div class='metric-label'>Scripts</div></div><div class='metric-box'><div class='metric-val'>3x</div><div class='metric-label'>Thumbnails</div></div><div class='metric-box'><div class='metric-val'>20+</div><div class='metric-label'>SEO Tags</div></div><div class='metric-box'><div class='metric-val'>3</div><div class='metric-label'>Languages</div></div></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='neon-card'><div class='section-title'>HOOK ARCHITECT</div><div class='section-desc'>5 psychology-driven hooks using Curiosity, FOMO, Shock, Controversy and Relatability in your language.</div><span class='badge-purple'>PSYCHOLOGY</span></div>", unsafe_allow_html=True)
        st.markdown("<div class='neon-card'><div class='section-title'>THUMBNAIL ENGINEER</div><div class='section-desc'>3 Midjourney and DALL-E ready prompts with bilingual text overlay suggestions.</div><span class='badge-cyan'>MIDJOURNEY READY</span></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='neon-card'><div class='section-title'>SCRIPTWRITER</div><div class='section-desc'>Full scripts with visual cues, B-roll, sound directions and strong CTA in your language.</div><span class='badge-purple'>VISUAL CUES</span></div>", unsafe_allow_html=True)
        st.markdown("<div class='neon-card'><div class='section-title'>SMART SEO</div><div class='section-desc'>Tiered hashtags, SEO titles, keyword descriptions and best posting times for max reach.</div><span class='badge-cyan'>ALGORITHM</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='neon-card' style='border-color:rgba(0,229,255,0.2);margin-top:0.5rem;'><div class='section-title' style='color:#00e5ff;'>QUICK START</div><div style='color:#b0b0c0;font-size:0.97rem;line-height:2;'><strong style='color:#00e5ff;'>1.</strong> Enter Gemini API Key in sidebar - free at aistudio.google.com<br><strong style='color:#00e5ff;'>2.</strong> Pick Platform and Language<br><strong style='color:#00e5ff;'>3.</strong> Go to any tool in sidebar<br><strong style='color:#00e5ff;'>4.</strong> Enter topic and hit GENERATE</div></div>", unsafe_allow_html=True)

elif page == "Hooks":
    render_hero("HOOK ARCHITECT", "STOP THE SCROLL - TRIGGER PSYCHOLOGY - CAPTURE ATTENTION", "MODULE 01")
    c1, c2 = st.columns([2, 1])
    with c1:
        topic = st.text_input("VIDEO TOPIC", placeholder="e.g. How I made $10k in 30 days with AI tools", key="hook_topic")
    with c2:
        style = st.selectbox("HOOK STYLE", ["Aggressive and Bold", "Mysterious and Intriguing", "Relatable and Personal", "Controversial and Edgy", "Educational and Shocking"], key="hook_style")
    if st.button("GENERATE 5 HOOKS", key="gen_hooks", use_container_width=True):
        if not api_key:
            st.error("Please enter your Gemini API Key in the sidebar first.")
        elif not topic.strip():
            st.warning("Please enter a video topic.")
        else:
            spin = {"English": "Generating hooks...", "Roman Urdu": "Zabardast hooks bana raha hai...", "Pure Urdu": "Hooks tayar ho rahi hain..."}
            with st.spinner(spin[selected_lang]):
                result = get_gemini_response(api_key, build_hook_prompt(topic, platform, style, lang_cfg))
            st.markdown("---")
            st.markdown("<div style='display:flex;gap:0.7rem;align-items:center;flex-wrap:wrap;margin-bottom:1rem;'><span class='badge-cyan'>GENERATED</span><span class='badge-purple'>" + platform.upper() + "</span>" + lang_badge() + "</div>", unsafe_allow_html=True)
            lines = result.strip().split("\n")
            current_hook, hook_num = [], 0
            colors = ["#b14fff", "#00e5ff", "#ff2d78", "#b14fff", "#00e5ff"]
            for line in lines:
                if line.strip().startswith("HOOK "):
                    if current_hook:
                        show_output("\n".join(current_hook).strip(), "HOOK " + str(hook_num), colors[(hook_num - 1) % 5])
                        current_hook = []
                    hook_num += 1
                    current_hook.append(line)
                else:
                    current_hook.append(line)
            if current_hook:
                show_output("\n".join(current_hook).strip(), "HOOK " + str(hook_num), colors[(hook_num - 1) % 5])
            st.session_state["last_topic"] = topic
            st.info("Go to Script Writer to turn your best hook into a full script!")

elif page == "Script":
    render_hero("60-SEC SCRIPTWRITER", "RETENTION OPTIMIZED - VISUAL CUES - MAX WATCH TIME", "MODULE 02")
    c1, c2 = st.columns([2, 1])
    with c1:
        topic = st.text_input("VIDEO TOPIC", value=st.session_state.get("last_topic", ""), placeholder="e.g. 5 AI tools that replaced my team", key="script_topic")
    with c2:
        duration = st.selectbox("DURATION", ["30 seconds", "45 seconds", "60 seconds", "90 seconds"], index=2, key="script_dur")
    ph = {"English": "e.g. I was broke - then I discovered this...", "Roman Urdu": "e.g. Doston, mera account zero tha - phir ye hua...", "Pure Urdu": "e.g. Dosto, sab kuch badal gaya..."}
    hook_input = st.text_area("OPENING HOOK", placeholder=ph[selected_lang], height=80, key="script_hook")
    if st.button("GENERATE FULL SCRIPT", key="gen_script", use_container_width=True):
        if not api_key:
            st.error("Please enter your Gemini API Key in the sidebar first.")
        elif not topic.strip():
            st.warning("Please enter a video topic.")
        elif not hook_input.strip():
            st.warning("Please add an opening hook.")
        else:
            dur_s = int(duration.split()[0])
            spin = {"English": "Writing your viral script...", "Roman Urdu": "Script likh raha hai...", "Pure Urdu": "Script tayar ho rahi hai..."}
            with st.spinner(spin[selected_lang]):
                result = get_gemini_response(api_key, build_script_prompt(topic, hook_input, platform, dur_s, lang_cfg))
            st.markdown("---")
            st.markdown("<div style='display:flex;gap:0.7rem;align-items:center;flex-wrap:wrap;margin-bottom:1rem;'><span class='badge-cyan'>SCRIPT READY</span><span class='badge-purple'>" + duration.upper() + "</span>" + lang_badge() + "</div>", unsafe_allow_html=True)
            fmt = result
            cues = {
                "[VISUAL CUE]": "<span style='color:#00e5ff;font-family:Share Tech Mono,monospace;font-size:0.78rem;'>[VISUAL CUE]</span>",
                "[SOUND CUE]": "<span style='color:#ff2d78;font-family:Share Tech Mono,monospace;font-size:0.78rem;'>[SOUND CUE]</span>",
                "[MUSIC]": "<span style='color:#ff2d78;font-family:Share Tech Mono,monospace;font-size:0.78rem;'>[MUSIC]</span>",
                "[TEXT OVERLAY]": "<span style='color:#b14fff;font-family:Share Tech Mono,monospace;font-size:0.78rem;'>[TEXT OVERLAY]</span>",
                "[TRANSITION]": "<span style='color:#ffd700;font-family:Share Tech Mono,monospace;font-size:0.78rem;'>[TRANSITION]</span>",
            }
            for k, v in cues.items():
                fmt = fmt.replace(k, v)
            extra = lang_cfg["font_class"]
            st.markdown("<div class='output-block " + extra + "' style='font-size:0.95rem;line-height:2.1;'>" + fmt + "</div>", unsafe_allow_html=True)
            with st.expander("Copy Raw Script"):
                st.markdown("<div class='copy-area " + extra + "'>" + result + "</div>", unsafe_allow_html=True)

elif page == "Thumbnail":
    render_hero("THUMBNAIL ENGINEER", "MIDJOURNEY-READY PROMPTS - HIGH CTR - VIRAL VISUALS", "MODULE 03")
    if selected_lang != "English":
        st.markdown("<div style='background:rgba(0,229,255,0.05);border:1px solid rgba(0,229,255,0.2);border-radius:8px;padding:0.8rem 1rem;margin-bottom:1rem;'><span style='font-family:Share Tech Mono,monospace;font-size:0.72rem;color:#00e5ff;'>NOTE</span><br><span style='color:#b0b0c0;font-size:0.9rem;'>Image prompts stay in English for best AI results. Bilingual text overlay suggestions included.</span></div>", unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    with c1:
        topic = st.text_input("VIDEO TOPIC", value=st.session_state.get("last_topic", ""), placeholder="e.g. How I lost 20 pounds in 60 days", key="thumb_topic")
    with c2:
        thumb_style = st.selectbox("VISUAL STYLE", ["Hyper-Realistic Photography", "Cinematic and Dramatic", "Bold Graphic Text-Heavy", "Minimalist and Clean", "Explosive and Action-Packed"], key="thumb_style")
    if st.button("GENERATE THUMBNAIL PROMPTS", key="gen_thumb", use_container_width=True):
        if not api_key:
            st.error("Please enter your Gemini API Key in the sidebar first.")
        elif not topic.strip():
            st.warning("Please enter a video topic.")
        else:
            with st.spinner("Engineering viral thumbnail concepts..."):
                result = get_gemini_response(api_key, build_thumbnail_prompt(topic, platform, thumb_style, lang_cfg))
            st.markdown("---")
            st.markdown("<div style='display:flex;gap:0.7rem;align-items:center;flex-wrap:wrap;margin-bottom:1rem;'><span class='badge-cyan'>3 PROMPTS READY</span><span class='badge-purple'>" + thumb_style.upper() + "</span>" + lang_badge() + "</div>", unsafe_allow_html=True)
            prompt_blocks, negative_block, current = [], "", []
            for line in result.split("\n"):
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
                st.markdown("<div class='output-block' style='border-left-color:" + c + ";'><span class='hook-number' style='color:" + c + ";'>THUMBNAIL PROMPT " + str(i + 1) + "</span>" + block.strip() + "</div>", unsafe_allow_html=True)
            if negative_block.strip():
                st.markdown("<div class='output-block' style='border-left-color:#ff2d78;background:rgba(255,45,120,0.04);'><span class='hook-number' style='color:#ff2d78;'>NEGATIVE PROMPTS</span>" + negative_block.strip() + "</div>", unsafe_allow_html=True)
            st.markdown("<div style='margin-top:0.8rem;padding:0.8rem 1rem;background:rgba(0,229,255,0.05);border-radius:8px;border:1px solid rgba(0,229,255,0.15);'><span style='color:#00e5ff;font-size:0.73rem;'>PRO TIP: </span><span style='color:#7a7a9a;font-size:0.88rem;'>Paste into Midjourney with /imagine or DALL-E 3. Use AR 16:9 for thumbnails.</span></div>", unsafe_allow_html=True)

elif page == "SEO":
    render_hero("SMART SEO AND TAGS", "ALGORITHM OPTIMIZED - HASHTAG STRATEGY - MAXIMUM REACH", "MODULE 04")
    c1, c2 = st.columns([2, 1])
    with c1:
        topic = st.text_input("VIDEO TOPIC", value=st.session_state.get("last_topic", ""), placeholder="e.g. Passive income ideas for beginners", key="seo_topic")
    with c2:
        niche = st.selectbox("CONTENT NICHE", ["Finance and Money", "Fitness and Health", "Tech and AI", "Business and Entrepreneurship", "Lifestyle and Vlogs", "Food and Cooking", "Fashion and Beauty", "Gaming", "Education and How-To", "Travel and Adventure"], key="seo_niche")
    if st.button("GENERATE SEO PACKAGE", key="gen_seo", use_container_width=True):
        if not api_key:
            st.error("Please enter your Gemini API Key in the sidebar first.")
        elif not topic.strip():
            st.warning("Please enter a video topic.")
        else:
            spin = {"English": "Generating SEO package...", "Roman Urdu": "SEO bana raha hai...", "Pure Urdu": "SEO tayar ho raha hai..."}
            with st.spinner(spin[selected_lang]):
                result = get_gemini_response(api_key, build_seo_prompt(topic, platform, niche, lang_cfg))
            st.markdown("---")
            st.markdown("<div style='display:flex;gap:0.7rem;align-items:center;flex-wrap:wrap;margin-bottom:1.1rem;'><span class='badge-cyan'>SEO READY</span><span class='badge-purple'>" + niche.upper() + "</span>" + lang_badge() + "</div>", unsafe_allow_html=True)
            sections, current_section = {}, "other"
            sections[current_section] = []
            section_map = {"VIDEO TITLE": "titles", "OPTIMIZED DESCRIPTION": "description", "HASHTAG STRATEGY": "hashtags", "KEYWORD DENSITY": "keywords", "BEST POSTING TIMES": "timing", "ENGAGEMENT BAIT": "bait"}
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
            extra = lang_cfg["font_class"]
            def render_sec(title, content, bc):
                body = "\n".join(content).strip()
                if body:
                    st.markdown("<div class='output-block " + extra + "' style='border-left-color:" + bc + ";'><span class='hook-number' style='color:" + bc + ";direction:ltr;text-align:left;'>" + title + "</span>" + body + "</div>", unsafe_allow_html=True)
            render_sec("VIDEO TITLE OPTIONS", sections.get("titles", []), "#00e5ff")
            render_sec("OPTIMIZED DESCRIPTION", sections.get("description", []), "#b14fff")
            render_sec("HASHTAG STRATEGY", sections.get("hashtags", []), "#b14fff")
            hashtag_text = "\n".join(sections.get("hashtags", []))
            tags = [w for w in hashtag_text.split() if w.startswith("#") and len(w) > 2]
            if tags:
                pills = "".join("<span class='tag-pill'>" + t + "</span>" for t in tags)
                st.markdown("<div style='margin:0.4rem 0 1rem;padding:1rem;background:#0d0d1f;border-radius:8px;border:1px solid rgba(177,79,255,0.25);'><div style='font-family:Share Tech Mono,monospace;font-size:0.7rem;color:#7a7a9a;margin-bottom:0.7rem;direction:ltr;'>ALL HASHTAGS</div><div style='direction:ltr;text-align:left;'>" + pills + "</div></div>", unsafe_allow_html=True)
            render_sec("KEYWORD TARGETS", sections.get("keywords", []), "#00e5ff")
            render_sec("BEST POSTING TIMES", sections.get("timing", []), "#ff2d78")
            render_sec("ENGAGEMENT BAIT", sections.get("bait", []), "#b14fff")
            with st.expander("Copy Full Output"):
                st.markdown("<div class='copy-area " + extra + "'>" + result + "</div>", unsafe_allow_html=True)
