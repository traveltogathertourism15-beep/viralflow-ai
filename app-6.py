import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="ViralFlow AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    "<style>"
    "@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&family=Share+Tech+Mono&display=swap');"
    ":root{--p:#b14fff;--c:#00e5ff;--g:#ffd700;--bg:#050510;--card:#0d0d1f;--input:#0a0a1a;--muted:#7a7a9a;--txt:#e8e8ff;}"
    "html,body,[data-testid=stAppViewContainer]{background:#050510!important;color:#e8e8ff!important;font-family:Rajdhani,sans-serif!important;}"
    "[data-testid=stSidebar]{background:linear-gradient(180deg,#07071a,#0d0d25)!important;border-right:1px solid rgba(177,79,255,.25)!important;}"
    "[data-testid=stSidebar] *{color:#fff!important;}"
    "#MainMenu,footer,header{visibility:hidden;}"
    "[data-testid=stButton]>button{background:linear-gradient(135deg,#b14fff,#6a00cc)!important;color:#fff!important;border:none!important;border-radius:8px!important;font-family:Orbitron,sans-serif!important;font-size:.75rem!important;font-weight:700!important;letter-spacing:.14em!important;padding:.65rem 1.6rem!important;text-transform:uppercase!important;box-shadow:0 0 20px rgba(177,79,255,.4)!important;cursor:pointer!important;pointer-events:auto!important;z-index:10!important;position:relative!important;}"
    "[data-testid=stButton]>button:hover{background:linear-gradient(135deg,#c96fff,#b14fff)!important;box-shadow:0 0 35px rgba(177,79,255,.75)!important;}"
    "[data-testid=stTextInput] input,[data-testid=stTextArea] textarea{background:#0a0a1a!important;border:1px solid rgba(177,79,255,.3)!important;color:#e8e8ff!important;border-radius:8px!important;font-size:1rem!important;}"
    "[data-testid=stTextInput] input:focus,[data-testid=stTextArea] textarea:focus{border-color:#00e5ff!important;outline:none!important;}"
    "[data-testid=stTextInput] label,[data-testid=stTextArea] label,[data-testid=stSelectbox] label{color:#7a7a9a!important;font-family:Share Tech Mono,monospace!important;font-size:.75rem!important;letter-spacing:.18em!important;text-transform:uppercase!important;}"
    "[data-testid=stSelectbox]>div>div{background:#0a0a1a!important;color:#e8e8ff!important;border:1px solid rgba(177,79,255,.3)!important;}"
    ".ncard{background:#0d0d1f;border:1px solid rgba(177,79,255,.25);border-radius:12px;padding:1.4rem;margin:.7rem 0;position:relative;overflow:hidden;}"
    ".ncard::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#b14fff,#00e5ff);}"
    ".htitle{font-family:Orbitron,sans-serif;font-size:clamp(1.6rem,5vw,3.5rem);font-weight:900;background:linear-gradient(90deg,#b14fff,#00e5ff,#b14fff);background-size:200%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;animation:sh 3s linear infinite;margin:0;text-align:center;}"
    "@keyframes sh{0%{background-position:0%}100%{background-position:200%}}"
    ".hsub{font-family:Share Tech Mono,monospace;color:#00e5ff;font-size:.8rem;letter-spacing:.25em;opacity:.8;text-align:center;margin:.5rem 0;}"
    ".hdiv{height:2px;background:linear-gradient(90deg,transparent,#b14fff,#00e5ff,transparent);margin:1.2rem auto;max-width:500px;}"
    ".oblock{background:#08081c;border:1px solid rgba(0,229,255,.2);border-left:3px solid #00e5ff;border-radius:8px;padding:1.1rem 1.3rem;margin:.6rem 0;color:#e8e8ff;line-height:1.9;white-space:pre-wrap;word-break:break-word;}"
    ".pill{display:inline-block;background:rgba(177,79,255,.12);border:1px solid rgba(177,79,255,.35);color:#b14fff;border-radius:20px;padding:.2rem .75rem;margin:.2rem;font-size:.76rem;}"
    ".bc{display:inline-block;border-radius:4px;padding:.12rem .6rem;font-family:Share Tech Mono,monospace;font-size:.7rem;text-transform:uppercase;letter-spacing:.12em;}"
    ".bp{background:rgba(177,79,255,.15);border:1px solid #b14fff;color:#b14fff;}"
    ".bcy{background:rgba(0,229,255,.1);border:1px solid #00e5ff;color:#00e5ff;}"
    ".bg{background:rgba(255,215,0,.1);border:1px solid #ffd700;color:#ffd700;}"
    ".mrow{display:flex;gap:.7rem;flex-wrap:wrap;margin:.8rem 0;}"
    ".mbox{flex:1;min-width:75px;background:#0d0d1f;border:1px solid rgba(177,79,255,.25);border-radius:10px;padding:.8rem;text-align:center;}"
    ".mv{font-family:Orbitron,sans-serif;font-size:1.5rem;font-weight:700;background:linear-gradient(90deg,#b14fff,#00e5ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}"
    ".ml{font-size:.62rem;color:#7a7a9a;letter-spacing:.1em;text-transform:uppercase;margin-top:.15rem;font-family:Share Tech Mono,monospace;}"
    "[data-testid=stExpander]{border:1px solid rgba(177,79,255,.25)!important;border-radius:8px!important;background:#0d0d1f!important;}"
    "::-webkit-scrollbar{width:5px;} ::-webkit-scrollbar-thumb{background:#b14fff;border-radius:3px;}"
    "@media(max-width:768px){.htitle{font-size:1.5rem!important;}}"
    "</style>",
    unsafe_allow_html=True
)

