"""
╔══════════════════════════════════════════════════════════════════════════════╗
║       INTEL CORPORATION — RESEARCH TERMINAL  (Damodaran Framework)         ║
║  Forecasting · Valuation · Marketing Strategy · Live Data · Live News      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  HOW TO RUN IN VS CODE:                                                    ║
║  1. Open a terminal  (Ctrl + `)                                            ║
║  2. pip install streamlit yfinance plotly pandas numpy requests feedparser ║
║  3. streamlit run intel_terminal.py                                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

Prepared by: Aditi Ranjan  |  BBA Corporate Finance  |  March 2026
Data Sources: Intel 10-K FY2020–2024, Damodaran Framework, Yahoo Finance
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import feedparser
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Intel Research Terminal",
    page_icon="🔵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── BRAND COLOURS (Intel Corporate Palette) ───────────────────────────────────
BLUE        = "#0071C5"       # Intel primary blue
BLUE_DARK   = "#003C71"       # Intel dark navy
BLUE_LIGHT  = "#E0F0FF"       # Intel light blue tint
CYAN        = "#00A4EF"       # Intel secondary cyan
CYAN_LIGHT  = "#E0F7FF"       # Cyan tint
STEEL       = "#4A6FA5"       # Steel blue
STEEL_LIGHT = "#EDF2FA"       # Steel tint
GOLD        = "#D68A00"       # Amber/gold for warnings
GOLD_LIGHT  = "#FFF6E0"       # Gold tint
RED         = "#C0392B"       # Error / bearish
RED_LIGHT   = "#FFECEC"       # Red tint
GREEN       = "#1B6B3A"       # Positive / bullish
GREEN_LIGHT = "#E8F5EE"       # Green tint
BG          = "#F0F4F9"       # Page background
BORDER      = "#CDD6E8"       # Card border

# ── THEME CSS ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

  body, [data-testid="stApp"] {{
    background-color: {BG};
    color: #1A1A2E;
    font-family: 'Inter', 'Segoe UI', sans-serif;
  }}
  [data-testid="stSidebar"] {{ background: {BLUE_DARK} !important; }}
  [data-testid="stSidebar"] * {{ color: #CBD5E1 !important; font-family: 'Inter', sans-serif !important; }}
  [data-testid="stSidebar"] .stRadio > label {{
    color: #94A3B8 !important; font-size: 0.72rem;
    text-transform: uppercase; letter-spacing: 1.2px;
  }}
  [data-testid="stSidebar"] .stRadio label {{ color: #E2E8F0 !important; font-size: 0.88rem; }}
  h1, h2, h3 {{ color: {BLUE_DARK} !important; font-family: 'Inter', sans-serif !important; }}

  /* ── Cards ── */
  .q-card {{
    background: #fff; border: 1px solid {BORDER};
    border-radius: 12px; padding: 1rem 1.25rem; margin-bottom: 0.9rem;
    box-shadow: 0 1px 4px rgba(0,60,113,0.07);
  }}
  .q-card-blue {{
    background: {BLUE_LIGHT}; border-left: 4px solid {BLUE};
    border-radius: 0 10px 10px 0; padding: 0.9rem 1.1rem; margin-bottom: 0.9rem;
  }}
  .q-card-cyan {{
    background: {CYAN_LIGHT}; border-left: 4px solid {CYAN};
    border-radius: 0 10px 10px 0; padding: 0.9rem 1.1rem; margin-bottom: 0.9rem;
  }}
  .q-card-steel {{
    background: {STEEL_LIGHT}; border-left: 4px solid {STEEL};
    border-radius: 0 10px 10px 0; padding: 0.9rem 1.1rem; margin-bottom: 0.9rem;
  }}
  .q-card-gold {{
    background: {GOLD_LIGHT}; border-left: 4px solid {GOLD};
    border-radius: 0 10px 10px 0; padding: 0.9rem 1.1rem; margin-bottom: 0.9rem;
  }}
  .q-card-red {{
    background: {RED_LIGHT}; border-left: 4px solid {RED};
    border-radius: 0 10px 10px 0; padding: 0.9rem 1.1rem; margin-bottom: 0.9rem;
  }}
  .q-card-green {{
    background: {GREEN_LIGHT}; border-left: 4px solid {GREEN};
    border-radius: 0 10px 10px 0; padding: 0.9rem 1.1rem; margin-bottom: 0.9rem;
  }}

  /* ── Section heading ── */
  .sec-head {{
    font-size: 0.98rem; font-weight: 700; color: {BLUE_DARK} !important;
    border-left: 4px solid {BLUE}; padding-left: 10px;
    margin: 1.4rem 0 0.8rem; letter-spacing: 0.2px;
  }}

  /* ── Narrative ── */
  .narrative {{
    background: {BLUE_LIGHT}; border-left: 3px solid {BLUE};
    border-radius: 0 8px 8px 0; padding: 0.8rem 1.1rem;
    font-style: italic; font-size: 0.89rem; line-height: 1.8;
    color: #0c2a4a; margin-bottom: 1rem;
  }}

  /* ── Pull-quote ── */
  .pullquote {{
    background: linear-gradient(135deg, {BLUE_LIGHT} 0%, {CYAN_LIGHT} 100%);
    border-left: 5px solid {BLUE}; border-right: 5px solid {CYAN};
    border-radius: 4px; padding: 0.9rem 1.4rem; margin: 1rem 1.5rem;
    font-style: italic; font-size: 0.96rem; font-weight: 500;
    color: {BLUE_DARK}; text-align: center;
  }}

  /* ── KPI card ── */
  .kpi-card {{
    background: #fff; border: 1px solid {BORDER};
    border-top: 3px solid {BLUE}; border-radius: 10px;
    padding: 0.85rem 1rem; text-align: center;
    box-shadow: 0 2px 8px rgba(0,113,197,0.08);
    transition: transform 0.15s;
  }}
  .kpi-card:hover {{ transform: translateY(-1px); }}
  .kpi-label {{ font-size: 0.67rem; color: #6B7280; text-transform: uppercase; letter-spacing: 0.9px; margin-bottom: 5px; font-weight: 600; }}
  .kpi-value {{ font-size: 1.38rem; font-weight: 800; color: {BLUE_DARK}; }}
  .kpi-sub   {{ font-size: 0.7rem; color: #6B7280; margin-top: 4px; }}

  /* ── Tags ── */
  .tag-blue  {{ background:{BLUE_LIGHT};  color:{BLUE};      padding:3px 11px; border-radius:99px; font-size:0.72rem; font-weight:700; }}
  .tag-cyan  {{ background:{CYAN_LIGHT};  color:{CYAN};      padding:3px 11px; border-radius:99px; font-size:0.72rem; font-weight:700; }}
  .tag-steel {{ background:{STEEL_LIGHT}; color:{STEEL};     padding:3px 11px; border-radius:99px; font-size:0.72rem; font-weight:700; }}
  .tag-gold  {{ background:{GOLD_LIGHT};  color:{GOLD};      padding:3px 11px; border-radius:99px; font-size:0.72rem; font-weight:700; }}
  .tag-red   {{ background:{RED_LIGHT};   color:{RED};       padding:3px 11px; border-radius:99px; font-size:0.72rem; font-weight:700; }}
  .tag-green {{ background:{GREEN_LIGHT}; color:{GREEN};     padding:3px 11px; border-radius:99px; font-size:0.72rem; font-weight:700; }}

  /* ── News ── */
  .news-pos {{ background:#F0FBF4; border-left:4px solid {GREEN};  padding:0.65rem 1rem; border-radius:0 8px 8px 0; margin-bottom:0.55rem; }}
  .news-neg {{ background:{RED_LIGHT};   border-left:4px solid {RED};   padding:0.65rem 1rem; border-radius:0 8px 8px 0; margin-bottom:0.55rem; }}
  .news-neu {{ background:{BLUE_LIGHT};  border-left:4px solid {BLUE};  padding:0.65rem 1rem; border-radius:0 8px 8px 0; margin-bottom:0.55rem; }}
  .news-title {{ font-size:0.87rem; font-weight:600; color:#1A1A2E; line-height:1.45; }}
  .news-meta  {{ font-size:0.7rem;  color:#6B7280; margin-top:4px; }}

  /* ── Ansoff ── */
  .ansoff-card {{
    background: #fff; border-radius: 10px; padding: 0.95rem 1.1rem;
    margin-bottom: 0.8rem; border: 1px solid {BORDER};
    box-shadow: 0 1px 4px rgba(0,60,113,0.05);
  }}
  .ansoff-title {{ font-size: 0.92rem; font-weight: 700; color: {BLUE_DARK}; }}
  .ansoff-sub   {{ font-size: 0.73rem; color: #6B7280; margin-bottom: 8px; }}
  .ansoff-item  {{ font-size: 0.83rem; color: #374151; margin-bottom: 4px; line-height:1.45; }}

  /* ── Fingerprint ── */
  .fp-card {{
    background: #fff; border-left: 3px solid {BLUE};
    border-radius: 0 8px 8px 0; padding: 0.65rem 1rem; margin-bottom: 0.6rem;
    box-shadow: 0 1px 3px rgba(0,113,197,0.07);
  }}
  .fp-label  {{ font-size:0.67rem; color:#6B7280; text-transform:uppercase; letter-spacing:0.5px; font-weight:600; }}
  .fp-value  {{ font-size:1.05rem; font-weight:700; color:{BLUE_DARK}; }}
  .fp-signal {{ font-size:0.72rem; color:#374151; margin-top:2px; }}

  /* ── Scenario card ── */
  .scen-card {{
    border-radius: 10px; padding: 1rem 1.1rem; margin-bottom: 0.8rem;
    border: 1px solid {BORDER};
  }}

  /* ── Dataframe ── */
  .stDataFrame td, .stDataFrame th {{ color:#1A1A2E !important; font-size:0.82rem !important; font-family:'Inter',sans-serif !important; }}
  .stDataFrame th {{ background-color:{BLUE_DARK} !important; color:white !important; font-weight:600 !important; }}
  .stDataFrame tr:nth-child(even) td {{ background-color:#F0F4F9 !important; }}

  /* ── Tabs ── */
  .stTabs [data-baseweb="tab"] {{ color:#374151 !important; font-weight:500; font-family:'Inter',sans-serif; }}
  .stTabs [aria-selected="true"] {{ color:{BLUE} !important; border-bottom-color:{BLUE} !important; font-weight:700; }}

  /* ── Slider ── */
  .stSlider label {{ color:{BLUE_DARK} !important; font-weight:500; }}
  [data-testid="stSlider"] > div > div > div > div {{ background:{BLUE} !important; }}

  /* ── Metrics ── */
  [data-testid="stMetric"] label {{ color:#6B7280 !important; font-size:0.78rem !important; }}
  [data-testid="stMetricValue"]  {{ color:{BLUE_DARK} !important; font-weight:800 !important; }}

  /* ── Buttons ── */
  [data-testid="baseButton-secondary"] {{
    background:{BLUE} !important; color:#fff !important;
    border:none !important; border-radius:8px !important;
    font-family:'Inter',sans-serif !important; font-weight:600 !important;
  }}

  /* ── Footer ── */
  .footer {{
    font-size:0.7rem; color:#9CA3AF; text-align:center;
    margin-top:2.5rem; border-top:1px solid {BORDER}; padding-top:1rem;
  }}
</style>
""", unsafe_allow_html=True)


# ── HISTORICAL DATA (FY2020–FY2024, from 10-K filings) ───────────────────────
HIST = pd.DataFrame([
    {"Year":"FY20","Revenue":77.9,"GrossM":56.0,"EBIT_M":30.4,"NI":20.9, "Capex":14.3,"FCF":17.9, "ROIC":22.0,"EBIT":23.7,"DA":12.1,"CFO":35.4},
    {"Year":"FY21","Revenue":79.0,"GrossM":55.4,"EBIT_M":24.6,"NI":19.9, "Capex":20.3,"FCF":12.1, "ROIC":17.0,"EBIT":19.5,"DA":13.8,"CFO":30.0},
    {"Year":"FY22","Revenue":63.1,"GrossM":42.6,"EBIT_M":3.7, "NI":8.0,  "Capex":24.8,"FCF":-3.1, "ROIC":4.0, "EBIT":2.3, "DA":14.9,"CFO":15.4},
    {"Year":"FY23","Revenue":54.2,"GrossM":40.0,"EBIT_M":0.1, "NI":1.7,  "Capex":25.8,"FCF":-13.5,"ROIC":0.1, "EBIT":0.1, "DA":14.5,"CFO":11.5},
    {"Year":"FY24","Revenue":53.1,"GrossM":35.1,"EBIT_M":0.0, "NI":-18.8,"Capex":23.9,"FCF":-15.7,"ROIC":0.0, "EBIT":0.0, "DA":14.9,"CFO":8.3},
])

