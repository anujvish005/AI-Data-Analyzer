import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
import os
from datetime import datetime
from groq import Groq

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DataLens AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Design System & CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

:root {
    --cream:       #faf8f5;
    --white:       #ffffff;
    --sand:        #f0ece4;
    --sand-dark:   #e4ddd2;
    --sage:        #7a9e87;
    --sage-light:  #d4e6da;
    --sage-pale:   #eef5f1;
    --terracotta:  #c47b5a;
    --terra-pale:  #f5ebe4;
    --slate:       #3d4a5c;
    --slate-mid:   #6b7a8d;
    --slate-light: #9aa5b1;
    --ink:         #1e2530;
    --border:      #e8e2d9;
    --shadow-sm:   0 1px 3px rgba(61,74,92,0.08);
    --shadow-md:   0 4px 16px rgba(61,74,92,0.10);
    --radius-sm:   8px;
    --radius-md:   14px;
    --radius-lg:   20px;
}

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; color: var(--ink); }
.stApp { background: var(--cream); }
[data-testid="stSidebar"] { background: var(--white); border-right: 1px solid var(--border); }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--sand); }
::-webkit-scrollbar-thumb { background: var(--sand-dark); border-radius: 10px; }

/* Hero */
.hero {
    background: linear-gradient(135deg, #ffffff 0%, #f0ece4 50%, #eef5f1 100%);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 2.2rem 2.8rem;
    margin-bottom: 1.8rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: var(--shadow-sm);
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute; top: -50px; right: -50px;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(122,158,135,0.13) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-badge {
    display: inline-block;
    background: var(--sage-pale);
    color: var(--sage);
    border: 1px solid var(--sage-light);
    border-radius: 20px;
    padding: 0.2rem 0.85rem;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.65rem;
    font-family: 'DM Mono', monospace;
}
.hero h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 2.5rem;
    color: var(--ink);
    margin: 0 0 0.35rem 0;
    line-height: 1.15;
    font-weight: 400;
}
.hero h1 em { font-style: italic; color: var(--sage); }
.hero-sub { color: var(--slate-mid); font-size: 0.9rem; margin: 0; }
.hero-icon { font-size: 4.5rem; opacity: 0.15; line-height: 1; }

/* Stat Cards */
.stat-row { display: flex; gap: 0.8rem; margin-bottom: 1.5rem; }
.stat-card {
    flex: 1;
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 1rem 1.1rem;
    text-align: center;
    box-shadow: var(--shadow-sm);
    position: relative;
    overflow: hidden;
    transition: box-shadow 0.2s, transform 0.2s;
}
.stat-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--sage), var(--terracotta));
}
.stat-card:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); }
.stat-val { font-family: 'DM Serif Display', serif; font-size: 1.85rem; color: var(--ink); line-height: 1.1; }
.stat-lbl { font-size: 0.68rem; color: var(--slate-light); text-transform: uppercase; letter-spacing: 0.1em; margin-top: 0.2rem; font-weight: 500; }

/* Section Label */
.sec-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem; color: var(--slate-light);
    text-transform: uppercase; letter-spacing: 0.18em;
    margin-bottom: 0.8rem;
    display: flex; align-items: center; gap: 0.5rem;
}
.sec-label::after { content: ''; flex: 1; height: 1px; background: var(--border); }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--sand);
    border-radius: var(--radius-md);
    padding: 4px; gap: 2px;
    border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.82rem; font-weight: 500;
    color: var(--slate-mid);
    border-radius: var(--radius-sm);
    padding: 0.45rem 1rem;
}
.stTabs [aria-selected="true"] {
    background: var(--white) !important;
    color: var(--ink) !important;
    box-shadow: var(--shadow-sm) !important;
    font-weight: 600 !important;
}