LANGS = {
    "English": {
        "code": "en", "flag": "EN", "label": "ENGLISH", "urdu": False,
        "ins": "Write all output in clear high-energy English for viral short-form content.",
        "hfla": "Use powerful English words action verbs and punchy sentences.",
        "seo": "All titles descriptions and hashtags in English.",
    },
    "Roman Urdu": {
        "code": "ru", "flag": "PK", "label": "ROMAN URDU", "urdu": False,
        "ins": "Write all output in ROMAN URDU. Trendy conversational style used by Pakistani and Indian TikTok creators. Urdu words in English letters. Use: Doston Zabardast Kamaal Yaar Bhai Sun lo Sach bolunga Ekdum fire Viral ho gaya Game changer Seedha baat.",
        "hfla": "Start with Doston, or Yaar sun lo, or Bhai ek second ruko, or Sach bolunga,",
        "seo": "Titles and descriptions in Roman Urdu mixed English. Hashtags in English characters only.",
    },
    "Pure Urdu": {
        "code": "pu", "flag": "PK", "label": "URDU SCRIPT", "urdu": True,
        "ins": "Write ALL output in PURE URDU SCRIPT only. Grammatically correct professional Urdu. Every sentence in authentic Urdu script.",
        "hfla": "Address audience with dosto or yaaro, use Urdu idioms, short punchy sentences.",
        "seo": "Titles and descriptions in Urdu script. Hashtags with Urdu plus Roman in brackets.",
    },
}

def ai(key, prompt):
    try:
        genai.configure(api_key=key)
        m = genai.GenerativeModel("gemini-1.5-flash")
        return m.generate_content(prompt).text
    except Exception as e:
        return "Error: " + str(e)

def hook_p(topic, plat, style, L):
    return "\n".join([
        "You are a viral content strategist.",
        "LANGUAGE: " + L["ins"] + " " + L["hfla"],
        "Create EXACTLY 5 hooks for: " + topic,
        "Platform: " + plat + " Style: " + style,
        "Use: 1.Curiosity 2.Shock 3.Controversy 4.FOMO 5.Relatability",
        "Format:",
        "HOOK 1 | [TRIGGER]",
        "[Hook in required language - max 2 sentences]",
        "HOOK 2 | [TRIGGER]",
        "[Hook text]",
        "HOOK 3 | [TRIGGER]",
        "[Hook text]",
        "HOOK 4 | [TRIGGER]",
        "[Hook text]",
        "HOOK 5 | [TRIGGER]",
        "[Hook text]",
        "No hashtags. Max 2 sentences each.",
    ])