SEGMENTS = pd.DataFrame([
    {"Segment":"CCG (Client)",         "Rev_FY24":31.9,"EBIT_FY24":7.0, "Margin_FY24":22.0,"Rev_FY23":27.4,"Description":"PC/Laptop processors; Core Ultra w/ AI NPU"},
    {"Segment":"DCAI (Data Centre/AI)","Rev_FY24":15.9,"EBIT_FY24":1.1, "Margin_FY24":7.0, "Rev_FY23":15.6,"Description":"Xeon CPUs, Gaudi AI accelerators"},
    {"Segment":"NEX (Network/Edge)",   "Rev_FY24":5.8, "EBIT_FY24":0.2, "Margin_FY24":3.0, "Rev_FY23":6.2, "Description":"Network silicon, edge compute"},
    {"Segment":"IFS (Intel Foundry)",  "Rev_FY24":4.3, "EBIT_FY24":-8.0,"Margin_FY24":-186.0,"Rev_FY23":0.0,"Description":"External foundry; 18A process; nascent"},
])

PEERS = pd.DataFrame([
    {"Company":"Intel",    "PE": 0,  "EBIT_M": 0.0, "Rev_CAGR":-7, "ROIC": 0, "PB":0.9, "Note":"Transitioning"},
    {"Company":"AMD",      "PE":45,  "EBIT_M":10.0, "Rev_CAGR":12, "ROIC": 3, "PB":3.8, "Note":"Gaining share"},
    {"Company":"NVIDIA",   "PE":55,  "EBIT_M":55.0, "Rev_CAGR":78, "ROIC":82, "PB":52,  "Note":"AI monopoly"},
    {"Company":"TSMC",     "PE":22,  "EBIT_M":42.0, "Rev_CAGR":25, "ROIC":24, "PB":7.0, "Note":"Foundry leader"},
    {"Company":"Qualcomm", "PE":15,  "EBIT_M":27.9, "Rev_CAGR": 7, "ROIC":52, "PB":6.2, "Note":"Mobile leader"},
    {"Company":"Broadcom", "PE":35,  "EBIT_M":35.0, "Rev_CAGR":20, "ROIC":18, "PB":9.5, "Note":"Diversified"},
])

BASE = {
    "revenue":53.1,"ebit":0.0,"ni":-18.8,"fcff":-15.7,
    "capex":23.9,"da":14.9,"cfo":8.3,"net_debt":17.2,
    "shares":4.29,"equity":104.0,"gross_m":35.1,
}


# ── LIVE DATA ─────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def get_live_price():
    try:
        t    = yf.Ticker("INTC")
        info = t.info
        price = float(info.get("currentPrice") or info.get("regularMarketPrice") or 22.50)
        prev  = float(info.get("previousClose") or 22.60)
        chg   = round(price - prev, 2)
        chgp  = round((chg / prev) * 100, 2) if prev else 0.0
        mktcap= info.get("marketCap", 0)
        return {
            "price":      round(price, 2),
            "change":     chg,
            "change_pct": chgp,
            "volume":     f"{info.get('volume',0)/1e6:.1f}M",
            "market_cap": f"${mktcap/1e9:.1f}B",
            "52w_high":   info.get("fiftyTwoWeekHigh", 37),
            "52w_low":    info.get("fiftyTwoWeekLow",  16),
            "pe":         round(float(info.get("trailingPE") or 0), 1),
            "pb":         round(float(info.get("priceToBook") or 0.9), 2),
            "div_yield":  round(float(info.get("dividendYield") or 0) * 100, 2),
            "beta":       round(float(info.get("beta") or 1.10), 2),
            "shares":     round(float(info.get("sharesOutstanding", 4.29e9)) / 1e9, 3),
        }
    except Exception:
        return {"price":22.50,"change":-0.10,"change_pct":-0.44,"volume":"42.1M",
                "market_cap":"~$96B","52w_high":37,"52w_low":16,"pe":0,
                "pb":0.9,"div_yield":0.0,"beta":1.10,"shares":4.29}


@st.cache_data(ttl=300)
def get_price_history(period="6mo"):
    try:
        return yf.Ticker("INTC").history(period=period)
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=600)
def get_live_news():
    items = []
    feeds = [
        "https://news.google.com/rss/search?q=Intel+Corporation+INTC+semiconductor&hl=en-US&gl=US&ceid=US:en",
        "https://news.google.com/rss/search?q=Intel+18A+foundry+earnings&hl=en-US&gl=US&ceid=US:en",
    ]
    pos_kw = ["wins","breakthrough","milestone","customer","contract","revenue","growth","18a",
              "recovery","progress","partnership","design win","foundry","upgrade","beat","ai pc"]
    neg_kw = ["loss","cut","miss","decline","delay","layoff","competition","amd","nvidia",
              "tsmc","downgrade","concern","risk","falls","drop","disappoints","below"]
    for url in feeds:
        try:
            feed = feedparser.parse(url)
            for e in feed.entries[:8]:
                title = e.get("title","")
                link  = e.get("link","#")
                dp    = e.get("published_parsed")
                date  = datetime(*dp[:6]).strftime("%d %b %Y") if dp else "—"
                tl    = title.lower()
                sent  = "neutral"
                if any(k in tl for k in pos_kw): sent = "positive"
                if any(k in tl for k in neg_kw): sent = "negative"
                if title and title not in [x["title"] for x in items]:
                    items.append({"title":title,"link":link,"date":date,"sentiment":sent})
            if len(items) >= 14: break
        except Exception:
            continue
    if not items:
        items = [
            {"title":"Intel 18A process on track for external customer tape-outs in 2026","link":"#","date":"Mar 2026","sentiment":"positive"},
            {"title":"Intel Q4 2024: Revenue $14.3B; GAAP net loss driven by non-cash impairments","link":"#","date":"Jan 2026","sentiment":"negative"},
            {"title":"US government commits $7.86B CHIPS Act funding to Intel fab expansion","link":"#","date":"Feb 2026","sentiment":"positive"},
            {"title":"Panther Lake client processor on track for H2 2025 launch","link":"#","date":"Jan 2026","sentiment":"positive"},
            {"title":"AMD gains further server CPU share in Q4 2024 enterprise refresh","link":"#","date":"Feb 2026","sentiment":"negative"},
            {"title":"Intel Foundry secures first external tape-out from unnamed partner","link":"#","date":"Mar 2026","sentiment":"positive"},
            {"title":"Gaudi 3 AI accelerator signs new enterprise customer in financial services","link":"#","date":"Feb 2026","sentiment":"positive"},
            {"title":"Intel announces further workforce restructuring; 15,000 jobs eliminated by end 2025","link":"#","date":"Nov 2025","sentiment":"negative"},
            {"title":"NVIDIA's H200 backlog stretches 18+ months; opens door for Gaudi 3","link":"#","date":"Jan 2026","sentiment":"positive"},
            {"title":"Intel Core Ultra AI PC units surpass 30M shipped globally","link":"#","date":"Mar 2026","sentiment":"positive"},
        ]
    return items[:14]


# ── DCF ENGINE ────────────────────────────────────────────────────────────────
def run_dcf(wacc, g_term, rev_cagr, ebit_margin_y5, live_price):
    """
    Intel DCF: EBIT margins ramp from ~2% (Y1) to ebit_margin_y5 (Y5).
    Revenue grows at fixed rev_cagr. WACC captures transformation risk.
    """
    base_rev  = BASE["revenue"]   # $53.1B
    tax_rate  = 0.13
    net_debt  = BASE["net_debt"]  # $17.2B
    shares    = BASE["shares"]    # 4.29B
    stc       = 0.40              # Sales-to-Capital (capex-heavy IDM)
    DA_PCT    = 0.28              # D&A ~28% revenue (high for IDM)

    # Margin path: linearly ramp from 2% (Y1) to ebit_margin_y5 (Y5)
    margin_path = [2.0 + (ebit_margin_y5 - 2.0) * i / 4 for i in range(5)]

    rows, pv_total = [], 0.0
    rev_prev = base_rev
    for i in range(5):
        rev_i    = base_rev * (1 + rev_cagr/100) ** (i+1)
        ebit_m_i = margin_path[i]
        ebit_i   = rev_i * ebit_m_i / 100
        nopat_i  = ebit_i * (1 - tax_rate)
        drv      = rev_i - rev_prev
        reinv_i  = drv / stc
        fcff_i   = nopat_i - reinv_i
        ni_i     = ebit_i * 0.87 - 1.8   # rough NI (interest ~$1.8B)
        rev_prev = rev_i
        df_      = (1 + wacc/100) ** (i+1)
        pv_i     = fcff_i / df_
        pv_total += pv_i
        rows.append({
            "Year":          f"FY{25+i}",
            "Revenue ($B)":  round(rev_i, 1),
            "EBIT Margin":   f"{ebit_m_i:.1f}%",
            "EBIT ($B)":     round(ebit_i, 2),
            "NOPAT ($B)":    round(nopat_i, 2),
            "FCFF ($B)":     round(fcff_i, 2),
            "Disc. Factor":  round(1/df_, 4),
            "PV FCFF ($B)":  round(pv_i, 2),
        })

    if wacc <= g_term:
        return None
    tv_fcff  = rows[-1]["FCFF ($B)"] * (1 + g_term/100)
    tv       = tv_fcff / ((wacc - g_term) / 100)
    pv_tv    = tv / (1 + wacc/100) ** 5
    ev       = pv_total + pv_tv
    eq_val   = ev - net_debt
    ivps     = (eq_val * 1000) / shares  # $B * 1000 / B shares = $/share  (wait, ev is in $B already)
    # Actually: ev in $B, shares in B → ivps = ev / shares (both in $B / B = $/share)
    ivps     = eq_val / shares           # $/share
    upside   = round(((ivps / live_price) - 1) * 100, 1)

    return {
        "rows":        rows,
        "pv_explicit": round(pv_total, 2),
        "pv_tv":       round(pv_tv, 2),
        "ev":          round(ev, 2),
        "eq_val":      round(eq_val, 2),
        "ivps":        round(ivps, 2),
        "upside":      upside,
        "tv_pct":      round(pv_tv / ev * 100, 1) if ev > 0 else 0,
    }


def sensitivity_table(rev_cagr, ebit_m_y5, live_price):
    wacc_vals = [7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0]
    g_vals    = [1.5, 2.0, 2.5, 3.0, 3.5]
    data = {}
    for w in wacc_vals:
        row = []
        for g in g_vals:
            r = run_dcf(w, g, rev_cagr, ebit_m_y5, live_price)
            row.append(round(r["ivps"], 1) if r else "N/A")
        data[f"WACC {w}%"] = row
    return pd.DataFrame(data, index=[f"g = {g}%" for g in g_vals])


def mc_simulation(rev_cagr, ebit_m_y5, wacc, g_term, live_price, n=1500):
    np.random.seed(42)
    intrinsics = []
    for _ in range(n):
        g_s = np.random.triangular(max(rev_cagr-4, 0), rev_cagr, rev_cagr+4)
        m_s = np.random.triangular(max(ebit_m_y5-6, 0), ebit_m_y5, ebit_m_y5+6)
        w_s = np.random.triangular(wacc-1.5, wacc, wacc+2.0)
        r   = run_dcf(w_s, g_term, g_s, m_s, live_price)
        if r: intrinsics.append(r["ivps"])
    return np.array(intrinsics)


# ── CHART HELPERS ─────────────────────────────────────────────────────────────
_L = dict(
    plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
    font=dict(color="#1A1A2E", family="Inter, Segoe UI"),
    margin=dict(l=20, r=20, t=36, b=20),
    legend=dict(orientation="h", y=1.1, font=dict(color="#374151", size=11)),
)

