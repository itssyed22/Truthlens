import streamlit as st
import json
import re
from pathlib import Path
from agent.coordinator import check_news

# ── Page Config ──
st.set_page_config(
    page_title="TruthLens",
    page_icon="🔍",
    layout="centered"
)

# ── Load CSS ──
def load_css(path):
    with open(path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css(Path("static/style.css"))

# ── Background Orbs ──
st.markdown("""
<div class="tl-orb tl-orb-1"></div>
<div class="tl-orb tl-orb-2"></div>
<div class="tl-orb tl-orb-3"></div>
""", unsafe_allow_html=True)

# ── Navbar ──
st.markdown("""
<div class="tl-nav">
    <div class="tl-logo">Truth<em>Lens</em></div>
    <div class="tl-nav-links">
        <a class="tl-nav-link active" href="#">Platform</a>
        <a class="tl-nav-link" href="#">Intelligence</a>
        <a class="tl-nav-link" href="#">Network</a>
    </div>
    <a class="tl-nav-btn" href="#">Console</a>
</div>
""", unsafe_allow_html=True)

# ── Hero Section ──
st.markdown("""
<div class="tl-hero">
    <div class="tl-badge">
        <div class="tl-badge-dot"></div>
        Production Active · v2.4
    </div>
    <h1 class="tl-title">
        Decode Claims.<br>
        <span class="tl-title-grad">Expose Reality.</span>
    </h1>
    <p class="tl-subtitle">
        Agentic AI engine that audits media claims, maps consensus streams,
        and delivers real-time truth verdicts.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Input Field ──
headline = st.text_area(
    "",
    height=115,
    placeholder="Paste any news headline or statement here...",
    label_visibility="collapsed"
)

# ── Analyze Button ──
analyze = st.button("⚡  Analyze Statement")

# ── Shimmer Divider ──
st.markdown('<div class="tl-shimmer"></div>', unsafe_allow_html=True)

# ── Stats Strip ──
st.markdown("""
<div class="tl-stats">
    <div class="tl-stat">
        <div class="tl-stat-val">100+</div>
        <div class="tl-stat-lbl">Audits Run</div>
    </div>
    <div class="tl-stat">
        <div class="tl-stat-val">40ms</div>
        <div class="tl-stat-lbl">Avg Latency</div>
    </div>
    <div class="tl-stat">
        <div class="tl-stat-val">99.4%</div>
        <div class="tl-stat-lbl">Accuracy Index</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Analysis Logic ──
if analyze:
    if not headline.strip():
        st.warning("Please enter a statement to analyze.")
    else:
        with st.spinner("Scanning claim signature..."):
            raw = check_news(headline)

        try:
            json_match = re.search(r'\{.*\}', raw, re.DOTALL)
            data = json.loads(json_match.group()) if json_match else json.loads(raw)

            score   = int(data.get("credibility_score", 50))
            verdict = str(data.get("verdict", "UNVERIFIED")).upper().strip()
            claims  = data.get("claims", [])
            reason  = data.get("reasoning", "")
            evidence = data.get("evidence", "")

            # Ring math: circumference of r=55 circle = 2π×55 ≈ 345.4
            circumference = 345.4
            dash_offset   = circumference - (score / 100) * circumference

            if score >= 75:
                ring_color = "#34d399"
            elif score >= 45:
                ring_color = "#fbbf24"
            else:
                ring_color = "#f87171"

            # ── Score + Verdict Cards ──
            score_card = f"""
            <div class="tl-glass">
                <div class="tl-card-label">Credibility Score</div>
                <div class="tl-ring-wrap">
                    <svg width="130" height="130" viewBox="0 0 130 130">
                        <circle class="tl-ring-track" cx="65" cy="65" r="55"/>
                        <circle class="tl-ring-fill"
                            cx="65" cy="65" r="55"
                            stroke="{ring_color}"
                            stroke-dashoffset="{dash_offset}"
                        />
                    </svg>
                    <div class="tl-ring-center">
                        <div class="tl-ring-num">{score}</div>
                        <div class="tl-ring-sub">Index</div>
                    </div>
                </div>
            </div>
            """

            verdict_card = f"""
            <div class="tl-glass">
                <div class="tl-card-label">Verdict</div>
                <div class="tl-verdict-box vt-{verdict}">
                    <div class="tl-verdict-word">{verdict}</div>
                    <div class="tl-verdict-pill">Scan Complete</div>
                </div>
            </div>
            """

            st.markdown(f"""
            <div class="tl-result-row">
                <div class="tl-result-col">{score_card}</div>
                <div class="tl-result-col">{verdict_card}</div>
            </div>
            """, unsafe_allow_html=True)

            # ── Claims Panel ──
            if claims:
                claim_rows = "".join(
                    f'<div class="tl-claim-row">'
                    f'<div class="tl-claim-bullet"></div>'
                    f'<div>{c}</div>'
                    f'</div>'
                    for c in claims
                )
                st.markdown(f"""
                <div class="tl-panel">
                    <div class="tl-panel-head">
                        <div class="tl-panel-dot"></div>
                        Key Claims Identified
                    </div>
                    {claim_rows}
                </div>
                """, unsafe_allow_html=True)

            # ── Reasoning Panel ──
            if reason:
                st.markdown(f"""
                <div class="tl-panel">
                    <div class="tl-panel-head">
                        <div class="tl-panel-dot"></div>
                        Reasoning
                    </div>
                    <div class="tl-body-text">{reason}</div>
                </div>
                """, unsafe_allow_html=True)

            # ── Evidence Expander ──
            if evidence:
                with st.expander("Evidence Notes"):
                    st.markdown(
                        f'<div class="tl-mono-text">{evidence}</div>',
                        unsafe_allow_html=True
                    )

        except Exception:
            st.markdown(f"""
            <div class="tl-panel">
                <div class="tl-panel-head">
                    <div class="tl-panel-dot"></div>
                    Raw Output
                </div>
                <div class="tl-mono-text">{raw}</div>
            </div>
            """, unsafe_allow_html=True)