/* Buttons */
.stButton > button {
    background: var(--ink); color: #fff;
    border: none; border-radius: var(--radius-sm);
    font-family: 'DM Sans', sans-serif;
    font-size: 0.84rem; font-weight: 500;
    padding: 0.6rem 1.4rem;
    transition: all 0.2s;
    box-shadow: var(--shadow-sm);
}
.stButton > button:hover { background: var(--slate); transform: translateY(-1px); box-shadow: var(--shadow-md); }

/* Inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--white) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--ink) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--sage) !important;
    box-shadow: 0 0 0 3px rgba(122,158,135,0.15) !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: var(--white) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--ink) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
}

/* File Uploader */
[data-testid="stFileUploader"] {
    background: var(--white);
    border: 2px dashed var(--sand-dark);
    border-radius: var(--radius-md);
    transition: border-color 0.2s, background 0.2s;
}
[data-testid="stFileUploader"]:hover { border-color: var(--sage); background: var(--sage-pale); }

/* Dataframe */
.stDataFrame { border-radius: var(--radius-md) !important; border: 1px solid var(--border) !important; }

/* Alerts */
.stSuccess > div { background: var(--sage-pale) !important; border-color: var(--sage) !important; border-radius: var(--radius-sm) !important; }
.stWarning > div { background: #fef9ec !important; border-radius: var(--radius-sm) !important; }
.stInfo > div    { background: #eef4fb !important; border-radius: var(--radius-sm) !important; }
.stError > div   { background: #fdf0ee !important; border-color: var(--terracotta) !important; border-radius: var(--radius-sm) !important; }

/* Download Button */
.stDownloadButton > button {
    background: var(--white) !important; color: var(--ink) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important; font-weight: 500 !important;
    width: 100% !important;
}
.stDownloadButton > button:hover { border-color: var(--sage) !important; color: var(--sage) !important; background: var(--sage-pale) !important; }

/* Sidebar logo */
.sidebar-logo {
    display: flex; align-items: center; gap: 0.6rem;
    padding: 0 1rem 1.5rem 1rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.5rem;
}
.sidebar-logo-mark {
    width: 32px; height: 32px;
    background: linear-gradient(135deg, var(--sage), var(--terracotta));
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    color: white; font-size: 1rem; font-weight: 700; flex-shrink: 0;
}
.sidebar-logo-name { font-family: 'DM Serif Display', serif; font-size: 1.1rem; color: var(--ink); }
.sidebar-logo-sub { font-family: 'DM Mono', monospace; font-size: 0.6rem; color: var(--slate-light); letter-spacing: 0.06em; }
.sidebar-sec-lbl {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem; color: var(--slate-light);
    text-transform: uppercase; letter-spacing: 0.15em;
    margin-bottom: 0.5rem; padding: 0 0.5rem;
}

/* AI Response */
.ai-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-left: 3px solid var(--sage);
    border-radius: var(--radius-md);
    padding: 1.5rem 1.8rem;
    box-shadow: var(--shadow-sm);
    font-size: 0.9rem; line-height: 1.85;
    color: var(--slate);
    white-space: pre-wrap; word-wrap: break-word;
}

/* Chat */
.chat-msg { display: flex; gap: 0.7rem; align-items: flex-start; margin-bottom: 0.8rem; }
.chat-avatar {
    width: 28px; height: 28px; border-radius: 50%;
    flex-shrink: 0; display: flex; align-items: center;
    justify-content: center; font-size: 0.72rem; font-weight: 600;
}
.chat-avatar.user { background: var(--sand); color: var(--slate); border: 1px solid var(--border); }
.chat-avatar.ai   { background: linear-gradient(135deg, var(--sage), var(--terracotta)); color: white; }
.chat-bubble { max-width: calc(100% - 40px); padding: 0.7rem 1rem; border-radius: var(--radius-sm); font-size: 0.87rem; line-height: 1.65; }
.chat-bubble.user { background: var(--sand); color: var(--ink); border: 1px solid var(--border); }
.chat-bubble.ai   { background: var(--white); color: var(--slate); border: 1px solid var(--border); box-shadow: var(--shadow-sm); white-space: pre-wrap; }

/* Landing */
.landing {
    background: var(--white);
    border: 2px dashed var(--sand-dark);
    border-radius: var(--radius-lg);
    padding: 4rem 2rem; text-align: center; margin-top: 0.5rem;
}
.landing-icon { font-size: 3rem; margin-bottom: 0.8rem; opacity: 0.5; }
.landing h3 { font-family: 'DM Serif Display', serif; font-size: 1.5rem; color: var(--ink); margin: 0 0 0.5rem 0; font-weight: 400; }
.landing p  { color: var(--slate-mid); font-size: 0.87rem; line-height: 1.7; margin: 0 0 1.5rem 0; }
.feature-chips { display: flex; flex-wrap: wrap; gap: 0.5rem; justify-content: center; }
.feature-chip {
    background: var(--sand); border: 1px solid var(--border);
    border-radius: 20px; padding: 0.3rem 0.8rem;
    font-size: 0.75rem; color: var(--slate-mid); font-weight: 500;
}

label { font-family: 'DM Sans', sans-serif !important; font-size: 0.82rem !important; font-weight: 500 !important; color: var(--slate) !important; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def get_groq_client():
    api_key = st.session_state.get("groq_api_key", "") or os.getenv("GROQ_API_KEY", "")
    return Groq(api_key=api_key) if api_key else None

def analyze_with_ai(client, prompt, model):
    r = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7, max_tokens=2048,
    )
    return r.choices[0].message.content

def df_summary(df):
    return f"""Shape: {df.shape[0]} rows × {df.shape[1]} columns
Columns: {', '.join(df.columns.tolist())}
Types:\n{df.dtypes.to_string()}
Stats:\n{df.describe(include='all').to_string()}
Nulls:\n{df.isnull().sum().to_string()}
Sample (30 rows):\n{df.head(30).to_string()}"""

PALETTE = ["#7a9e87","#c47b5a","#e8c547","#7aace8","#b07aad","#5a9ec4","#d4765a","#5aad8f"]

def chart_layout():
    return dict(
        paper_bgcolor="#ffffff", plot_bgcolor="#faf8f5",
        font=dict(family="DM Sans", color="#6b7a8d", size=11),
        title_font=dict(family="DM Serif Display", size=15, color="#1e2530"),
        xaxis=dict(gridcolor="#e8e2d9", showgrid=True, zeroline=False),
        yaxis=dict(gridcolor="#e8e2d9", showgrid=True, zeroline=False),
        margin=dict(l=40, r=20, t=50, b=40),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )

def auto_charts(df):
    num = df.select_dtypes(include='number').columns.tolist()
    cat = df.select_dtypes(include=['object','category']).columns.tolist()
    charts = []

    if len(num) >= 2:
        fig = px.imshow(df[num].corr(), text_auto=".2f",
                        color_continuous_scale=["#f5ebe4","#e4ddd2","#7a9e87"],
                        title="Correlation Heatmap")
        fig.update_layout(**chart_layout())
        charts.append(fig)

    if num:
        fig = px.histogram(df, x=num[0], nbins=30, title=f"Distribution — {num[0]}",
                           color_discrete_sequence=["#7a9e87"])
        fig.update_layout(**chart_layout())
        charts.append(fig)

    if cat and num:
        top = df[cat[0]].value_counts().head(12).index
        grp = df[df[cat[0]].isin(top)].groupby(cat[0])[num[0]].mean().reset_index()
        fig = px.bar(grp, x=cat[0], y=num[0], color=cat[0],
                     title=f"Avg {num[0]} by {cat[0]}",
                     color_discrete_sequence=PALETTE)
        fig.update_layout(**chart_layout(), showlegend=False)
        charts.append(fig)

    if len(num) >= 2:
        fig = px.scatter(df, x=num[0], y=num[1], color=cat[0] if cat else None,
                         opacity=0.65, title=f"{num[0]} vs {num[1]}",
                         color_discrete_sequence=PALETTE)
        fig.update_layout(**chart_layout())
        charts.append(fig)

    if cat and num:
        top = df[cat[0]].value_counts().head(10).index
        fig = px.box(df[df[cat[0]].isin(top)], x=cat[0], y=num[0],
                     color=cat[0], title=f"Box Plot — {num[0]}",
                     color_discrete_sequence=PALETTE)
        fig.update_layout(**chart_layout(), showlegend=False)
        charts.append(fig)

    return charts


# ── Session state ─────────────────────────────────────────────────────────────
for k, v in [("chat_history",[]), ("groq_api_key",""), ("df",None)]:
    if k not in st.session_state:
        st.session_state[k] = v


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-mark">✦</div>
        <div>
            <div class="sidebar-logo-name">DataLens</div>
            <div class="sidebar-logo-sub">AI · Powered by Groq</div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sidebar-sec-lbl">API Key</div>', unsafe_allow_html=True)
    key_in = st.text_input("Groq API Key", type="password",
                           placeholder="Paste your gsk_... key",
                           value=st.session_state.groq_api_key,
                           label_visibility="collapsed",
                           help="Free key at console.groq.com")
    if key_in:
        st.session_state.groq_api_key = key_in
    if st.session_state.groq_api_key:
        st.success("✓ Key saved for this session")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sec-lbl">AI Model</div>', unsafe_allow_html=True)
    model = st.selectbox("Model", ["llama-3.3-70b-versatile","llama-3.1-8b-instant","mixtral-8x7b-32768","gemma2-9b-it"], label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sec-lbl">Analysis Mode</div>', unsafe_allow_html=True)
    analysis_type = st.selectbox("Mode", ["General Insights","Statistical Deep Dive","Business Intelligence","Anomaly Detection","Predictive Patterns"], label_visibility="collapsed")

    if st.session_state.df is not None:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="sidebar-sec-lbl">Export</div>', unsafe_allow_html=True)
        buf = io.StringIO()
        st.session_state.df.describe(include='all').to_csv(buf)
        st.download_button("⬇  Stats CSV", data=buf.getvalue(),
                           file_name=f"stats_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", mime="text/csv")
        if st.session_state.chat_history:
            log = "\n\n".join([f"{'YOU' if m['role']=='user' else 'AI'}: {m['content']}" for m in st.session_state.chat_history])
            st.download_button("⬇  Chat Log", data=log,
                               file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt", mime="text/plain")
        if st.button("🗑  Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()

    st.markdown("""<br><div style="padding:0 0.5rem;">
    <p style="font-size:0.7rem;color:#9aa5b1;line-height:1.8;margin:0;">
    Your data stays in your browser.<br>API key is session-only.<br>
    Built with Streamlit + Groq.
    </p></div>""", unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div>
        <div class="hero-badge">✦ AI-Powered Analytics</div>
        <h1>DataLens <em>AI</em></h1>
        <p class="hero-sub">Upload any CSV · Visualize instantly · Chat with your data in plain English</p>
    </div>
    <div class="hero-icon">◎</div>
</div>""", unsafe_allow_html=True)

if not st.session_state.groq_api_key:
    st.warning("Add your free Groq API key in the sidebar to enable AI features → [console.groq.com](https://console.groq.com)")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"], help="Up to 200MB")


# ── App Body ──────────────────────────────────────────────────────────────────
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.session_state.df = df
    num_cols = df.select_dtypes(include='number').columns.tolist()
    cat_cols = df.select_dtypes(include=['object','category']).columns.tolist()

    # Stat cards
    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-card"><div class="stat-val">{df.shape[0]:,}</div><div class="stat-lbl">Rows</div></div>
        <div class="stat-card"><div class="stat-val">{df.shape[1]}</div><div class="stat-lbl">Columns</div></div>
        <div class="stat-card"><div class="stat-val">{len(num_cols)}</div><div class="stat-lbl">Numeric</div></div>
        <div class="stat-card"><div class="stat-val">{len(cat_cols)}</div><div class="stat-lbl">Text Cols</div></div>
        <div class="stat-card"><div class="stat-val">{df.isnull().sum().sum():,}</div><div class="stat-lbl">Missing</div></div>
    </div>""", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["  📋 Data Preview  ","  📊 Visualize  ","  🤖 AI Analysis  ","  💬 Chat  "])

    # ── Tab 1 ─────────────────────────────────────────────────────────────────
    with tab1:
        st.markdown('<div class="sec-label">Raw Data</div>', unsafe_allow_html=True)
        rows = st.slider("Rows to preview", 5, min(200, len(df)), 20)
        st.dataframe(df.head(rows))

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<br><div class="sec-label">Column Info</div>', unsafe_allow_html=True)
            st.dataframe(pd.DataFrame({
                "Column": df.columns, "Type": df.dtypes.astype(str).values,
                "Non-Null": df.notnull().sum().values,
                "Nulls": df.isnull().sum().values,
                "Unique": df.nunique().values,
            }), hide_index=True)
        with c2:
            st.markdown('<br><div class="sec-label">Summary Statistics</div>', unsafe_allow_html=True)
            st.dataframe(df.describe(include='all').T)

    # ── Tab 2 ─────────────────────────────────────────────────────────────────
    with tab2:
        st.markdown('<div class="sec-label">Auto-Generated Charts</div>', unsafe_allow_html=True)
        charts = auto_charts(df)
        if not charts:
            st.info("Need more numeric/categorical columns to auto-generate charts.")
        else:
            for i in range(0, len(charts), 2):
                cols = st.columns(2)
                for j in range(2):
                    if i+j < len(charts):
                        with cols[j]: st.plotly_chart(charts[i+j])

        st.markdown("---")
        st.markdown('<div class="sec-label">Custom Chart Builder</div>', unsafe_allow_html=True)
        all_cols = df.columns.tolist()
        cb1, cb2, cb3, cb4 = st.columns(4)
        with cb1: ctype = st.selectbox("Chart", ["Bar","Line","Scatter","Histogram","Box","Pie"])
        with cb2: xcol  = st.selectbox("X Axis", all_cols)
        with cb3: ycol  = st.selectbox("Y Axis", num_cols if num_cols else all_cols)
        with cb4: ccol  = st.selectbox("Color By", ["None"] + cat_cols)
        carg = None if ccol == "None" else ccol

        if st.button("Generate Chart ↗"):
            try:
                kw = dict(color_discrete_sequence=PALETTE)
                if   ctype == "Bar":       fig = px.bar(df, x=xcol, y=ycol, color=carg, **kw)
                elif ctype == "Line":      fig = px.line(df, x=xcol, y=ycol, color=carg, **kw)
                elif ctype == "Scatter":   fig = px.scatter(df, x=xcol, y=ycol, color=carg, opacity=0.7, **kw)
                elif ctype == "Histogram": fig = px.histogram(df, x=xcol, color=carg, nbins=30, **kw)
                elif ctype == "Box":       fig = px.box(df, x=carg, y=ycol, color=carg, **kw)
                elif ctype == "Pie":
                    vc = df[xcol].value_counts().head(10)
                    fig = px.pie(values=vc.values, names=vc.index, color_discrete_sequence=PALETTE)
                fig.update_layout(**chart_layout())
                st.plotly_chart(fig)
            except Exception as e:
                st.error(f"Chart error: {e}")

    # ── Tab 3 ─────────────────────────────────────────────────────────────────
    with tab3:
        st.markdown('<div class="sec-label">AI-Powered Analysis</div>', unsafe_allow_html=True)
        PROMPTS = {
            "General Insights":      "Analyze this dataset and provide comprehensive insights — patterns, trends, notable findings, and actionable recommendations.",
            "Statistical Deep Dive": "Perform a detailed statistical analysis covering distributions, outliers, and correlations.",
            "Business Intelligence": "Analyze from a business perspective. Identify KPIs, opportunities, risks, and actionable recommendations.",
            "Anomaly Detection":     "Identify anomalies and unusual patterns. Explain why each stands out and possible causes.",
            "Predictive Patterns":   "Identify patterns useful for prediction. Which variables matter most? What trends are emerging?"
        }
        extra = st.text_area("Additional instructions (optional)",
                             placeholder="e.g. Focus on the revenue column only...", height=70)
        if st.button(f"Run {analysis_type}  →"):
            if not st.session_state.groq_api_key:
                st.error("Add your Groq API key in the sidebar first.")
            else:
                with st.spinner("Analyzing your data…"):
                    try:
                        result = analyze_with_ai(get_groq_client(),
                                                 f"{PROMPTS[analysis_type]}\n\n{extra}\n\n{df_summary(df)}", model)
                        st.success("Analysis complete")
                        st.markdown(f'<div class="ai-card">{result}</div>', unsafe_allow_html=True)
                        st.session_state.chat_history += [
                            {"role":"user",      "content":f"[{analysis_type}] on uploaded dataset"},
                            {"role":"assistant", "content":result}
                        ]
                    except Exception as e:
                        st.error(f"AI error: {e}")

    # ── Tab 4 ─────────────────────────────────────────────────────────────────
    with tab4:
        st.markdown('<div class="sec-label">Chat with your Data</div>', unsafe_allow_html=True)

        for msg in st.session_state.chat_history:
            cls = "user" if msg["role"]=="user" else "ai"
            lbl = "You" if cls=="user" else "AI"
            st.markdown(f"""
            <div class="chat-msg">
                <div class="chat-avatar {cls}">{lbl[0]}</div>
                <div class="chat-bubble {cls}">{msg["content"]}</div>
            </div>""", unsafe_allow_html=True)

        if not st.session_state.chat_history:
            st.markdown('<p style="color:#9aa5b1;font-size:0.84rem;margin-bottom:0.8rem;">Try one of these or ask your own question:</p>', unsafe_allow_html=True)
            suggestions = ["What are the top 3 insights?","Which columns correlate most?","Any outliers to investigate?","What story does this data tell?"]
            sc = st.columns(2)
            for i, s in enumerate(suggestions):
                with sc[i%2]:
                    if st.button(s, key=f"s{i}"):
                        st.session_state["_pq"] = s
                        st.rerun()

        pending = st.session_state.pop("_pq", None)
        ci, cs = st.columns([5,1])
        with ci:
            uq = st.text_input("Question", value=pending or "",
                               placeholder="Ask anything about your data…",
                               label_visibility="collapsed")
        with cs:
            send = st.button("Send →")

        if send and uq.strip():
            if not st.session_state.groq_api_key:
                st.error("Add your Groq API key in the sidebar.")
            else:
                st.session_state.chat_history.append({"role":"user","content":uq})
                with st.spinner("Thinking…"):
                    try:
                        reply = analyze_with_ai(get_groq_client(),
                            f"You are a sharp data analyst. Answer concisely using data.\n\nDATASET:\n{df_summary(df)}\n\nQUESTION: {uq}",
                            model)
                        st.session_state.chat_history.append({"role":"assistant","content":reply})
                        st.rerun()
                    except Exception as e:
                        st.error(f"AI error: {e}")

else:
    st.markdown("""
    <div class="landing">
        <div class="landing-icon">◎</div>
        <h3>Drop a CSV file above to get started</h3>
        <p>DataLens will instantly give you visualizations,<br>statistics, and AI-powered insights about your data.</p>
        <div class="feature-chips">
            <span class="feature-chip">📊 Auto Charts</span>
            <span class="feature-chip">🔍 Smart Statistics</span>
            <span class="feature-chip">🤖 AI Analysis</span>
            <span class="feature-chip">💬 Chat with Data</span>
            <span class="feature-chip">🛠 Chart Builder</span>
            <span class="feature-chip">⬇ Export</span>
        </div>
    </div>""", unsafe_allow_html=True)