def rev_profile_chart():
    """Revenue, EBIT, FCF history — the wound in numbers."""
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=HIST["Year"], y=HIST["Revenue"], name="Revenue ($B)",
                         marker_color=BLUE, opacity=0.8), secondary_y=False)
    fig.add_trace(go.Scatter(x=HIST["Year"], y=HIST["EBIT_M"], name="EBIT Margin %",
                             line=dict(color=CYAN, width=2.5),
                             mode="lines+markers", marker=dict(size=8, color=CYAN)), secondary_y=True)
    fig.add_trace(go.Scatter(x=HIST["Year"], y=HIST["FCF"], name="Free Cash Flow ($B)",
                             line=dict(color=RED, width=2, dash="dot"),
                             mode="lines+markers", marker=dict(size=6, color=RED)), secondary_y=True)
    fig.add_hline(y=0, line=dict(color="#9CA3AF", width=1, dash="dash"), secondary_y=True)
    fig.update_layout(height=320, **_L,
                      yaxis=dict(tickprefix="$", ticksuffix="B", gridcolor="#F0F0F0",
                                 tickfont=dict(color="#374151")),
                      yaxis2=dict(ticksuffix="%", gridcolor="#F0F0F0",
                                  tickfont=dict(color="#374151"),
                                  title=dict(text="Margin / FCF %", font=dict(color="#374151"))))
    fig.update_xaxes(tickfont=dict(color="#374151"))
    return fig


def candlestick_chart(df):
    if df is None or df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No live data — check internet connection",
                           xref="paper", yref="paper", x=0.5, y=0.5,
                           showarrow=False, font=dict(size=14, color="#6B7280"))
        fig.update_layout(height=380, **_L)
        return fig
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=0.04, row_heights=[0.75, 0.25])
    fig.add_trace(go.Candlestick(x=df.index, open=df["Open"], high=df["High"],
                                  low=df["Low"], close=df["Close"], name="INTC",
                                  increasing_line_color=GREEN, decreasing_line_color=RED), row=1, col=1)
    ma20 = df["Close"].rolling(20).mean()
    ma50 = df["Close"].rolling(50).mean()
    fig.add_trace(go.Scatter(x=df.index, y=ma20, name="20D MA",
                             line=dict(color=CYAN, width=1.5, dash="dot")), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=ma50, name="50D MA",
                             line=dict(color=GOLD, width=1.5, dash="dash")), row=1, col=1)
    fig.add_trace(go.Bar(x=df.index, y=df["Volume"], name="Volume",
                         marker_color=BLUE, opacity=0.45), row=2, col=1)
    fig.update_layout(height=420, **_L, xaxis_rangeslider_visible=False,
                      yaxis=dict(tickprefix="$", tickfont=dict(color="#374151"), gridcolor="#F0F0F0"),
                      yaxis2=dict(tickfont=dict(color="#374151"), gridcolor="#F0F0F0"))
    fig.update_xaxes(tickfont=dict(color="#374151"))
    return fig


def capex_fcf_chart():
    fig = go.Figure()
    fig.add_trace(go.Bar(x=HIST["Year"], y=HIST["Capex"],  name="Gross Capex ($B)",
                         marker_color=BLUE, opacity=0.85))
    fig.add_trace(go.Bar(x=HIST["Year"], y=HIST["CFO"],    name="Operating Cash Flow ($B)",
                         marker_color=CYAN, opacity=0.7))
    fig.add_trace(go.Scatter(x=HIST["Year"], y=HIST["FCF"], name="Free Cash Flow ($B)",
                             line=dict(color=RED, width=2.5),
                             mode="lines+markers", marker=dict(size=8, color=RED)))
    fig.add_hline(y=0, line=dict(color="#9CA3AF", width=1, dash="dash"))
    fig.update_layout(height=310, **_L, barmode="group",
                      yaxis=dict(tickprefix="$", ticksuffix="B",
                                 gridcolor="#F0F0F0", tickfont=dict(color="#374151")),
                      xaxis=dict(tickfont=dict(color="#374151")))
    return fig


def segment_chart():
    colors = [BLUE, CYAN, STEEL, RED]
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Revenue FY24", x=SEGMENTS["Segment"],
                         y=SEGMENTS["Rev_FY24"], marker_color=BLUE, opacity=0.9))
    fig.add_trace(go.Bar(name="Revenue FY23", x=SEGMENTS["Segment"],
                         y=SEGMENTS["Rev_FY23"], marker_color=BLUE, opacity=0.4))
    fig.add_trace(go.Bar(name="EBIT FY24",    x=SEGMENTS["Segment"],
                         y=[max(e, 0) for e in SEGMENTS["EBIT_FY24"].tolist()],
                         marker_color=CYAN, opacity=0.85))
    fig.update_layout(height=310, **_L, barmode="group",
                      yaxis=dict(tickprefix="$", ticksuffix="B",
                                 gridcolor="#F0F0F0", tickfont=dict(color="#374151")),
                      xaxis=dict(tickfont=dict(color="#374151")))
    return fig


def segment_margin_chart():
    seg = SEGMENTS[SEGMENTS["Segment"] != "IFS (Intel Foundry)"].copy()
    colors = [BLUE, CYAN, STEEL]
    fig = go.Figure(go.Bar(
        x=seg["Segment"], y=seg["Margin_FY24"],
        marker_color=colors,
        text=[f"{m:.0f}%" for m in seg["Margin_FY24"]],
        textposition="outside", textfont=dict(color="#1A1A2E", size=11)
    ))
    # IFS annotation
    fig.add_annotation(x=2.7, y=-15, text="IFS: –186%\n(not shown)",
                       font=dict(color=RED, size=10), showarrow=False)
    fig.update_layout(height=290, **_L,
                      title=dict(text="EBIT Margin by Segment — FY2024 (IFS excluded for scale)",
                                 font=dict(color="#1A1A2E", size=12)),
                      yaxis=dict(ticksuffix="%", gridcolor="#F0F0F0",
                                 tickfont=dict(color="#374151")),
                      xaxis=dict(tickfont=dict(color="#374151")), showlegend=False)
    return fig


def forecast_chart(rows):
    hy = [r.replace("FY","20") for r in HIST["Year"].tolist()]  # "FY20" → "2020"
    years_h = ["2020","2021","2022","2023","2024"]
    py = [r["Year"].replace("FY","20") for r in rows]
    pr = [r["Revenue ($B)"] for r in rows]
    pe = [r["EBIT ($B)"]    for r in rows]
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=years_h, y=HIST["Revenue"].tolist(), name="Revenue (Hist.)",
                             line=dict(color=BLUE_DARK, width=2.5),
                             mode="lines+markers", marker=dict(size=6)), secondary_y=False)
    fig.add_trace(go.Scatter(x=[years_h[-1]] + py, y=[HIST["Revenue"].iloc[-1]] + pr,
                             name="Revenue (Proj.)",
                             line=dict(color=BLUE, width=2.5, dash="dash"),
                             mode="lines+markers", marker=dict(size=7, symbol="diamond")), secondary_y=False)
    fig.add_trace(go.Scatter(x=py, y=pe, name="EBIT (Proj.)",
                             line=dict(color=CYAN, width=2, dash="dash"),
                             mode="lines+markers", marker=dict(size=6, color=CYAN)), secondary_y=True)
    fig.add_vline(x="2024", line_dash="dot", line_color=GOLD,
                  annotation_text="← Actual  |  Projected →",
                  annotation_font=dict(color=GOLD, size=11),
                  annotation_position="top")
    fig.update_layout(height=360, **_L,
                      yaxis=dict(tickprefix="$", ticksuffix="B", gridcolor="#F0F0F0",
                                 tickfont=dict(color="#374151")),
                      yaxis2=dict(tickprefix="$", ticksuffix="B", gridcolor="#F0F0F0",
                                  tickfont=dict(color="#374151"),
                                  title=dict(text="EBIT ($B)", font=dict(color="#374151"))))
    fig.update_xaxes(tickfont=dict(color="#374151"))
    return fig


def dcf_bar_chart(result):
    yrs  = [r["Year"] for r in result["rows"]]
    fcff = [r["FCFF ($B)"] for r in result["rows"]]
    pvs  = [r["PV FCFF ($B)"] for r in result["rows"]]
    fig  = go.Figure()
    fig.add_trace(go.Bar(x=yrs, y=fcff, name="FCFF ($B)", marker_color=BLUE, opacity=0.85,
                         text=[f"${v:.1f}B" for v in fcff], textposition="outside",
                         textfont=dict(color="#1A1A2E", size=10)))
    fig.add_trace(go.Bar(x=yrs, y=pvs,  name="PV of FCFF ($B)", marker_color=CYAN, opacity=0.75))
    fig.add_hline(y=0, line=dict(color="#9CA3AF", width=1, dash="dash"))
    fig.update_layout(height=290, **_L, barmode="group",
                      yaxis=dict(tickprefix="$", ticksuffix="B",
                                 gridcolor="#F0F0F0", tickfont=dict(color="#374151")),
                      xaxis=dict(tickfont=dict(color="#374151")))
    return fig


def scenario_bar_chart(live_price):
    cfgs = {
        "Bull 🚀":  (8.0, 20.0, GREEN,   "18A works. Gaudi 3 traction. Foundry $6B revenue."),
        "Base 📊":  (6.0, 15.0, BLUE,    "Recovery track. Margins normalise to 14-16%."),
        "Bear 🐻":  (2.0,  8.0, RED,     "18A delays. AMD gains. Foundry earns minimal revenue."),
    }
    metrics = ["FY2029 Revenue ($B)", "FY2029 EBIT ($B)", "Intrinsic Value ($/shr)"]
    fig = go.Figure()
    for name, (rg, em, col, _) in cfgs.items():
        rv5 = BASE["revenue"] * (1 + rg/100) ** 5
        eb5 = rv5 * em / 100
        r   = run_dcf(8.0, 2.5, rg, em, live_price)
        iv  = r["ivps"] if r else 0
        vals = [round(rv5,1), round(eb5,1), round(iv,2)]
        fig.add_trace(go.Bar(name=name, x=metrics, y=vals, marker_color=col, opacity=0.85,
                             text=[f"${v}" for v in vals], textposition="outside",
                             textfont=dict(color="#1A1A2E", size=11)))
    fig.update_layout(height=310, **_L, barmode="group",
                      title=dict(text="Scenario Comparison — FY2029 Projections",
                                 font=dict(color="#1A1A2E", size=13)),
                      yaxis=dict(tickprefix="$", gridcolor="#F0F0F0",
                                 tickfont=dict(color="#374151")),
                      xaxis=dict(tickfont=dict(color="#374151", size=11)))
    return fig


def radar_chart():
    cats = ["Valuation<br>(inv. P/E)", "EBIT Margin", "Rev Growth", "ROIC", "R&D Intensity"]
    cos  = [
        ("Intel",    [55, 5,  15, 5,  85], BLUE),
        ("AMD",      [45, 20, 55, 8,  50], CYAN),
        ("NVIDIA",   [10, 100,90, 100,60], GOLD),
        ("TSMC",     [40, 84, 60, 48, 45], STEEL),
    ]
    fig = go.Figure()
    for name, vals, col in cos:
        fig.add_trace(go.Scatterpolar(
            r=vals+[vals[0]], theta=cats+[cats[0]],
            fill="toself", name=name,
            line=dict(color=col, width=2),
            fillcolor=col,
            opacity=0.22 if name != "Intel" else 0.30,
        ))
    fig.update_layout(height=340, paper_bgcolor="#FFFFFF",
                      polar=dict(
                          radialaxis=dict(visible=True, range=[0, 110],
                                          tickfont=dict(color="#9CA3AF"),
                                          gridcolor="#E5E7EB"),
                          angularaxis=dict(tickfont=dict(color="#374151", size=11))
                      ),
                      legend=dict(orientation="h", y=-0.08,
                                  font=dict(color="#374151", size=11)),
                      margin=dict(l=30, r=30, t=30, b=50),
                      font=dict(color="#1A1A2E", family="Inter"))
    return fig