def script_p(topic, hook, plat, dur, L):
    d, d2 = str(dur), str(dur - 10)
    return "\n".join([
        "You are a viral scriptwriter.",
        "LANGUAGE: " + L["ins"],
        "Write a " + d + " second script.",
        "Topic: " + topic + " Hook: " + hook + " Platform: " + plat,
        "Spoken dialogue in required language. Keep [VISUAL CUE] [SOUND CUE] in English.",
        "[HOOK 0-3s] {opening hook}",
        "[VISUAL CUE]: {screen} [SOUND CUE]: {music}",
        "[BODY 3-" + d2 + "s] {punchy sentences}",
        "[VISUAL CUE]: {broll} [TRANSITION]: {cut}",
        "[CTA " + d2 + "-" + d + "s] {call to action}",
        "[TEXT OVERLAY]: {onscreen text}",
        "Min 4 visual cues 2 sound cues 1 text overlay.",
    ])

def thumb_p(topic, plat, style, L):
    extra = "Also add TEXT OVERLAY in " + L["label"] + " for each." if L["code"] != "en" else ""
    return "\n".join([
        "You are a thumbnail designer.",
        "Topic: " + topic + " Platform: " + plat + " Style: " + style,
        extra,
        "Generate 3 detailed image prompts in ENGLISH.",
        "PROMPT 1 | [STYLE]",
        "[Detailed prompt: subject expression colors lighting composition 8K quality]",
        "PROMPT 2 | [STYLE]",
        "[Detailed prompt]",
        "PROMPT 3 | [STYLE]",
        "[Detailed prompt]",
        "NEGATIVE PROMPTS:",
        "[What to exclude]",
    ])

def seo_p(topic, plat, niche, L):
    return "\n".join([
        "You are a viral SEO expert.",
        "LANGUAGE: " + L["ins"] + " " + L["seo"],
        "Topic: " + topic + " Platform: " + plat + " Niche: " + niche,
        "VIDEO TITLE OPTIONS:",
        "Title 1: [title] Title 2: [title] Title 3: [question title]",
        "OPTIMIZED DESCRIPTION:",
        "[150-200 words in required language]",
        "HASHTAG STRATEGY:",
        "MEGA TAGS (3): #tag #tag #tag",
        "VIRAL TAGS (5): #tag #tag #tag #tag #tag",
        "NICHE TAGS (8): #tag #tag #tag #tag #tag #tag #tag #tag",
        "MICRO TAGS (4): #tag #tag #tag #tag",
        "KEYWORD DENSITY TARGETS:",
        "Primary: [word] Secondary: [w1] [w2] [w3]",
        "BEST POSTING TIMES for " + plat + ":",
        "[Day]: [Time] - [reason]",
        "[Day]: [Time] - [reason]",
        "ENGAGEMENT BAIT LINE:",
        "[One sentence to drive comments]",
    ])