def margin_recovery_chart(rows):
    yrs  = [r["Year"] for r in rows]
    mgns = [float(r["EBIT Margin"].replace("%","")) for r in rows]
    hist_y = ["FY20","FY21","FY22","FY23","FY24"]
    hist_m = HIST["EBIT_M"].tolist()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hist_y, y=hist_m, name="EBIT Margin (Hist.)",
                             line=dict(color=BLUE_DARK, width=2.5),
                             mode="lines+markers", marker=dict(size=7)))
    fig.add_trace(go.Scatter(x=[hist_y[-1]] + yrs,
                             y=[hist_m[-1]] + mgns,
                             name="EBIT Margin (Proj.)",
                             line=dict(color=BLUE, width=2.5, dash="dash"),
                             mode="lines+markers",
                             marker=dict(size=7, symbol="diamond", color=CYAN)))
    fig.add_hrect(y0=14, y1=17, fillcolor=GREEN, opacity=0.08,
                  annotation_text="Pre-crisis range\n(2021–2022)",
                  annotation_font=dict(size=10, color=GREEN))
    fig.add_hline(y=0, line=dict(color="#9CA3AF", width=1, dash="dot"))
    fig.update_layout(height=300, **_L,
                      title=dict(text="EBIT Margin Recovery Path",
                                 font=dict(color="#1A1A2E", size=12)),
                      yaxis=dict(ticksuffix="%", gridcolor="#F0F0F0",
                                 tickfont=dict(color="#374151")),
                      xaxis=dict(tickfont=dict(color="#374151")))
    return fig


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
st.sidebar.markdown(f"""
<div style="background:linear-gradient(135deg,{BLUE_DARK} 0%,{BLUE} 100%);
            color:white;padding:16px;border-radius:10px;margin-bottom:1.2rem;">
  <div style="font-size:1.1rem;font-weight:800;letter-spacing:0.5px;">INTC Terminal</div>
  <div style="font-size:0.73rem;opacity:0.8;margin-top:3px;">NASDAQ: INTC  ·  Damodaran Framework</div>
  <div style="font-size:0.68rem;opacity:0.65;margin-top:2px;">Semiconductor · IDM 2.0 · Turnaround</div>
</div>
""", unsafe_allow_html=True)

PAGE = st.sidebar.radio("Navigate", [
    "📡  Live Market",
    "🏭  Industry Analysis",
    "💰  Valuation (DCF)",
    "📈  Forecasting",
    "⚔️   Competition",
    "🔄  Life Cycle",
    "🎯  Marketing Strategy",
    "📰  Live News",
])

st.sidebar.markdown("---")
st.sidebar.markdown(f"""
<div style="font-size:0.78rem;color:#94A3B8;line-height:1.8;">
  <b style="color:#CBD5E1;">Data Sources</b><br>
  · Live price: Yahoo Finance<br>
  · Fundamentals: Intel 10-K FY20–24<br>
  · News: Google News RSS<br>
  · Framework: Damodaran (NYU Stern)<br>
  <br>
  <b style="color:#CBD5E1;">Prepared by:</b><br>
  Aditi Ranjan<br>
  BBA Corporate Finance<br>
  <br>
  <b style="color:#CBD5E1;">Valuation Date:</b><br>
  {datetime.now().strftime("%d %b %Y  %H:%M")}
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("🔄  Refresh Live Data"):
    st.cache_data.clear()
    st.rerun()


# ── LIVE DATA ─────────────────────────────────────────────────────────────────
live      = get_live_price()
chg_sign  = "+" if live["change"] >= 0 else ""
chg_arrow = "▲" if live["change"] >= 0 else "▼"
chg_color = "#16A34A" if live["change"] >= 0 else "#DC2626"

# ── MASTER HEADER ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(135deg,{BLUE_DARK} 0%,{BLUE} 60%,{CYAN} 100%);
            padding:1.4rem 1.8rem;border-radius:14px;margin-bottom:1.3rem;
            box-shadow:0 6px 24px rgba(0,60,113,0.30);">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;
              flex-wrap:wrap;gap:12px;">
    <div>
      <div style="font-size:1.55rem;font-weight:800;color:#fff;letter-spacing:0.5px;
                  font-family:'Inter',sans-serif;">
        INTEL CORPORATION &nbsp;·&nbsp; RESEARCH TERMINAL
      </div>
      <div style="font-size:0.79rem;color:rgba(255,255,255,0.68);margin-top:4px;
                  font-family:'Inter',sans-serif;">
        Forecasting · Valuation · Marketing Strategy · Damodaran Framework
        &nbsp;·&nbsp; {datetime.now().strftime("%d %B %Y")}
      </div>
      <div style="margin-top:0.9rem;display:flex;align-items:baseline;
                  gap:1.4rem;flex-wrap:wrap;">
        <span style="font-size:2.6rem;font-weight:800;color:#fff;
                     font-family:'Inter',sans-serif;">${live['price']}</span>
        <span style="font-size:1rem;color:{chg_color};font-weight:700;
                     background:rgba(255,255,255,0.14);padding:4px 12px;
                     border-radius:99px;font-family:'Inter',sans-serif;">
          {chg_arrow} {chg_sign}{live['change']} ({chg_sign}{live['change_pct']}%)
        </span>
        <span style="font-size:0.78rem;color:rgba(255,255,255,0.50);
                     font-family:'Inter',sans-serif;">
          NASDAQ: INTC &nbsp;·&nbsp; Live via Yahoo Finance
        </span>
      </div>
    </div>
    <div style="text-align:right;color:rgba(255,255,255,0.72);font-family:'Inter',sans-serif;">
      <div style="font-size:0.78rem;">Mkt Cap: <b style="color:#fff;">{live['market_cap']}</b></div>
      <div style="font-size:0.78rem;margin-top:3px;">Volume: <b style="color:#fff;">{live['volume']}</b></div>
      <div style="font-size:0.78rem;margin-top:3px;">52W: <b style="color:#fff;">${live['52w_low']} – ${live['52w_high']}</b></div>
      <div style="font-size:0.78rem;margin-top:3px;">P/B: <b style="color:#fff;">{live['pb']}×</b>
        &nbsp;·&nbsp; Beta: <b style="color:#fff;">{live['beta']}</b></div>
      <div style="font-size:0.72rem;margin-top:5px;color:rgba(255,255,255,0.50);">
        Dividend suspended Oct 2024
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE 1 — LIVE MARKET
# ═════════════════════════════════════════════════════════════════════════════
if PAGE == "📡  Live Market":
    st.markdown('<div class="narrative">Intel\'s stock is not a number — it is a vote on whether a 50-year-old giant can reinvent itself for the age of artificial intelligence. The price you see today encodes the market\'s collective probability estimate that the 18A process works, the foundry business is real, and the transformation succeeds. Reading the number honestly requires understanding the story behind it.</div>', unsafe_allow_html=True)

    kpis = [
        ("Current Price",    f"${live['price']}",        f"{chg_sign}{live['change_pct']}% today"),
        ("Market Cap",       live["market_cap"],           "NASDAQ listed"),
        ("P/B Ratio (TTM)",  f"{live['pb']}×",            "Below book value"),
        ("P/E Ratio",        "N/M (loss yr)",              "GAAP NI –$18.8B FY24"),
        ("Dividend Yield",   "0% (suspended)",             "Suspended Oct 2024"),
        ("Beta (β)",         f"{live['beta']}",            "Cyclical + transforming"),
    ]
    cols = st.columns(6)
    for col, (lbl, val, sub) in zip(cols, kpis):
        col.markdown(
            f'<div class="kpi-card"><div class="kpi-label">{lbl}</div>'
            f'<div class="kpi-value">{val}</div>'
            f'<div class="kpi-sub">{sub}</div></div>',
            unsafe_allow_html=True
        )

    st.markdown("")
    c1, c2 = st.columns([2.2, 1])

    with c1:
        st.markdown('<div class="sec-head">Price Chart — Candlestick + Volume + Moving Averages</div>', unsafe_allow_html=True)
        period = st.selectbox("Period", ["1mo","3mo","6mo","1y","2y"], index=2,
                              label_visibility="collapsed")
        st.plotly_chart(candlestick_chart(get_price_history(period)), use_container_width=True)

    with c2:
        st.markdown('<div class="sec-head">52-Week Range</div>', unsafe_allow_html=True)
        try:
            lo = float(str(live["52w_low"]).replace(",",""))
            hi = float(str(live["52w_high"]).replace(",",""))
        except Exception:
            lo, hi = 16.0, 37.0
        gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=live["price"],
            number=dict(prefix="$", font=dict(color=BLUE, size=30)),
            gauge=dict(
                axis=dict(range=[lo, hi], tickfont=dict(color="#374151")),
                bar=dict(color=BLUE),
                steps=[{"range":[lo,(lo+hi)/2],"color":"#FEE2E2"},
                       {"range":[(lo+hi)/2,hi],"color":"#DBEAFE"}],
                bordercolor=BORDER
            ),
            title=dict(text=f"${lo:.0f} – ${hi:.0f}  (52-Week)",
                       font=dict(color="#374151", size=12))
        ))
        gauge.update_layout(height=250, paper_bgcolor="#FFFFFF",
                            margin=dict(l=20,r=20,t=60,b=10),
                            font=dict(color="#1A1A2E"))
        st.plotly_chart(gauge, use_container_width=True)

        st.markdown('<div class="sec-head">FY2024 Snapshot</div>', unsafe_allow_html=True)
        for lbl, val in [
            ("Revenue",          "$53.1B"),
            ("Gross Margin",     "35.1%"),
            ("EBIT Margin",      "~0%"),
            ("Net Income (GAAP)","–$18.8B"),
            ("Free Cash Flow",   "–$15.7B"),
            ("Gross Capex",      "$23.9B"),
        ]:
            st.markdown(
                f"<span style='color:#6B7280;font-size:0.8rem;'>{lbl}</span> &nbsp;"
                f"<b style='color:#1A1A2E;'>{val}</b>",
                unsafe_allow_html=True
            )

    st.markdown('<div class="sec-head">Revenue, EBIT Margin & FCF — FY2020 to FY2024 (The Wound in Numbers)</div>', unsafe_allow_html=True)
    st.plotly_chart(rev_profile_chart(), use_container_width=True)

    st.markdown('<div class="sec-head">Capital Expenditure vs Operating Cash Flow — The Investment Thesis</div>', unsafe_allow_html=True)
    st.plotly_chart(capex_fcf_chart(), use_container_width=True)

    st.markdown(f"""
    <div class="q-card-blue">
      <b style="color:{BLUE_DARK};">The \$120 Billion Bet</b><br>
      <span style="font-size:0.88rem;color:#0c2a4a;">
        Intel spent <b>\$120 billion in capital expenditures over FY2020–2024</b> — more than its
        current market capitalisation — building what it believes will be the world's most advanced
        semiconductor manufacturing process (Intel 18A). A company trading at below book value that
        owns \$120B of the world's most sophisticated manufacturing infrastructure is either
        <b>deeply undervalued or sitting on assets that will never earn an adequate return</b>.
        The next three years will determine which.
      </span>
    </div>
    """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE 2 — INDUSTRY
# ═════════════════════════════════════════════════════════════════════════════
elif PAGE == "🏭  Industry Analysis":
    st.markdown('<div class="narrative">Before examining a single Intel number, the Damodaran discipline requires understanding the industry ceiling. Intel is a dominant player in markets that are growing slowly, and a marginal player in markets that are growing fast. This is not a death sentence — it is the precise description of its transformation challenge.</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head">The Five Arenas — Intel\'s Market Position</div>', unsafe_allow_html=True)
    ind_df = pd.DataFrame([
        {"Segment":"AI Accelerators","2024 TAM":"~$100B","2029E TAM":"$250B+","CAGR":"~20%+","Intel Exposure":"<1% — Gaudi 3; nascent","Intel Revenue FY24":"~$0.5B","Strategic Verdict":"Most urgently needs traction"},
        {"Segment":"Data Centre CPUs","2024 TAM":"~$35B", "2029E TAM":"$55B", "CAGR":"~9%","Intel Exposure":"~65% share (declining)","Intel Revenue FY24":"~$15.9B","Strategic Verdict":"Core franchise; AMD gaining"},
        {"Segment":"Client CPUs (PC)","2024 TAM":"~$50B", "2029E TAM":"$56B", "CAGR":"~2%","Intel Exposure":"~60% — ARM threat building","Intel Revenue FY24":"~$31.9B","Strategic Verdict":"Cash cow; low growth"},
        {"Segment":"Foundry Services","2024 TAM":"~$130B","2029E TAM":"$200B","CAGR":"~9%","Intel Exposure":"~3% — building Intel 18A","Intel Revenue FY24":"~$4.3B","Strategic Verdict":"The transformational bet"},
        {"Segment":"Network & Edge","2024 TAM":"~$20B", "2029E TAM":"$28B", "CAGR":"~7%","Intel Exposure":"~29% share — stable","Intel Revenue FY24":"~$5.8B","Strategic Verdict":"Steady; low priority"},
    ])
    st.dataframe(ind_df, use_container_width=True, hide_index=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="sec-head">Segment Revenue — FY2023 vs FY2024</div>', unsafe_allow_html=True)
        st.plotly_chart(segment_chart(), use_container_width=True)
    with c2:
        st.markdown('<div class="sec-head">EBIT Margin by Segment — FY2024</div>', unsafe_allow_html=True)
        st.plotly_chart(segment_margin_chart(), use_container_width=True)

    st.markdown(f"""
    <div class="narrative">
      The structural asymmetry is damning in its clarity: Client CPUs generate ~60% of Intel's revenue
      but grow at 2% per year. AI Accelerators, the fastest-growing market in the history of electronics,
      account for less than 1% of Intel's revenue. Intel is running a growth strategy against a
      declining-growth base — and the outcome depends on whether the transformation investments
      generate new revenue streams before the legacy markets begin to seriously erode.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-head">The Three Forces Reshaping Intel\'s World</div>', unsafe_allow_html=True)
    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown(f"""
        <div class="q-card-blue">
          <b style="color:{BLUE_DARK};">Force 1: The AI Revolution</b><br>
          <span style="font-size:0.84rem;color:#0c2a4a;">
            NVIDIA's dominance of AI training has rewritten semiconductor economics.
            When a single H100 GPU sells for \$30,000 and has a 2-year waiting list,
            Intel's traditional pricing model becomes irrelevant. AI has created
            winner-take-most dynamics — and Intel arrived late.
          </span>
        </div>
        """, unsafe_allow_html=True)
    with f2:
        st.markdown(f"""
        <div class="q-card-cyan">
          <b style="color:{BLUE_DARK};">Force 2: Geopolitical Fragmentation</b><br>
          <span style="font-size:0.84rem;color:#0c2a4a;">
            TSMC makes ~90% of the world's most advanced chips from Taiwan.
            Every government is quietly desperate for a non-Taiwan alternative.
            The US CHIPS Act (\$52B) and Intel's \$7.86B award are a direct
            response to this anxiety. Intel is uniquely positioned — if 18A works.
          </span>
        </div>
        """, unsafe_allow_html=True)
    with f3:
        st.markdown(f"""
        <div class="q-card-steel">
          <b style="color:{BLUE_DARK};">Force 3: ARM Architecture Migration</b><br>
          <span style="font-size:0.84rem;color:#0c2a4a;">
            Apple's M-series MacBook proved ARM could beat x86 on performance
            per watt. Enterprise inertia is powerful — but the siege has begun.
            Intel's response (AI NPU in Core Ultra) buys time; it does not
            solve the structural efficiency gap with ARM.
          </span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="pullquote">
      Intel's industry is a 'winner's curse' business. The prize for winning (process leadership)
      requires spending decades and hundreds of billions. The prize for losing is irrelevance
      within a generation. There is no comfortable middle ground.
    </div>
    """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE 3 — VALUATION
# ═════════════════════════════════════════════════════════════════════════════
elif PAGE == "💰  Valuation (DCF)":
    st.markdown('<div class="narrative">You cannot value Intel on today\'s earnings — a company cannot be valued on near-zero earnings. The correct question is: what is the present value of the cash flows this company will generate if the transformation succeeds? The gap between that value and today\'s price is the market\'s estimate of execution risk.</div>', unsafe_allow_html=True)

    c_sliders, c_result = st.columns([1, 1])

    with c_sliders:
        st.markdown('<div class="sec-head">Adjust DCF Assumptions</div>', unsafe_allow_html=True)
        wacc_val    = st.slider("WACC (%)",                   6.0,  12.0,  8.0, 0.1, format="%.1f%%")
        g_val       = st.slider("Terminal Growth Rate (%)",   1.0,   4.0,  2.5, 0.1, format="%.1f%%")
        rev_cagr    = st.slider("Revenue CAGR — 5yr (%)",     1.0,  12.0,  6.8, 0.5, format="%.1f%%")
        ebit_m_y5   = st.slider("EBIT Margin Y5 (%)",         3.0,  22.0, 15.0, 0.5, format="%.1f%%")

        st.markdown(f"""
        <div class="q-card-blue" style="margin-top:12px;">
          <b style="color:{BLUE_DARK};">WACC Build-Up (Damodaran CAPM)</b><br>
          <span style="font-size:0.82rem;color:#0c2a4a;">
            Rf = 4.30% (10-yr UST, Mar 2026)<br>
            ERP = 5.50% · β = {live['beta']} (cyclical + transforming)<br>
            Ke = {round(4.30 + live['beta']*5.50, 2)}% &nbsp;·&nbsp; Kd(at) = 3.44%<br>
            Debt ~33% of capital &nbsp;·&nbsp; <b>Applied WACC = {wacc_val}%</b>
          </span>
        </div>
        <div class="q-card-gold">
          <b style="color:{GOLD};">EBIT Margin Ramp Path</b><br>
          <span style="font-size:0.78rem;color:#6B4500;">
            Y1 2.0% → Y2 {round(2+(ebit_m_y5-2)*1/4,1)}% → Y3 {round(2+(ebit_m_y5-2)*2/4,1)}% 
            → Y4 {round(2+(ebit_m_y5-2)*3/4,1)}% → Y5 {ebit_m_y5:.1f}%
          </span>
        </div>
        """, unsafe_allow_html=True)

    result = run_dcf(wacc_val, g_val, rev_cagr, ebit_m_y5, live["price"])

    with c_result:
        st.markdown('<div class="sec-head">DCF Output</div>', unsafe_allow_html=True)
        if result is None:
            st.error("⚠ WACC must exceed terminal growth rate. Adjust sliders.")
        else:
            up       = result["upside"]
            up_col   = GREEN if up > 20 else BLUE if up > 0 else RED
            up_arrow = "▲" if up > 0 else "▼"
            mos_lbl  = "UNDERVALUED" if up > 20 else "FAIRLY VALUED" if up > 0 else "OVERVALUED"

            st.markdown(f"""
            <div style="background:#fff;border:2px solid {up_col}44;border-radius:14px;
                        padding:1.6rem;text-align:center;
                        box-shadow:0 4px 16px {up_col}18;">
              <div style="font-size:0.85rem;color:#6B7280;margin-bottom:6px;font-weight:600;
                          text-transform:uppercase;letter-spacing:0.8px;">Intrinsic Value Per Share</div>
              <div style="font-size:3.4rem;font-weight:800;color:{up_col};
                          font-family:'Inter',sans-serif;line-height:1.1;">
                ${result['ivps']}</div>
              <div style="font-size:1.05rem;color:{up_col};margin-top:10px;font-weight:700;">
                {up_arrow} {up}% vs market price ${live['price']}</div>
              <div style="margin-top:8px;">
                <span style="background:{up_col}18;color:{up_col};padding:4px 14px;
                             border-radius:99px;font-size:0.8rem;font-weight:700;">
                  {mos_lbl}
                </span>
              </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("")
            r1, r2 = st.columns(2)
            r1.metric("PV Explicit FCFFs", f"${result['pv_explicit']:.1f}B")
            r2.metric("PV Terminal Value",  f"${result['pv_tv']:.1f}B")
            r1.metric("Enterprise Value",   f"${result['ev']:.1f}B")
            r2.metric("Equity Value",       f"${result['eq_val']:.1f}B")
            if result["tv_pct"] > 75:
                st.warning(f"⚠ Terminal value = **{result['tv_pct']}%** of EV. Extreme sensitivity to WACC and g — verify assumptions carefully.")
            else:
                st.info(f"Terminal value = **{result['tv_pct']}%** of Enterprise Value")

    if result:
        st.markdown('<div class="sec-head">FCFF Projection vs Present Value</div>', unsafe_allow_html=True)
        st.plotly_chart(dcf_bar_chart(result), use_container_width=True)

        if result["rows"]:
            st.markdown('<div class="sec-head">Projected FCFF Schedule</div>', unsafe_allow_html=True)
            st.dataframe(pd.DataFrame(result["rows"]), use_container_width=True, hide_index=True)

        st.markdown('<div class="sec-head">Scenario Comparison — Three Stories, Three Values</div>', unsafe_allow_html=True)
        st.plotly_chart(scenario_bar_chart(live["price"]), use_container_width=True)

        b1, b2, b3 = st.columns(3)
        with b1:
            st.markdown(f"""
            <div class="scen-card" style="background:{GREEN_LIGHT};border-top:3px solid {GREEN};">
              <b style="color:{GREEN};">🚀 Bull Case (25%)</b><br>
              <span style="font-size:0.82rem;color:#1A3A2A;">18A achieves process parity with TSMC.
              Gaudi 3 captures 5–8% AI accelerator market. Foundry earns \$6B+ external revenue by FY2029.
              Revenue \$80B+. EBIT 20%+.<br><b>Intrinsic value: \$52–58</b></span>
            </div>
            """, unsafe_allow_html=True)
        with b2:
            b_base = run_dcf(8.0, 2.5, 6.8, 15.0, live["price"])
            biv = f"${b_base['ivps']}" if b_base else "$30–32"
            st.markdown(f"""
            <div class="scen-card" style="background:{BLUE_LIGHT};border-top:3px solid {BLUE};">
              <b style="color:{BLUE_DARK};">📊 Base Case (50%)</b><br>
              <span style="font-size:0.82rem;color:#0c2a4a;">18A works well enough. Panther Lake
              ships on time. Foundry earns \$5–6B external revenue. EBIT margins recover to 14–16%.
              FCF turns positive FY2026–27.<br><b>Intrinsic value: {biv}</b></span>
            </div>
            """, unsafe_allow_html=True)
        with b3:
            b_bear = run_dcf(8.0, 2.5, 2.0, 8.0, live["price"])
            biv_br = f"${b_bear['ivps']}" if b_bear else "$14–16"
            st.markdown(f"""
            <div class="scen-card" style="background:{RED_LIGHT};border-top:3px solid {RED};">
              <b style="color:{RED};">🐻 Bear Case (25%)</b><br>
              <span style="font-size:0.82rem;color:#6B1A1A;">18A yields disappoint. Foundry customers
              stay with TSMC. AMD takes 40%+ of data centre CPUs. Intel becomes semi-fabless.
              Revenue stabilises at \$50–55B, thin margins.<br><b>Intrinsic value: {biv_br}</b></span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="sec-head">Sensitivity Table — Intrinsic Value ($) by WACC and Terminal Growth</div>', unsafe_allow_html=True)
        sens = sensitivity_table(rev_cagr, ebit_m_y5, live["price"])
        st.dataframe(sens.style.background_gradient(cmap="RdYlGn", axis=None), use_container_width=True)

        st.markdown('<div class="sec-head">Monte Carlo — Probability Distribution of Intrinsic Value</div>', unsafe_allow_html=True)
        with st.spinner("Running 1,500 Monte Carlo trials…"):
            mc_arr = mc_simulation(rev_cagr, ebit_m_y5, wacc_val, g_val, live["price"])

        mc_fig = go.Figure()
        mc_fig.add_trace(go.Histogram(x=mc_arr, nbinsx=50, marker_color=BLUE,
                                       opacity=0.82, name="Intrinsic Value $"))
        for pct, lbl, lc in [(10,"P10",RED),(50,"Median",CYAN),(90,"P90",GREEN)]:
            v = float(np.percentile(mc_arr, pct))
            mc_fig.add_vline(x=v, line=dict(color=lc, width=1.8, dash="dash"),
                             annotation_text=f"{lbl} ${v:.1f}",
                             annotation_font=dict(color=lc, size=10))
        mc_fig.add_vline(x=live["price"], line=dict(color=GOLD, width=2),
                         annotation_text=f"Market ${live['price']}",
                         annotation_font=dict(color=GOLD, size=10))
        mc_fig.update_layout(height=280, **_L, showlegend=False,
                             xaxis_title="Intrinsic Value ($/share)",
                             yaxis_title="Frequency",
                             title=dict(text="Monte Carlo: 1,500 trials (triangular on growth, margin, WACC)",
                                        font=dict(color="#1A1A2E", size=12)))
        st.plotly_chart(mc_fig, use_container_width=True)
        p_above = float(np.mean(mc_arr > live["price"]) * 100)
        ci10 = float(np.percentile(mc_arr, 10))
        ci90 = float(np.percentile(mc_arr, 90))
        ma_, mb_, mc__ = st.columns(3)
        ma_.metric("P(Intrinsic > Market Price)", f"{p_above:.1f}%")
        mb_.metric("80% Confidence Interval",      f"${ci10:.1f} – ${ci90:.1f}")
        mc__.metric("Mean Intrinsic Value",        f"${float(np.mean(mc_arr)):.2f}")


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE 4 — FORECASTING
# ═════════════════════════════════════════════════════════════════════════════
elif PAGE == "📈  Forecasting":
    st.markdown('<div class="narrative">Forecasting Intel is unlike forecasting any other company. You are not projecting steady-state earnings — you are modelling a transition from a state of distress to a state of recovery, with a binary variable (18A process success) determining most of the outcome. The numbers below encode a specific story: partial success, gradual normalisation, measured recovery.</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Adjust Forecast Assumptions</div>', unsafe_allow_html=True)
    cf1, cf2, cf3 = st.columns(3)
    with cf1: rg  = st.slider("Revenue Growth CAGR (%)", 1.0, 12.0, 6.8, 0.5)
    with cf2: em5 = st.slider("EBIT Margin Y5 (%)",       3.0, 22.0, 15.0, 0.5)
    with cf3: tax = st.slider("Effective Tax Rate (%)",    8.0, 20.0, 13.0, 0.5)

    proj_rows = []
    rev_prev  = BASE["revenue"]
    margin_path = [2.0 + (em5 - 2.0) * i / 4 for i in range(5)]

    for i in range(5):
        rev_i    = BASE["revenue"] * (1 + rg/100) ** (i+1)
        ebit_m_i = margin_path[i]
        ebit_i   = rev_i * ebit_m_i / 100
        da_i     = rev_i * 0.28
        ni_i     = ebit_i * (1 - tax/100) - 1.8  # interest ~$1.8B
        drv      = rev_i - rev_prev
        reinv_i  = drv / 0.40
        fcff_i   = ebit_i * (1 - tax/100) - reinv_i
        cfo_i    = ni_i + da_i + 3.0  # SBC + working capital
        capex_i  = da_i + max(reinv_i, 0) * 0.8
        rev_prev = rev_i
        proj_rows.append({
            "Year":          f"FY{25+i}",
            "Revenue ($B)":  round(rev_i, 1),
            "EBIT Margin":   f"{ebit_m_i:.1f}%",
            "EBIT ($B)":     round(ebit_i, 2),
            "NI ($B)":       round(ni_i, 2),
            "FCFF ($B)":     round(fcff_i, 2),
            "CapEx ($B)":    round(capex_i, 1),
            "CFO ($B)":      round(cfo_i, 1),
        })

    c1, c2 = st.columns([1.6, 1])
    with c1:
        st.plotly_chart(forecast_chart(proj_rows), use_container_width=True)
        st.plotly_chart(margin_recovery_chart(proj_rows), use_container_width=True)
    with c2:
        display = [{
            "Year":          r["Year"],
            "Revenue ($B)":  f"${r['Revenue ($B)']}",
            "EBIT Margin":   r["EBIT Margin"],
            "EBIT ($B)":     f"${r['EBIT ($B)']}",
            "NI ($B)":       f"${r['NI ($B)']}",
            "FCFF ($B)":     f"${r['FCFF ($B)']}",
        } for r in proj_rows]
        st.dataframe(pd.DataFrame(display), use_container_width=True, hide_index=True)

        dcf_s = run_dcf(8.0, 2.5, rg, em5, live["price"])
        st.markdown("")
        ca, cb = st.columns(2)
        ca.metric("FY2029 Revenue", f"${proj_rows[-1]['Revenue ($B)']}B",
                  f"+{round(((proj_rows[-1]['Revenue ($B)']/BASE['revenue'])**(1/5)-1)*100,1)}% CAGR")
        cb.metric("FY2029 EBIT", f"${proj_rows[-1]['EBIT ($B)']}B",
                  f"Margin {proj_rows[-1]['EBIT Margin']}")
        if dcf_s:
            st.metric("DCF Intrinsic Value", f"${dcf_s['ivps']}",
                      f"{'▲' if dcf_s['upside']>0 else '▼'} {dcf_s['upside']}% vs ${live['price']}")
        st.metric("FY2029 FCFF", f"${proj_rows[-1]['FCFF ($B)']}B",
                  "FCF inflection from trough")

    st.markdown('<div class="sec-head">Scenario Comparison — FY2029 Revenue, EBIT, Intrinsic Value</div>', unsafe_allow_html=True)
    st.plotly_chart(scenario_bar_chart(live["price"]), use_container_width=True)

    st.markdown('<div class="sec-head">Growth Method Triangulation</div>', unsafe_allow_html=True)
    growth_methods = pd.DataFrame([
        {"Method":"Fundamental (ROC × RR)","Implied CAGR":"8.0%","Weight":"Theoretical","Rationale":"Normalised ROC 10% × Reinvestment Rate 80% = 8.0%. Reflects heavy capital intensity."},
        {"Method":"Historical CAGR (FY20–24)","Implied CAGR":"–9.3%","Weight":"Reject","Rationale":"Revenue declined from $77.9B to $53.1B. Not representative of future trajectory."},
        {"Method":"Bottom-Up (CCG+DCAI+NEX+IFS)","Implied CAGR":"6.5%","Weight":"Cross-check","Rationale":"CCG +2%, DCAI +10% (AI PC + server), NEX +5%, IFS ramp from $4B to $12B. Sum: ~$73B by FY2029."},
        {"Method":"Top-Down (Semi TAM × Share)","Implied CAGR":"7.1%","Weight":"Cross-check","Rationale":"Semi TAM $586B→$1T, Intel addressable ~$250B, share 7.3%. Adjusted for market headwinds."},
        {"Method":"Guidance / Analyst Consensus","Implied CAGR":"3–7%","Weight":"Ceiling","Rationale":"Management guided 3–7%. Consensus: mid-single-digit recovery. Reflects post-restructuring base."},
        {"Method":"★ Chosen Base Case","Implied CAGR":"6.8%","Weight":"PRIMARY","Rationale":"Blended bottom-up/fundamental. Revenue $53.1B→$73.8B. Modest early (supply healing), accelerating with 18A ramp."},
    ])
    st.dataframe(growth_methods, use_container_width=True, hide_index=True)

    st.markdown(f"""
    <div class="pullquote">
      A 6.8% CAGR adds \$20.7B of incremental revenue over five years. That is not aggressive —
      it requires Intel to regain some data centre share, grow AI PC volumes, and begin
      generating real foundry revenue. It does not require Gaudi 3 to defeat NVIDIA.
      The conservatism is intentional.
    </div>
    """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE 5 — COMPETITION
# ═════════════════════════════════════════════════════════════════════════════
elif PAGE == "⚔️   Competition":
    st.markdown('<div class="narrative">Intel does not have a single competitor. It has three distinct battles simultaneously, in three different arenas, against three different adversaries. The strategies required to win each battle are different — and sometimes in tension with each other. Understanding this multi-front war is essential for understanding Intel\'s risk.</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1.2, 1])
    with c1:
        st.markdown('<div class="sec-head">Relative Positioning — Radar Chart</div>', unsafe_allow_html=True)
        st.plotly_chart(radar_chart(), use_container_width=True)
    with c2:
        st.markdown('<div class="sec-head">Three Simultaneous Battles</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="q-card-blue">
          <b style="color:{BLUE_DARK};">Battle 1 — vs AMD in CPUs</b><br>
          <span style="font-size:0.84rem;color:#0c2a4a;">AMD has gone from 5% of server CPU revenue
          to ~35% in six years. Intel's Xeon 6 is competitive, but momentum is AMD's.
          Realistic path: <b>hold 55–60% server share through platform advantages</b>.
          The enterprise software ecosystem and supply chain relationships still matter.</span>
        </div>
        <div class="q-card-cyan">
          <b style="color:{BLUE_DARK};">Battle 2 — vs NVIDIA in AI</b><br>
          <span style="font-size:0.84rem;color:#0c2a4a;">This is the war Intel is most visibly losing.
          NVIDIA earns 60% operating margins on AI chips. Gaudi 3 competes on price-performance,
          but CUDA is the real moat — a decade of developer habit.
          Realistic path: <b>5–8% AI accelerator share by FY2028</b> via price advantage.</span>
        </div>
        <div class="q-card-steel">
          <b style="color:{BLUE_DARK};">Battle 3 — vs TSMC in Foundry</b><br>
          <span style="font-size:0.84rem;color:#0c2a4a;">TSMC's dominance of advanced manufacturing
          is both Intel's competitive challenge and its strategic opportunity. Every government
          is desperate for a non-Taiwan alternative. Realistic path: <b>10–15% of Western
          foundry market via geo-premium and CHIPS Act support</b>.</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Peer Benchmarking — Key Metrics</div>', unsafe_allow_html=True)
    pd_d = PEERS.copy()
    pd_d["PE"]       = pd_d["PE"].apply(lambda x: f"~{x}×" if x > 0 else "N/M (loss)")
    pd_d["EBIT_M"]   = pd_d["EBIT_M"].apply(lambda x: f"{x:.1f}%")
    pd_d["Rev_CAGR"] = pd_d["Rev_CAGR"].apply(lambda x: f"~{x}%" if x >= 0 else f"{x}%")
    pd_d["ROIC"]     = pd_d["ROIC"].apply(lambda x: f"~{x}%" if x > 0 else f"~{x}% (loss)")
    pd_d["PB"]       = pd_d["PB"].apply(lambda x: f"~{x}×")
    st.dataframe(
        pd_d.rename(columns={"PE":"P/E TTM","EBIT_M":"EBIT Margin","Rev_CAGR":"3yr CAGR",
                              "PB":"P/B","Note":"Context"}),
        use_container_width=True, hide_index=True
    )

    st.markdown('<div class="sec-head">EBIT Margin Comparison — Intel vs Peers</div>', unsafe_allow_html=True)
    cols_p = [BLUE, CYAN, GOLD, STEEL, "#B8860B", RED]
    peers_vis = PEERS[PEERS["EBIT_M"] >= 0].copy()
    fig_p = go.Figure(go.Bar(
        x=peers_vis["Company"], y=peers_vis["EBIT_M"],
        marker_color=cols_p[:len(peers_vis)],
        text=[f"{m:.0f}%" for m in peers_vis["EBIT_M"]], textposition="outside",
        textfont=dict(color="#1A1A2E", size=11)
    ))
    fig_p.update_layout(height=280, **_L,
                        title=dict(text="EBIT Margin — Intel vs Peers (FY2024 / LTM)",
                                   font=dict(color="#1A1A2E", size=13)),
                        yaxis=dict(ticksuffix="%", gridcolor="#F0F0F0",
                                   tickfont=dict(color="#374151")),
                        xaxis=dict(tickfont=dict(color="#374151", size=12)), showlegend=False)
    st.plotly_chart(fig_p, use_container_width=True)

    st.markdown('<div class="sec-head">Battle Map — Position, Adversary Advantage, Intel\'s Path</div>', unsafe_allow_html=True)
    battle_df = pd.DataFrame([
        {"Battle":"Server CPUs vs AMD",   "Intel Position":"~65% share, losing ground","Adversary Advantage":"AMD: superior arch. efficiency; TSMC process","Intel Realistic Path":"Hold 55–60% share through platform + Xeon 6"},
        {"Battle":"AI Chips vs NVIDIA",   "Intel Position":"<1% of accelerator market","Adversary Advantage":"NVIDIA: CUDA ecosystem; 10-yr developer moat","Intel Realistic Path":"5–8% share by FY2028 via price advantage + open stack"},
        {"Battle":"Foundry vs TSMC",      "Intel Position":"3% of advanced wafer market","Adversary Advantage":"TSMC: 20-yr lead; trusted yield; scale","Intel Realistic Path":"10–15% of Western market via geo-premium + CHIPS Act"},
        {"Battle":"PC CPUs vs ARM",       "Intel Position":"~60% PC share; ARM threat building","Adversary Advantage":"ARM: power efficiency; Apple M-series proof","Intel Realistic Path":"Defend through AI PC NPU; Core Ultra differentiation"},
    ])
    st.dataframe(battle_df, use_container_width=True, hide_index=True)

    st.markdown(f"""
    <div class="narrative">
      One number cuts through the entire competitive narrative. Intel spent \$120 billion on
      capital expenditures over the last five years. A company that owns \$120B of the world's
      most sophisticated manufacturing infrastructure and trades at roughly \$96B market
      capitalisation is either deeply undervalued — or sitting on assets that will never earn
      an adequate return. The next three years will determine which.
    </div>
    """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE 6 — LIFE CYCLE
# ═════════════════════════════════════════════════════════════════════════════
elif PAGE == "🔄  Life Cycle":
    st.markdown('<div class="narrative">Damodaran\'s most important insight: the biggest valuation errors come from applying the wrong life-cycle assumptions to a company. Intel\'s situation is rare and dangerous — a mature company that has voluntarily re-entered the investment phase. It is spending like a start-up while earning like a company in distress. This is either a brilliant transformation play or the final act of an empire in decline.</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head">The Five Stages — Intel\'s Unusual Position</div>', unsafe_allow_html=True)
    lc = pd.DataFrame([
        {"Stage":"Start-up",               "Rev. Growth":">100%",     "Margins":"Negative","FCF":"Deeply Neg.","Reinvestment":">100%","Dividends":"Zero",    "INTC?":""},
        {"Stage":"Young Growth",            "Rev. Growth":"50–100%",   "Margins":"Low/+",   "FCF":"Negative",   "Reinvestment":"80–100%","Dividends":"Zero",   "INTC?":""},
        {"Stage":"High Growth",             "Rev. Growth":"20–50%",    "Margins":"Rising",  "FCF":"Near Zero",  "Reinvestment":"50–80%","Dividends":"Low",    "INTC?":""},
        {"Stage":"Mature Growth",           "Rev. Growth":"5–20%",     "Margins":"Peak",    "FCF":"Positive",   "Reinvestment":"30–50%","Dividends":"Moderate","INTC?":"(was)"},
        {"Stage":"★ Crisis Reinvestment ← INTC","Rev. Growth":"Flat/Neg.","Margins":"Near 0","FCF":"Deeply Neg.","Reinvestment":"High(forced)","Dividends":"Suspended","INTC?":"✅"},
        {"Stage":"Decline",                 "Rev. Growth":"<0%",       "Margins":"Falling", "FCF":"Falling",    "Reinvestment":"Minimal","Dividends":"V.High/N/A","INTC?":""},
    ])
    def hl_intc(row):
        if "INTC" in str(row["Stage"]) and "★" in str(row["Stage"]):
            return [f"background-color:{BLUE_LIGHT};color:{BLUE_DARK};font-weight:700"]*len(row)
        return [""]*len(row)
    st.dataframe(lc.style.apply(hl_intc, axis=1), use_container_width=True, hide_index=True)

    st.markdown('<div class="sec-head">Financial Fingerprints — The Crisis Reinvestment Profile</div>', unsafe_allow_html=True)
    fps = [
        ("Revenue Growth (FY24)",     "–2% YoY",         "Legacy engine stalling ⚠"),
        ("EBIT Margin (FY24)",         "~0% GAAP",         "Cost structure not yet reset ⚠"),
        ("Free Cash Flow (FY24)",      "–$15.7B",          "Deeply negative — transformation cost ⚠"),
        ("Capex / Revenue",            "45% (FY24)",        "Classic 'forced reinvestment' ⚠"),
        ("Return on Invested Capital", "~0% (FY24)",        "No value created yet — below CoC ⚠"),
        ("R&D / Revenue",              "~31%",              "Genuine innovation intensity ✓"),
        ("Dividend Policy",            "Suspended Oct 2024","Management prioritising capital ⚠"),
        ("Net Loss (FY24)",            "–$18.8B (GAAP)",   "Mostly non-cash write-downs ⚠"),
    ]
    cols4 = st.columns(4)
    for i, (lbl, val, sig) in enumerate(fps):
        cols4[i%4].markdown(f"""
        <div class="fp-card">
          <div class="fp-label">{lbl}</div>
          <div class="fp-value">{val}</div>
          <div class="fp-signal">{sig}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="q-card-blue" style="margin-top:1rem;">
      <b style="color:{BLUE_DARK};">The Defining Characteristic: Voluntary Reinvestment</b><br>
      <span style="font-size:0.88rem;color:#0c2a4a;">
        Intel is a mature company that has <b>voluntarily re-entered the investment phase</b>.
        In 2024, Intel invested \$23.9B in capital expenditures while generating only \$8.3B in
        operating cash flow. The gap — \$15.6B of cash consumption — is the price tag of
        transformation. The dividend is gone. Buybacks are gone. Every dollar of cash flow,
        and then some, is being directed into factories and research.
        <b>The company is asking shareholders to wait.</b>
      </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-head">The Two Paths Forward</div>', unsafe_allow_html=True)
    p1, p2 = st.columns(2)
    with p1:
        st.markdown(f"""
        <div class="scen-card" style="background:{GREEN_LIGHT};border-top:3px solid {GREEN};">
          <b style="color:{GREEN};">Recovery Path (50% probability)</b><br>
          <span style="font-size:0.84rem;color:#1A3A2A;">
            Intel 18A achieves required yields by FY2026. Panther Lake ships on schedule.
            First external foundry customers place meaningful orders. Revenue recovers toward
            \$70–73B by FY2029. EBIT margins expand from zero toward 14–16%.
            FCF turns positive. Dividend returns. Company earns cost of capital again.<br>
            <b>Intrinsic value: \$30–34</b>
          </span>
        </div>
        """, unsafe_allow_html=True)
    with p2:
        st.markdown(f"""
        <div class="scen-card" style="background:{RED_LIGHT};border-top:3px solid {RED};">
          <b style="color:{RED};">Decline Path (25% probability)</b><br>
          <span style="font-size:0.84rem;color:#6B1A1A;">
            18A yields disappoint. Foundry customers stay with TSMC. AMD takes more server share.
            Intel becomes well-financed but strategically diminished — still profitable in PCs
            and legacy enterprise, but no longer at the frontier. Revenue stabilises at
            \$50–55B with thin margins.<br>
            <b>Intrinsic value: \$14–16 (stock is a value trap)</b>
          </span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Three Inflection Points That Will Define the Decade</div>', unsafe_allow_html=True)
    inf_df = pd.DataFrame([
        {"Inflection":"Intel 18A Yields Hit Target","The Test":"Can Intel manufacture competitive chips at scale?","Timeline":"FY2025–FY2026","If Met":"External customers commit; foundry revenue grows; transformation narrative validated","If Missed":"Losses mount; outsource to TSMC; semi-fabless = 8-10% margins; bear case"},
        {"Inflection":"Gaudi 3 Market Traction","The Test":"Can Intel build an AI accelerator ecosystem?","Timeline":"FY2026–FY2028","If Met":"5–8% AI market share; developer ecosystem starts; NVIDIA pricing leverage reduced","If Missed":"AI miss becomes permanent; Gaudi 4 becomes a science project"},
        {"Inflection":"FCF Inflection Positive","The Test":"Does capex peak and earnings recover simultaneously?","Timeline":"FY2026–FY2027","If Met":"Dividend returns; institutional investors re-engage; P/B re-rates above 1×","If Missed":"Equity issuance risk; balance sheet stress; value trap confirmed"},
    ])
    st.dataframe(inf_df, use_container_width=True, hide_index=True)

    st.markdown(f"""
    <div class="pullquote">
      Intel is a mature company that has voluntarily re-entered the investment phase.
      This is its defining characteristic — and the single most important fact for any
      investor considering the stock. The question is not whether Intel was great.
      It was. The question is whether the thing being built is worth the wait.
    </div>
    """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE 7 — MARKETING STRATEGY
# ═════════════════════════════════════════════════════════════════════════════
elif PAGE == "🎯  Marketing Strategy":
    st.markdown('<div class="narrative">Marketing strategy that ignores life cycle is not strategy — it is aspiration. Intel in 2026 cannot market with the confidence of a monopolist, because it is not one. But it cannot abandon its heritage, because the heritage is the only thing keeping enterprise customers loyal during the transition. The strategy must be honest about what Intel is: a company in the middle of the most ambitious corporate transformation in semiconductor history.</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head">The Three Narratives Intel Must Own</div>', unsafe_allow_html=True)
    n1, n2, n3 = st.columns(3)
    with n1:
        st.markdown(f"""
        <div class="q-card-blue">
          <b style="color:{BLUE_DARK};">Narrative 1: Enterprise Loyalty</b><br>
          <span style="font-size:0.84rem;color:#0c2a4a;">
            For enterprise IT buyers: <i>"We have never stopped being the most trusted
            platform for enterprise workloads. Xeon 6 is competitive. Core Ultra with
            built-in NPU lets your employees run AI on-device without sending data
            to the cloud."</i><br>
            Conservative, honest, leverages heritage + new AI capability.
          </span>
        </div>
        """, unsafe_allow_html=True)
    with n2:
        st.markdown(f"""
        <div class="q-card-cyan">
          <b style="color:{BLUE_DARK};">Narrative 2: Developer Independence</b><br>
          <span style="font-size:0.84rem;color:#0c2a4a;">
            For AI developers: <i>"You have built your career on software that only runs
            on one company's hardware. When that company controls supply, you lose leverage.
            Intel's oneAPI and OpenVINO provide hardware-agnostic AI development.
            Independence is a feature, not a fallback."</i>
          </span>
        </div>
        """, unsafe_allow_html=True)
    with n3:
        st.markdown(f"""
        <div class="q-card-steel">
          <b style="color:{BLUE_DARK};">Narrative 3: Foundry Sovereignty</b><br>
          <span style="font-size:0.84rem;color:#0c2a4a;">
            For governments and strategic customers: <i>"The world runs on chips made
            in Taiwan. That is an extraordinary geopolitical risk. Intel is the only
            Western company with the manufacturing capability to offer a credible
            alternative. The CHIPS Act is a down payment on resilience."</i>
          </span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Ansoff Matrix — Strategic Growth Directions</div>', unsafe_allow_html=True)
    a1, a2 = st.columns(2)
    ansoff_items = [
        ("Market Penetration","Existing Products × Existing Markets","MODERATE",STEEL,"tag-steel",
         ["Defend PC CPU leadership via AI PC differentiation — Core Ultra NPU as key selling point",
          "Xeon 6: match AMD TCO on price-per-core; compete on ecosystem and supply chain depth",
          "QTL equivalent: enforce patent and platform contracts with OEMs aggressively"], a1),
        ("Product Development","New Products × Existing Markets","HIGH ★",BLUE,"tag-blue",
         ["Gaudi 3 AI accelerator: enterprise inference at 40–50% discount to NVIDIA H200",
          "Intel 18A: next-gen manufacturing process; the foundational new product for the foundry business",
          "Core Ultra (AI PC): on-device NPU for GenAI workloads — privacy + performance narrative",
          "oneAPI / OpenVINO: developer platform as the software moat Intel needs to build"], a2),
        ("Market Development","Existing Products × New Markets","HIGH ★",CYAN,"tag-cyan",
         ["Intel Foundry (IFS): sell 18A process to fabless companies and government customers globally",
          "US & EU government contracts: defence, intelligence, sovereign chip manufacturing",
          "Emerging market AI infrastructure: partner with sovereign AI programmes (India, EU, Middle East)",
          "Data centre AI inference: Gaudi 3 for cloud providers wanting NVIDIA price relief"], a1),
        ("Diversification","New Products × New Markets","LOW",GOLD,"tag-gold",
         ["Avoid new businesses not in semiconductor design or manufacturing — stay focused",
          "Mobileye (automotive vision): already partially public; manage carefully, avoid distraction",
          "Capital discipline: the worst strategic error would be to dilute attention during transformation"], a2),
    ]
    for title, sub, rec, col, tag_cls, actions, target_col in ansoff_items:
        target_col.markdown(f"""
        <div class="ansoff-card" style="border-top:3px solid {col};">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
            <div>
              <div class="ansoff-title">{title}</div>
              <div class="ansoff-sub">{sub}</div>
            </div>
            <span class="{tag_cls}">{rec}</span>
          </div>
          {''.join(f'<div class="ansoff-item">› {a}</div>' for a in actions)}
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Pricing Architecture — Three Markets, Three Philosophies</div>', unsafe_allow_html=True)
    pricing_df = pd.DataFrame([
        {"Product":"Core Ultra (AI PC)","Pricing Philosophy":"Premium — AI NPU justifies ASP increase","vs. Competition":"+5–8% ASP vs prior gen AMD","Financial Implication":"+1.0 pp gross margin by FY2027"},
        {"Product":"Xeon 6 (Server CPU)","Pricing Philosophy":"Value-parity — match AMD TCO; compete on ecosystem","vs. Competition":"Slight discount to AMD on price/core","Financial Implication":"Margin pressure; offset by volume stabilisation"},
        {"Product":"Gaudi 3 (AI Accel.)","Pricing Philosophy":"Aggressive penetration — 40–50% discount to NVIDIA","vs. Competition":"~$15K vs NVIDIA H200 ~$25–30K","Financial Implication":"Near-term GM sacrifice for market entry; ecosystem investment"},
        {"Product":"Intel Foundry (18A)","Pricing Philosophy":"Geo-premium — charge for 'Made in USA/EU'","vs. Competition":"5–10% premium to TSMC equivalent","Financial Implication":"Offsets lower scale economics; justifiable to govt. customers"},
    ])
    st.dataframe(pricing_df, use_container_width=True, hide_index=True)

    st.markdown('<div class="sec-head">Communication Strategy — Four Audiences, Four Messages</div>', unsafe_allow_html=True)
    comm_df = pd.DataFrame([
        {"Audience":"PC Consumers / OEMs","Primary Message":"Intel AI PC — Your AI, Built In","Key Channel":"OEM co-op ($1.5B/yr budget); digital; retail co-branding","Metric of Success":"AI PC units shipped; ASP premium vs AMD"},
        {"Audience":"Data Centre Architects","Primary Message":"Xeon 6 + Gaudi 3: Open AI Infrastructure","Key Channel":"Trade shows; direct field sales; developer conferences","Metric of Success":"Gaudi 3 POC deployments; design wins; Xeon 6 vs AMD wins"},
        {"Audience":"AI / ML Developers","Primary Message":"Build Once, Run Anywhere — Intel's Open AI Stack","Key Channel":"GitHub; PyPI; devCloud; hackathons; university labs","Metric of Success":"oneAPI downloads; benchmark citations; open-source PRs"},
        {"Audience":"Foundry Prospects","Primary Message":"Made in America. Built to Scale. CHIPS-Backed.","Key Channel":"Government relations; CEO-level BD; defence trade shows","Metric of Success":"LOIs signed; first external tape-out completions; yield data"},
        {"Audience":"Financial Investors","Primary Message":"Execution proof-points, quarter by quarter","Key Channel":"Earnings calls; Technology Day events; IR roadshows","Metric of Success":"18A yield rates; Foundry revenue milestones; FCF inflection"},
    ])
    st.dataframe(comm_df, use_container_width=True, hide_index=True)

    st.markdown('<div class="sec-head">4Ps Operational Audit — What Needs Fixing Now</div>', unsafe_allow_html=True)
    fourp = pd.DataFrame([
        {"Lever":"Product","The Gap Today":"18A unproven at scale; Gaudi 3 benchmark-competitive but ecosystem-poor; Core Ultra AI claims unsubstantiated by real workloads","Required Action (FY26–28)":"Ship Panther Lake on time. Deliver 18A yield data publicly. Gaudi 3: 5 public enterprise case studies. Core Ultra: OEM benchmark co-marketing.","Financial Impact":"Every quarter of execution re-rates the stock 10–15%"},
        {"Lever":"Price","The Gap Today":"No clear pricing strategy communicated to market; Gaudi 3 discounts ad hoc","Required Action (FY26–28)":"Formalise geo-premium for IFS. Gaudi 3 published pricing vs NVIDIA. Core Ultra ASP target $+20 vs Core i9.","Financial Impact":"IFS geo-premium: +200 bps gross margin on foundry; Gaudi market entry"},
        {"Lever":"Place (Channel)","The Gap Today":"Enterprise direct sales team depleted during restructuring; foundry business development nascent","Required Action (FY26–28)":"Rebuild dedicated foundry BD team (50+ senior reps). OEM AI PC co-op programs. Government relations team expansion.","Financial Impact":"Foundry revenue: $0 → $6B by FY2029 requires 3-yr customer development now"},
        {"Lever":"Promotion","The Gap Today":"Under-communicating transformation progress; developers don't believe Intel is serious about AI; no clear brand platform","Required Action (FY26–28)":"'Intel is back' campaign with proof, not promises. Developer relations investment: $500M/yr. Quarterly 18A progress disclosures.","Financial Impact":"Credibility = customer commitments = revenue = FCF inflection"},
    ])
    st.dataframe(fourp, use_container_width=True, hide_index=True)

    st.markdown(f"""
    <div class="pullquote">
      Intel\'s marketing strategy should not pretend the last five years did not happen.
      The stumbles are known. What Intel can do — and what its best moments of communication
      have always done — is tell a compelling, honest story about what it is building and why
      it will matter. Credibility is built incrementally, through delivered promises, not
      through louder advertising.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Strategy Coherence Audit — 6-Point Consistency Check</div>', unsafe_allow_html=True)
    audit = pd.DataFrame([
        {"Dimension":"Growth Direction (Ansoff)","Strategy":"Product Dev (IFS/Gaudi) + Market Dev (Foundry/Govt)","LC Consistent?":"✅ Yes — Crisis Reinvestment stage requires new platform","Financial Consistent?":"✅ Yes — Capex sustains both simultaneously","Conflict?":"None"},
        {"Dimension":"Competitive Positioning","Strategy":"Challenger pricing (Gaudi) + Heritage premium (CPU) + Geo-premium (IFS)","LC Consistent?":"✅ Yes — cannot act as monopolist; must buy share","Financial Consistent?":"⚠ Tension — Gaudi margin sacrifice vs CPU margin defence","Conflict?":"Margin mix complexity; manageable"},
        {"Dimension":"Pricing Strategy","Strategy":"Premium AI PC + Value server + Penetration AI + Geo-premium foundry","LC Consistent?":"✅ Yes — crisis stage requires market entry pricing","Financial Consistent?":"✅ Yes — modelled in margin ramp path","Conflict?":"None"},
        {"Dimension":"Channel Strategy","Strategy":"OEM co-op (consumer) + Direct field sales (enterprise) + B2G (foundry)","LC Consistent?":"✅ Yes — matches three distinct customer types","Financial Consistent?":"✅ Yes — SG&A recovery path accommodates","Conflict?":"None"},
        {"Dimension":"Promotion","Strategy":"Proof-based credibility campaign; developer investment; government relations","LC Consistent?":"✅ Yes — trust, not hype, is what transformation companies need","Financial Consistent?":"✅ Yes — $500M dev budget within R&D guidance","Conflict?":"None"},
        {"Dimension":"Capital Allocation","Strategy":"Sustain $20–24B capex; no dividend until FCF positive; \$7.86B CHIPS funding","LC Consistent?":"✅ Yes — crisis reinvestment stage demands it","Financial Consistent?":"✅ Yes — external co-investment (Apollo, Brookfield) bridges gap","Conflict?":"None"},
    ])
    st.dataframe(audit, use_container_width=True, hide_index=True)


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE 8 — LIVE NEWS
# ═════════════════════════════════════════════════════════════════════════════
elif PAGE == "📰  Live News":
    st.markdown('<div class="narrative">For Intel, news flow is not background noise — it is the transformation scorecard. Every headline about 18A yields, foundry customer wins, Gaudi deployments, or AMD design victories directly updates the probability distribution of the base vs. bear vs. bull case. Read it analytically, not emotionally.</div>', unsafe_allow_html=True)

    news = get_live_news()
    pos_n = sum(1 for n in news if n["sentiment"] == "positive")
    neg_n = sum(1 for n in news if n["sentiment"] == "negative")
    neu_n = sum(1 for n in news if n["sentiment"] == "neutral")

    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Total Headlines", f"{len(news)}")
    s2.metric("Positive ✅",     f"{pos_n}")
    s3.metric("Neutral ⬜",      f"{neu_n}")
    s4.metric("Negative ❌",     f"{neg_n}")

    sf = st.selectbox("Filter by sentiment", ["All","positive","neutral","negative"])
    filtered = news if sf == "All" else [n for n in news if n["sentiment"] == sf]

    css_map = {"positive":"news-pos","negative":"news-neg","neutral":"news-neu"}
    tag_map  = {
        "positive": f'<span class="tag-green">positive</span>',
        "negative": f'<span class="tag-red">negative</span>',
        "neutral":  f'<span class="tag-blue">neutral</span>',
    }

    st.markdown("")
    for item in filtered:
        link_html = (
            f'<a href="{item["link"]}" target="_blank" '
            f'style="font-size:0.72rem;color:{BLUE};text-decoration:none;font-weight:600;">Read →</a>'
            if item["link"] != "#" else ""
        )
        st.markdown(f"""
        <div class="{css_map[item['sentiment']]}">
          <div class="news-title">{item['title']}</div>
          <div class="news-meta">
            {tag_map[item['sentiment']]} &nbsp; {item['date']} &nbsp; {link_html}
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-head">News Sentiment Distribution</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])
    with c1:
        sent_fig = go.Figure(go.Pie(
            labels=["Positive","Neutral","Negative"],
            values=[max(pos_n,1), max(neu_n,1), max(neg_n,1)],
            hole=0.52,
            marker_colors=[GREEN, STEEL, RED],
            textinfo="label+percent",
            textfont=dict(color="#1A1A2E", size=12)
        ))
        sent_fig.update_layout(height=260, paper_bgcolor="#FFFFFF",
                               margin=dict(l=20,r=20,t=20,b=20),
                               font=dict(color="#1A1A2E"),
                               legend=dict(font=dict(color="#1A1A2E")))
        st.plotly_chart(sent_fig, use_container_width=True)
    with c2:
        st.markdown(f"""
        <div class="q-card-blue">
          <b style="color:{BLUE_DARK};">How to Read Intel News Flow</b><br>
          <span style="font-size:0.85rem;color:#0c2a4a;">
            <b>High-signal headlines</b>: 18A yield rate disclosures, external foundry LOIs/tape-outs,
            Gaudi 3 enterprise deployments, Panther Lake shipment milestones, FCF quarterly trend,
            AMD server share data, government CHIPS Act disbursement timing.<br><br>
            <b>Low-signal noise</b>: Stock analyst price target changes, broad semi-sector commentary,
            non-Intel AI news, geopolitical speculation unrelated to CHIPS Act.<br><br>
            <b>Watch for</b>: Any 18A yield announcement (most binary signal), Q1 FY2026 earnings
            guidance vs actuals, first external foundry customer tape-out announcement.
          </span>
        </div>
        <div class="q-card-gold">
          <b style="color:{GOLD};">Key Upcoming Catalysts (FY2026)</b><br>
          <span style="font-size:0.83rem;color:#6B4500;">
            · Q1 FY2026 Earnings (Expected ~Apr 2026)<br>
            · Intel Technology Day 2026 (18A yield / Panther Lake update)<br>
            · CHIPS Act first disbursement from \$7.86B award<br>
            · First external foundry customer tape-out on 18A<br>
            · Gaudi 3 volume ramp update and customer wins<br>
            · Panther Lake consumer launch (H2 2026 target)
          </span>
        </div>
        """, unsafe_allow_html=True)


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
  Intel Corporation Research Terminal &nbsp;|&nbsp;
  Live data: Yahoo Finance &nbsp;|&nbsp;
  Fundamentals: Intel 10-K FY2020–2024, Earnings Releases &nbsp;|&nbsp;
  News: Google News RSS &nbsp;|&nbsp;
  Framework: Damodaran (NYU Stern) &nbsp;|&nbsp;
  {datetime.now().strftime("%d %B %Y  %H:%M")} &nbsp;|&nbsp;
  Prepared by: Aditi Ranjan · BBA Corporate Finance &nbsp;|&nbsp;
  <b>Academic use only — not investment advice</b>
</div>
""", unsafe_allow_html=True)