# ── SIDEBAR ──
with st.sidebar:
    st.markdown(
        "<div style='text-align:center;padding:.8rem 0 .4rem'>"
        "<div style='font-family:Orbitron,sans-serif;font-size:1.3rem;font-weight:900;"
        "background:linear-gradient(90deg,#b14fff,#00e5ff);-webkit-background-clip:text;"
        "-webkit-text-fill-color:transparent;background-clip:text'>VIRALFLOW AI</div>"
        "<div style='font-family:Share Tech Mono,monospace;font-size:.6rem;color:#00e5ff;"
        "letter-spacing:.3em;opacity:.7;margin-top:.2rem'>CONTENT ENGINE v2.1</div>"
        "</div><hr style='border:none;height:1px;background:linear-gradient(90deg,"
        "transparent,rgba(177,79,255,.5),transparent);margin:.5rem 0 .8rem'/>",
        unsafe_allow_html=True
    )

    st.markdown("<div style='font-size:.7rem;color:#ffd700;font-family:Share Tech Mono,monospace;letter-spacing:.18em;text-transform:uppercase;margin-bottom:.3rem'>GEMINI API KEY</div>", unsafe_allow_html=True)
    api_key = st.text_input("k", type="password", placeholder="AIza...", label_visibility="collapsed")
    if api_key:
        st.markdown("<span class='bc bcy'>CONNECTED</span>", unsafe_allow_html=True)
    else:
        st.markdown("<span class='bc bp'>NOT SET</span>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:.7rem;color:#ffd700;font-family:Share Tech Mono,monospace;letter-spacing:.18em;text-transform:uppercase;margin-bottom:.3rem'>PLATFORM</div>", unsafe_allow_html=True)
    platform = st.selectbox("p", ["TikTok", "Instagram Reels", "YouTube Shorts"], label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:.7rem;color:#ffd700;font-family:Share Tech Mono,monospace;letter-spacing:.18em;text-transform:uppercase;margin-bottom:.3rem'>LANGUAGE</div>", unsafe_allow_html=True)
    sel = st.selectbox("l", list(LANGS.keys()), label_visibility="collapsed", key="sel_lang")
    L = LANGS[sel]

    info = {"English": "Global reach - High energy English", "Roman Urdu": "Pakistani TikTok slang style", "Pure Urdu": "Professional Urdu script"}
    st.markdown("<div style='background:rgba(255,215,0,.06);border:1px solid rgba(255,215,0,.2);border-radius:8px;padding:.5rem .8rem;margin-top:.4rem;color:#ffd700;font-size:.88rem'>" + info[sel] + "</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:.7rem;color:#ffd700;font-family:Share Tech Mono,monospace;letter-spacing:.2em;text-transform:uppercase;margin-bottom:.4rem'>NAVIGATE</div>", unsafe_allow_html=True)

    if "pg" not in st.session_state:
        st.session_state.pg = "Home"

    nav = {"🏠 Home": "Home", "🪝 Hook Architect": "Hooks", "📜 Script Writer": "Script", "🖼 Thumbnail": "Thumb", "🔖 SEO and Tags": "SEO"}
    for lbl, val in nav.items():
        if st.button(lbl, key="n_" + val, use_container_width=True):
            st.session_state.pg = val

    st.markdown("<br><div style='font-size:.6rem;color:#3a3a5a;text-align:center;line-height:1.7'>ViralFlow AI v2.1<br>Gemini 1.5 Flash</div>", unsafe_allow_html=True)

pg = st.session_state.pg

def hero(title, sub, badge):
    st.markdown(
        "<div style='text-align:center;padding:2rem 1rem 1rem'>"
        "<div style='font-size:.7rem;color:#b14fff;font-family:Share Tech Mono,monospace;"
        "letter-spacing:.35em;margin-bottom:.4rem'>" + badge + "</div>"
        "<h1 class='htitle'>" + title + "</h1>"
        "<div class='hsub'>" + sub + "</div>"
        "<div style='margin:.5rem 0'><span style='display:inline-flex;align-items:center;"
        "gap:.4rem;background:rgba(255,215,0,.07);border:1px solid rgba(255,215,0,.3);"
        "border-radius:20px;padding:.25rem .9rem;font-family:Share Tech Mono,monospace;"
        "font-size:.7rem;color:#ffd700;letter-spacing:.14em'>"
        "<span style='width:6px;height:6px;background:#ffd700;border-radius:50%;"
        "display:inline-block'></span>LANGUAGE: " + L["flag"] + " " + L["label"] + "</span></div>"
        "<div class='hdiv'></div></div>",
        unsafe_allow_html=True
    )

def out(content, label="", color="#00e5ff"):
    rtl = "direction:rtl;text-align:right;font-family:serif;font-size:1.1rem;line-height:2.1;" if L["urdu"] else ""
    lbl = "<span style='font-size:.68rem;letter-spacing:.2em;display:block;margin-bottom:.4rem;color:" + color + ";font-family:Orbitron,sans-serif;direction:ltr;text-align:left'>" + label + "</span>" if label else ""
    st.markdown("<div class='oblock' style='border-left-color:" + color + ";" + rtl + "'>" + lbl + content + "</div>", unsafe_allow_html=True)

def lbadge():
    return "<span class='bc bg'>" + L["flag"] + " " + L["label"] + "</span>"

# ── PAGES ──

if pg == "Home":
    hero("VIRALFLOW AI", "THE CONTENT ENGINE FOR CREATORS WHO DOMINATE", "AI POWERED - MULTILINGUAL - VIRAL OPTIMIZED")
    st.markdown(
        "<div class='mrow'>"
        "<div class='mbox'><div class='mv'>5x</div><div class='ml'>Hooks</div></div>"
        "<div class='mbox'><div class='mv'>60s</div><div class='ml'>Scripts</div></div>"
        "<div class='mbox'><div class='mv'>3x</div><div class='ml'>Thumbs</div></div>"
        "<div class='mbox'><div class='mv'>20+</div><div class='ml'>Tags</div></div>"
        "<div class='mbox'><div class='mv'>3</div><div class='ml'>Langs</div></div>"
        "</div>", unsafe_allow_html=True
    )
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='ncard'><div style='font-family:Orbitron,sans-serif;font-size:1rem;color:#00e5ff;margin-bottom:.4rem'>HOOK ARCHITECT</div><div style='color:#7a7a9a;font-size:.93rem'>5 psychology hooks using Curiosity FOMO Shock Controversy and Relatability in your language.</div><br><span class='bc bp'>PSYCHOLOGY</span></div>", unsafe_allow_html=True)
        st.markdown("<div class='ncard'><div style='font-family:Orbitron,sans-serif;font-size:1rem;color:#00e5ff;margin-bottom:.4rem'>THUMBNAIL ENGINEER</div><div style='color:#7a7a9a;font-size:.93rem'>3 Midjourney and DALL-E ready prompts with bilingual text overlay suggestions.</div><br><span class='bc bcy'>MIDJOURNEY</span></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='ncard'><div style='font-family:Orbitron,sans-serif;font-size:1rem;color:#00e5ff;margin-bottom:.4rem'>SCRIPTWRITER</div><div style='color:#7a7a9a;font-size:.93rem'>Full scripts with visual cues B-roll sound directions and strong CTA in your language.</div><br><span class='bc bp'>VISUAL CUES</span></div>", unsafe_allow_html=True)
        st.markdown("<div class='ncard'><div style='font-family:Orbitron,sans-serif;font-size:1rem;color:#00e5ff;margin-bottom:.4rem'>SMART SEO</div><div style='color:#7a7a9a;font-size:.93rem'>Tiered hashtags SEO titles keyword descriptions and best posting times.</div><br><span class='bc bcy'>ALGORITHM</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='ncard' style='border-color:rgba(0,229,255,.2)'><div style='font-family:Orbitron,sans-serif;font-size:1rem;color:#00e5ff;margin-bottom:.8rem'>QUICK START</div><div style='color:#b0b0c0;font-size:.96rem;line-height:2'><b style='color:#00e5ff'>1.</b> Enter Gemini API Key - free at aistudio.google.com<br><b style='color:#00e5ff'>2.</b> Pick Platform and Language in sidebar<br><b style='color:#00e5ff'>3.</b> Click any tool in navigation<br><b style='color:#00e5ff'>4.</b> Enter your topic and hit GENERATE</div></div>", unsafe_allow_html=True)

elif pg == "Hooks":
    hero("HOOK ARCHITECT", "STOP THE SCROLL - TRIGGER PSYCHOLOGY - CAPTURE ATTENTION", "MODULE 01")
    c1, c2 = st.columns([2, 1])
    with c1:
        topic = st.text_input("VIDEO TOPIC", placeholder="e.g. How I made money with AI tools", key="h_topic")
    with c2:
        style = st.selectbox("HOOK STYLE", ["Aggressive Bold", "Mysterious Intriguing", "Relatable Personal", "Controversial Edgy", "Educational Shocking"], key="h_style")
    if st.button("GENERATE 5 HOOKS", key="b_hooks", use_container_width=True):
        if not api_key:
            st.error("Enter Gemini API Key in sidebar first.")
        elif not topic.strip():
            st.warning("Enter a video topic.")
        else:
            sp = {"English": "Generating hooks...", "Roman Urdu": "Zabardast hooks bana raha hai...", "Pure Urdu": "Hooks tayar ho rahi hain..."}
            with st.spinner(sp[sel]):
                res = ai(api_key, hook_p(topic, platform, style, L))
            st.markdown("---")
            st.markdown("<div style='display:flex;gap:.6rem;flex-wrap:wrap;margin-bottom:.8rem'><span class='bc bcy'>GENERATED</span><span class='bc bp'>" + platform.upper() + "</span>" + lbadge() + "</div>", unsafe_allow_html=True)
            cur, num = [], 0
            clrs = ["#b14fff", "#00e5ff", "#ff2d78", "#b14fff", "#00e5ff"]
            for line in res.strip().split("\n"):
                if line.strip().startswith("HOOK "):
                    if cur:
                        out("\n".join(cur).strip(), "HOOK " + str(num), clrs[(num - 1) % 5])
                        cur = []
                    num += 1
                    cur.append(line)
                else:
                    cur.append(line)
            if cur:
                out("\n".join(cur).strip(), "HOOK " + str(num), clrs[(num - 1) % 5])
            st.session_state["ltopic"] = topic
            st.info("Go to Script Writer to turn your best hook into a full script!")

elif pg == "Script":
    hero("60-SEC SCRIPTWRITER", "RETENTION OPTIMIZED - VISUAL CUES - MAX WATCH TIME", "MODULE 02")
    c1, c2 = st.columns([2, 1])
    with c1:
        topic = st.text_input("VIDEO TOPIC", value=st.session_state.get("ltopic", ""), placeholder="e.g. 5 AI tools that changed everything", key="s_topic")
    with c2:
        dur = st.selectbox("DURATION", ["30 seconds", "45 seconds", "60 seconds", "90 seconds"], index=2, key="s_dur")
    ph = {"English": "I was broke then I discovered this...", "Roman Urdu": "Doston mera account zero tha phir ye hua...", "Pure Urdu": "Dosto sab kuch badal gaya..."}
    hook_in = st.text_area("OPENING HOOK", placeholder=ph[sel], height=75, key="s_hook")
    if st.button("GENERATE FULL SCRIPT", key="b_script", use_container_width=True):
        if not api_key:
            st.error("Enter Gemini API Key in sidebar first.")
        elif not topic.strip():
            st.warning("Enter a video topic.")
        elif not hook_in.strip():
            st.warning("Add an opening hook.")
        else:
            ds = int(dur.split()[0])
            sp = {"English": "Writing script...", "Roman Urdu": "Script likh raha hai...", "Pure Urdu": "Script tayar ho rahi hai..."}
            with st.spinner(sp[sel]):
                res = ai(api_key, script_p(topic, hook_in, platform, ds, L))
            st.markdown("---")
            st.markdown("<div style='display:flex;gap:.6rem;flex-wrap:wrap;margin-bottom:.8rem'><span class='bc bcy'>SCRIPT READY</span><span class='bc bp'>" + dur.upper() + "</span>" + lbadge() + "</div>", unsafe_allow_html=True)
            fmt = res
            for k, col in [("[VISUAL CUE]", "#00e5ff"), ("[SOUND CUE]", "#ff2d78"), ("[MUSIC]", "#ff2d78"), ("[TEXT OVERLAY]", "#b14fff"), ("[TRANSITION]", "#ffd700")]:
                fmt = fmt.replace(k, "<span style='color:" + col + ";font-family:Share Tech Mono,monospace;font-size:.78rem'>" + k + "</span>")
            rtl = "direction:rtl;text-align:right;font-family:serif;font-size:1.1rem;" if L["urdu"] else ""
            st.markdown("<div class='oblock' style='font-size:.94rem;line-height:2;" + rtl + "'>" + fmt + "</div>", unsafe_allow_html=True)
            with st.expander("Copy Raw Script"):
                st.code(res, language=None)

elif pg == "Thumb":
    hero("THUMBNAIL ENGINEER", "MIDJOURNEY READY - HIGH CTR - VIRAL VISUALS", "MODULE 03")
    if sel != "English":
        st.info("Image prompts stay in English for best AI results. Bilingual text overlay suggestions included.")
    c1, c2 = st.columns([2, 1])
    with c1:
        topic = st.text_input("VIDEO TOPIC", value=st.session_state.get("ltopic", ""), placeholder="e.g. How I lost 20 pounds in 60 days", key="t_topic")
    with c2:
        tstyle = st.selectbox("VISUAL STYLE", ["Hyper-Realistic Photo", "Cinematic Dramatic", "Bold Graphic Text", "Minimalist Clean", "Explosive Action"], key="t_style")
    if st.button("GENERATE THUMBNAIL PROMPTS", key="b_thumb", use_container_width=True):
        if not api_key:
            st.error("Enter Gemini API Key in sidebar first.")
        elif not topic.strip():
            st.warning("Enter a video topic.")
        else:
            with st.spinner("Engineering viral thumbnails..."):
                res = ai(api_key, thumb_p(topic, platform, tstyle, L))
            st.markdown("---")
            st.markdown("<div style='display:flex;gap:.6rem;flex-wrap:wrap;margin-bottom:.8rem'><span class='bc bcy'>3 PROMPTS READY</span><span class='bc bp'>" + tstyle.upper() + "</span>" + lbadge() + "</div>", unsafe_allow_html=True)
            blocks, neg, cur = [], "", []
            for line in res.split("\n"):
                if line.startswith("PROMPT ") and cur:
                    blocks.append("\n".join(cur))
                    cur = [line]
                elif line.startswith("NEGATIVE"):
                    if cur:
                        blocks.append("\n".join(cur))
                        cur = []
                    neg = line
                elif neg:
                    neg += "\n" + line
                else:
                    cur.append(line)
            if cur:
                blocks.append("\n".join(cur))
            for i, b in enumerate(blocks[:3]):
                c = ["#b14fff", "#00e5ff", "#ff2d78"][i % 3]
                st.markdown("<div class='oblock' style='border-left-color:" + c + "'><span style='color:" + c + ";font-size:.68rem;font-family:Orbitron,sans-serif;display:block;margin-bottom:.4rem'>PROMPT " + str(i + 1) + "</span>" + b.strip() + "</div>", unsafe_allow_html=True)
            if neg.strip():
                st.markdown("<div class='oblock' style='border-left-color:#ff2d78;background:rgba(255,45,120,.04)'><span style='color:#ff2d78;font-size:.68rem;font-family:Orbitron,sans-serif;display:block;margin-bottom:.4rem'>NEGATIVE PROMPTS</span>" + neg.strip() + "</div>", unsafe_allow_html=True)
            st.markdown("<div style='margin-top:.8rem;padding:.8rem 1rem;background:rgba(0,229,255,.05);border-radius:8px;border:1px solid rgba(0,229,255,.15)'><span style='color:#00e5ff;font-size:.72rem'>PRO TIP: </span><span style='color:#7a7a9a;font-size:.88rem'>Paste into Midjourney with /imagine or DALL-E 3. Use AR 16:9.</span></div>", unsafe_allow_html=True)

elif pg == "SEO":
    hero("SMART SEO AND TAGS", "ALGORITHM OPTIMIZED - HASHTAG STRATEGY - MAX REACH", "MODULE 04")
    c1, c2 = st.columns([2, 1])
    with c1:
        topic = st.text_input("VIDEO TOPIC", value=st.session_state.get("ltopic", ""), placeholder="e.g. Passive income for beginners", key="seo_t")
    with c2:
        niche = st.selectbox("NICHE", ["Finance Money", "Fitness Health", "Tech AI", "Business", "Lifestyle Vlogs", "Food Cooking", "Fashion Beauty", "Gaming", "Education", "Travel"], key="seo_n")
    if st.button("GENERATE SEO PACKAGE", key="b_seo", use_container_width=True):
        if not api_key:
            st.error("Enter Gemini API Key in sidebar first.")
        elif not topic.strip():
            st.warning("Enter a video topic.")
        else:
            sp = {"English": "Generating SEO package...", "Roman Urdu": "SEO bana raha hai...", "Pure Urdu": "SEO tayar ho raha hai..."}
            with st.spinner(sp[sel]):
                res = ai(api_key, seo_p(topic, platform, niche, L))
            st.markdown("---")
            st.markdown("<div style='display:flex;gap:.6rem;flex-wrap:wrap;margin-bottom:.9rem'><span class='bc bcy'>SEO READY</span><span class='bc bp'>" + niche.upper() + "</span>" + lbadge() + "</div>", unsafe_allow_html=True)
            secs, cur_s = {}, "other"
            smap = {"VIDEO TITLE": "titles", "OPTIMIZED DESCRIPTION": "desc", "HASHTAG": "tags", "KEYWORD": "kw", "POSTING TIMES": "times", "ENGAGEMENT BAIT": "bait"}
            for line in res.split("\n"):
                up = line.strip().upper()
                hit = False
                for k, v in smap.items():
                    if k in up:
                        cur_s = v
                        secs[cur_s] = []
                        hit = True
                        break
                if not hit:
                    secs.setdefault(cur_s, []).append(line)
            rtl = "direction:rtl;text-align:right;font-family:serif;font-size:1.1rem;" if L["urdu"] else ""
            def rsec(title, key, color):
                body = "\n".join(secs.get(key, [])).strip()
                if body:
                    st.markdown("<div class='oblock' style='border-left-color:" + color + ";" + rtl + "'><span style='color:" + color + ";font-size:.68rem;font-family:Orbitron,sans-serif;display:block;margin-bottom:.4rem;direction:ltr;text-align:left'>" + title + "</span>" + body + "</div>", unsafe_allow_html=True)
            rsec("VIDEO TITLE OPTIONS", "titles", "#00e5ff")
            rsec("OPTIMIZED DESCRIPTION", "desc", "#b14fff")
            rsec("HASHTAG STRATEGY", "tags", "#b14fff")
            tag_text = "\n".join(secs.get("tags", []))
            tags = [w for w in tag_text.split() if w.startswith("#") and len(w) > 2]
            if tags:
                pills = "".join("<span class='pill'>" + t + "</span>" for t in tags)
                st.markdown("<div style='padding:.8rem;background:#0d0d1f;border-radius:8px;border:1px solid rgba(177,79,255,.25);margin:.4rem 0 .9rem'><div style='font-size:.7rem;color:#7a7a9a;margin-bottom:.6rem;font-family:Share Tech Mono,monospace'>ALL HASHTAGS</div>" + pills + "</div>", unsafe_allow_html=True)
            rsec("KEYWORD TARGETS", "kw", "#00e5ff")
            rsec("BEST POSTING TIMES", "times", "#ff2d78")
            rsec("ENGAGEMENT BAIT", "bait", "#b14fff")
            with st.expander("Copy Full Output"):
                st.code(res, language=None)
