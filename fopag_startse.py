import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="StartSe · FOPAG Dashboard",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── STARTSE CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800;900&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: #060d1f;
    background-image:
        radial-gradient(ellipse 80% 40% at 50% -5%, rgba(0,87,255,0.16) 0%, transparent 65%),
        radial-gradient(ellipse 40% 30% at 85% 85%, rgba(0,40,140,0.1) 0%, transparent 60%);
    color: #e2e8f5;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #070e20 0%, #060c1c 100%) !important;
    border-right: 1px solid rgba(0,87,255,0.18);
}
[data-testid="stSidebar"] * { color: #c8d4e8 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stRadio label {
    color: #5a78a8 !important;
    font-size: 0.68rem !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stMultiSelect > div > div {
    background: #0a1220 !important;
    border-color: rgba(0,87,255,0.2) !important;
}

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #080f22 0%, #091328 60%, #060e1e 100%);
    border: 1px solid rgba(0,87,255,0.22);
    border-radius: 18px;
    padding: 34px 42px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content:''; position:absolute; top:-100px; right:-100px;
    width:350px; height:350px;
    background: radial-gradient(circle, rgba(0,87,255,0.13) 0%, transparent 65%);
    border-radius: 50%;
}
.hero-badge {
    display:inline-flex; align-items:center; gap:7px;
    background: rgba(0,87,255,0.1);
    border: 1px solid rgba(0,87,255,0.28);
    border-radius:100px; padding:4px 14px;
    font-size:0.68rem; font-weight:700;
    text-transform:uppercase; letter-spacing:1.2px; color:#4a8aff;
    margin-bottom:12px;
}
.hero h1 {
    font-family:'Montserrat',sans-serif; font-size:2.3rem; font-weight:900;
    color:#fff; margin:0 0 6px; letter-spacing:-1px; line-height:1.1;
}
.hero h1 em { font-style:normal; color:#0057FF; }
.hero p { color:#3a4d6a; font-size:0.88rem; margin:0; }

/* ── KPI Cards ── */
.kpi {
    background: linear-gradient(145deg,#0b1226,#09101e);
    border: 1px solid rgba(0,87,255,0.16);
    border-radius:16px; padding:22px 20px 18px;
    position:relative; overflow:hidden;
    transition: border-color .2s, transform .2s;
    height: 130px;
}
.kpi:hover { border-color:rgba(0,87,255,0.4); transform:translateY(-2px); }
.kpi-bar {
    position:absolute; top:0; left:0; right:0; height:3px; border-radius:16px 16px 0 0;
}
.kpi-bar.b1 { background:linear-gradient(90deg,#0057FF,#3d8bff); }
.kpi-bar.b2 { background:linear-gradient(90deg,#00b4d8,#48cae4); }
.kpi-bar.b3 { background:linear-gradient(90deg,#00c897,#2de0b0); }
.kpi-bar.b4 { background:linear-gradient(90deg,#f59e0b,#fbbf24); }
.kpi-bar.b5 { background:linear-gradient(90deg,#7c3aed,#a78bfa); }
.kpi-lbl { font-size:.68rem; font-weight:700; text-transform:uppercase; letter-spacing:.9px; color:#4a6080; margin-bottom:5px; }
.kpi-val { font-family:'Montserrat',sans-serif; font-size:1.6rem; font-weight:800; color:#fff; line-height:1; margin-bottom:3px; }
.kpi-sub { font-size:.72rem; color:#5a7090; font-weight:500; }

/* ── Section title ── */
.sec {
    font-family:'Montserrat',sans-serif; font-size:.82rem; font-weight:800;
    text-transform:uppercase; letter-spacing:1.2px; color:#c0cce0;
    margin-bottom:14px; padding-bottom:10px;
    border-bottom:1px solid rgba(0,87,255,0.12);
    display:flex; align-items:center; gap:8px;
}
.sec-dot { color:#0057FF; font-size:1rem; }

/* ── Insight ── */
.ins {
    background: rgba(0,87,255,0.05);
    border: 1px solid rgba(0,87,255,0.15);
    border-left:3px solid #0057FF;
    border-radius:10px; padding:12px 16px;
    margin-bottom:8px; font-size:.88rem; color:#a0b0cc; line-height:1.6;
}
.ins strong { color:#e2e8f5; }
.ins-green {
    background: rgba(0,200,151,0.05);
    border: 1px solid rgba(0,200,151,0.2);
    border-left:3px solid #00c897;
    border-radius:10px; padding:12px 16px;
    margin-bottom:8px; font-size:.88rem; color:#a0b0cc; line-height:1.6;
}
.ins-green strong { color:#e2e8f5; }
.ins-red {
    background: rgba(239,68,68,0.05);
    border: 1px solid rgba(239,68,68,0.2);
    border-left:3px solid #ef4444;
    border-radius:10px; padding:12px 16px;
    margin-bottom:8px; font-size:.88rem; color:#a0b0cc; line-height:1.6;
}
.ins-red strong { color:#e2e8f5; }
.ins-yellow {
    background: rgba(245,158,11,0.05);
    border: 1px solid rgba(245,158,11,0.2);
    border-left:3px solid #f59e0b;
    border-radius:10px; padding:12px 16px;
    margin-bottom:8px; font-size:.88rem; color:#a0b0cc; line-height:1.6;
}
.ins-yellow strong { color:#e2e8f5; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background:#09101e; border-radius:12px;
    border:1px solid rgba(0,87,255,0.16); padding:5px; gap:4px;
}
.stTabs [data-baseweb="tab"] {
    color:#4a6080; border-radius:8px;
    font-size:.78rem; font-weight:700; text-transform:uppercase; letter-spacing:.5px;
}
.stTabs [aria-selected="true"] {
    background:rgba(0,87,255,0.15) !important; color:#4a8aff !important;
}

/* ── Badge AB ── */
.badge-pos { display:inline-block; background:rgba(0,200,151,0.15); color:#00c897;
    border:1px solid rgba(0,200,151,0.3); border-radius:6px; padding:2px 8px;
    font-size:.7rem; font-weight:700; }
.badge-neg { display:inline-block; background:rgba(239,68,68,0.15); color:#ef4444;
    border:1px solid rgba(239,68,68,0.3); border-radius:6px; padding:2px 8px;
    font-size:.7rem; font-weight:700; }

/* ── Table styling ── */
[data-testid="stDataFrame"] { border-radius:12px; overflow:hidden; }

/* ── Download button ── */
.stDownloadButton > button {
    background:linear-gradient(90deg,#0057FF,#1a6fff) !important;
    color:#fff !important; border:none !important;
    border-radius:8px !important; font-weight:700 !important;
    text-transform:uppercase !important; letter-spacing:.5px !important;
    font-size:.75rem !important; padding:8px 20px !important;
}

/* ── Footer ── */
.footer {
    text-align:center; margin-top:48px; padding:24px 0 12px;
    border-top:1px solid rgba(0,87,255,0.08);
    color:#1a2840; font-size:.72rem; font-weight:700;
    text-transform:uppercase; letter-spacing:1.2px;
}
.footer em { color:#0057FF; font-style:normal; }
</style>
""", unsafe_allow_html=True)


# ─── LEITURA DINÂMICA DA PLANILHA ───────────────────────────────────────────
XLSX_NAME = "Analises_Fopag_-_visao_sem_pecas_chaves.xlsx"
XLSX_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), XLSX_NAME)

import os

# Hierarquia: nome do time → área
AREA_MAP = {
    "Marketing B2C": "Marketing", "Marketing B2B": "Marketing",
    "Vendas B2C": "Vendas", "Vendas B2B": "Vendas",
    "Produtos Corporate": "Produtos", "Tech Academy": "Produtos",
    "Produtos Offline/Eventos": "Produtos", "Produtos Inter": "Produtos",
    "Contabilidade": "Backoffice", "Financeiro": "Backoffice",
    "People": "Backoffice", "Atendimento": "Backoffice",
    "Revops": "Backoffice", "Facilites": "Backoffice",
    "Ops": "Backoffice", "Tech": "Backoffice",
    "Diretoria": "Diretoria",
}

# Times que queremos (linhas reais da planilha, ignorando totalizadores e % rows)
TIMES_VALIDOS = set(AREA_MAP.keys())

MESES_TODOS = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]

@st.cache_data(show_spinner=False)
def get_data(xlsx_path: str):
    raw = pd.read_excel(xlsx_path, sheet_name="Breakdown Alocação de Despesas", header=None)

    # Colunas conforme planilha:
    # Fechamento:  Jan=3, Fev=4, Mar=5, 1T=6
    # Orçamento:   Jan=8, Fev=9, Mar=10, 1T=11, AB=13, Abr-Dez=15-23, Anual=24
    # Forecast:    Jan=26, Fev=27, Mar=28, Abr=29, ... Dez=37, Anual=38
    FECH_COLS  = {m: i for m, i in zip(MESES_TODOS[:3], [3, 4, 5])}
    ORC_1T_COL = 11
    AB_COL     = 13
    ORC_COLS   = {m: i for m, i in zip(MESES_TODOS, [8,9,10,15,16,17,18,19,20,21,22,23])}
    FOR_COLS   = {m: i for m, i in zip(MESES_TODOS, range(26, 38))}

    records = []
    for i in range(8, len(raw)):
        nome = str(raw.iloc[i, 2]).strip()
        if nome not in TIMES_VALIDOS:
            continue
        fj = raw.iloc[i, 3]
        if not isinstance(fj, (int, float)) or pd.isna(fj):
            continue

        rec = {
            "Time": nome,
            "Área": AREA_MAP[nome],
            "Fech_1T2026": raw.iloc[i, 6],
            "Orc_1T2026":  raw.iloc[i, ORC_1T_COL],
            "AB_ratio":    raw.iloc[i, AB_COL],
        }
        # Fechamento mensal (Jan, Fev, Mar)
        for m, col in FECH_COLS.items():
            rec[f"Fech_{m}"] = raw.iloc[i, col]

        # Orçamento mensal (Jan-Dez)
        for m, col in ORC_COLS.items():
            v = raw.iloc[i, col]
            rec[f"Orc_{m}"] = v if isinstance(v, (int, float)) and not pd.isna(v) else 0

        # Forecast mensal (Jan-Dez)
        for m, col in FOR_COLS.items():
            v = raw.iloc[i, col]
            rec[f"For_{m}"] = v if isinstance(v, (int, float)) and not pd.isna(v) else 0

        rec["For_1T2026"] = rec["For_Jan"] + rec["For_Fev"] + rec["For_Mar"]

        records.append(rec)

    df = pd.DataFrame(records)

    # ── Totais da folha completa (linha 9 = "People" total) ──
    totais = {}
    for m, col in FECH_COLS.items():
        totais[f"Fech_{m}"] = raw.iloc[9, col]
    totais["Fech_1T"]  = raw.iloc[9, 6]
    for m, col in ORC_COLS.items():
        v = raw.iloc[9, col]
        totais[f"Orc_{m}"] = v if isinstance(v, (int, float)) and not pd.isna(v) else 0
    totais["Orc_1T"] = raw.iloc[9, ORC_1T_COL]
    for m, col in FOR_COLS.items():
        v = raw.iloc[9, col]
        totais[f"For_{m}"] = v if isinstance(v, (int, float)) and not pd.isna(v) else 0
    totais["For_1T"] = totais["For_Jan"] + totais["For_Fev"] + totais["For_Mar"]

    return df, totais

# ─── HELPERS ────────────────────────────────────────────────────────────────
def brl(v, compact=False):
    if pd.isna(v) or v == 0: return "R$ -"
    if compact:
        if abs(v) >= 1_000_000: return f"R$ {v/1_000_000:.1f}M"
        if abs(v) >= 1_000:     return f"R$ {v/1_000:.0f}K"
    s = f"{v:,.0f}".replace(",","X").replace(".",",").replace("X",".")
    return f"R$ {s}"

def pp(v):
    if pd.isna(v): return "-"
    s = "+" if v >= 0 else ""
    return f"{s}{v:.1f}%"

def ab_badge(v):
    pct_str = f"{v*100:+.1f}%"
    if v >= 0:
        return f'<span class="badge-pos">▲ {pct_str}</span>'
    else:
        return f'<span class="badge-neg">▼ {pct_str}</span>'

COLORS = ["#0057FF","#4a8aff","#00b4d8","#00c897","#7c3aed","#f59e0b","#ef4444","#06b6d4","#10b981","#8b5cf6","#f97316","#ec4899","#a78bfa","#34d399","#60a5fa","#fbbf24"]

LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#4a5e80", size=12),
    margin=dict(l=10, r=10, t=32, b=10),
    legend=dict(bgcolor="rgba(9,16,30,0.95)", bordercolor="rgba(0,87,255,0.18)", borderwidth=1, font=dict(size=11, color="#7a8eaa"))
)


# ─── CHARTS ─────────────────────────────────────────────────────────────────
def chart_hbar(df, xcol, ycol, title=""):
    df_s = df.sort_values(xcol)
    max_v = df_s[xcol].max()
    fig = go.Figure(go.Bar(
        x=df_s[xcol], y=df_s[ycol], orientation="h",
        marker=dict(color=df_s[xcol], colorscale=[[0,"#051540"],[0.45,"#0057FF"],[1,"#4a8aff"]], showscale=False, line=dict(width=0)),
        text=[brl(v, True) for v in df_s[xcol]],
        textposition="outside", textfont=dict(color="#4a5e80", size=11),
        hovertemplate="<b>%{y}</b><br>R$ %{x:,.0f}<extra></extra>"
    ))
    fig.update_layout(**LAYOUT, height=max(340, len(df_s)*44), title=title,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, max_v*1.3]),
        yaxis=dict(showgrid=False, tickfont=dict(size=12, color="#b0bcd4")))
    return fig


def chart_donut(labels, values, title=""):
    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.58,
        marker=dict(colors=COLORS[:len(labels)], line=dict(color="#060d1f", width=3)),
        texttemplate="%{label}<br><b>%{percent:.1%}</b>",
        textfont=dict(size=11, color="#b0bcd4"),
        hovertemplate="<b>%{label}</b><br>R$ %{value:,.0f} · %{percent:.1%}<extra></extra>"
    ))
    fig.update_layout(**LAYOUT, height=360, showlegend=False, title=title)
    return fig


def chart_grouped_bar(df_bu, time_col, cols, labels, title=""):
    fig = go.Figure()
    palette = ["#0057FF","#00c897","#f59e0b"]
    for col, lbl, color in zip(cols, labels, palette):
        fig.add_trace(go.Bar(
            name=lbl, x=df_bu[time_col], y=df_bu[col],
            marker_color=color, opacity=0.9,
            hovertemplate=f"<b>%{{x}}</b><br>{lbl}: R$ %{{y:,.0f}}<extra></extra>"
        ))
    fig.update_layout(**LAYOUT, barmode="group", height=400, title=title,
        xaxis=dict(tickangle=-35, tickfont=dict(color="#b0bcd4"), showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(0,87,255,0.07)", zeroline=False, tickformat=",.0f"))
    return fig


def chart_waterfall(df, xcol, ycol, total_override=None):
    df_s = df.sort_values(ycol, ascending=False)
    total = total_override if total_override is not None else df_s[ycol].sum()
    # Se há override, adiciona uma barra "Outros" para a diferença
    xs = df_s[xcol].tolist()
    ys = df_s[ycol].tolist()
    measures = ["relative"] * len(df_s)
    if total_override is not None:
        diff = total_override - df_s[ycol].sum()
        if abs(diff) > 1:
            xs.append("Outros/Encargos")
            ys.append(diff)
            measures.append("relative")
    xs.append("TOTAL")
    ys.append(total)
    measures.append("total")

    fig = go.Figure(go.Waterfall(
        orientation="v", measure=measures, x=xs, y=ys,
        connector=dict(line=dict(color="rgba(0,87,255,0.15)")),
        increasing=dict(marker=dict(color="#0057FF")),
        totals=dict(marker=dict(color="#00c897")),
        texttemplate="%{y:,.0f}", textfont=dict(size=10, color="#5a6e90"),
        hovertemplate="<b>%{x}</b><br>R$ %{y:,.0f}<extra></extra>"
    ))
    fig.update_layout(**LAYOUT, height=380,
        xaxis=dict(tickangle=-35, tickfont=dict(size=11, color="#b0bcd4"), showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(0,87,255,0.07)", zeroline=False))
    return fig


def chart_ab(df, time_col, ab_col):
    df_s = df.sort_values(ab_col)
    # Negativo = gastou MENOS que o orçado = EFICIÊNCIA = verde
    # Positivo = gastou MAIS que o orçado  = ATENÇÃO    = vermelho
    fig = go.Figure(go.Bar(
        x=df_s[ab_col]*100, y=df_s[time_col], orientation="h",
        marker_color=["#00c897" if v < 0 else "#ef4444" for v in df_s[ab_col]],
        text=[f"{v*100:+.1f}%" for v in df_s[ab_col]],
        textposition="outside", textfont=dict(size=11, color="#a0b0cc"),
        hovertemplate="<b>%{y}</b><br>A/B: %{x:.1f}%<extra></extra>"
    ))
    fig.update_layout(**LAYOUT, height=max(340, len(df_s)*44),
        xaxis=dict(showgrid=True, gridcolor="rgba(0,87,255,0.07)", zeroline=True, zerolinecolor="rgba(0,87,255,0.3)", title="%"),
        yaxis=dict(showgrid=False, tickfont=dict(size=12, color="#b0bcd4")))
    return fig


def chart_area_meses(totais, df_filtered, todos):
    meses_fech = ["Jan","Fev","Mar"]

    if todos:
        vals_fech = [totais[f"Fech_{m}"] for m in meses_fech]
        vals_orc  = [totais[f"Orc_{m}"]  for m in MESES_TODOS]
        vals_for  = [totais[f"For_{m}"]  for m in MESES_TODOS]
    else:
        vals_fech = [df_filtered[f"Fech_{m}"].sum() for m in meses_fech]
        vals_orc  = [df_filtered[f"Orc_{m}"].sum()  for m in MESES_TODOS]
        vals_for  = [df_filtered[f"For_{m}"].sum()  for m in MESES_TODOS]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=meses_fech, y=vals_fech, name="Fechamento Real",
        mode="lines+markers",
        line=dict(color="#0057FF", width=3),
        marker=dict(size=9, color="#4a8aff", line=dict(color="#060d1f", width=2)),
        fill="tozeroy", fillcolor="rgba(0,87,255,0.06)",
        hovertemplate="<b>%{x}</b><br>Real: R$ %{y:,.0f}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=MESES_TODOS, y=vals_orc, name="Orçamento",
        mode="lines+markers",
        line=dict(color="#00c897", width=2, dash="dot"),
        marker=dict(size=7, color="#00c897"),
        hovertemplate="<b>%{x}</b><br>Orç: R$ %{y:,.0f}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=MESES_TODOS, y=vals_for, name="Forecast",
        mode="lines+markers",
        line=dict(color="#f59e0b", width=2, dash="dashdot"),
        marker=dict(size=7, color="#f59e0b"),
        hovertemplate="<b>%{x}</b><br>Forecast: R$ %{y:,.0f}<extra></extra>"
    ))
    fig.update_layout(**LAYOUT, height=360,
        xaxis=dict(showgrid=False, tickfont=dict(color="#b0bcd4")),
        yaxis=dict(showgrid=True, gridcolor="rgba(0,87,255,0.07)", tickformat=",.0f"))
    return fig


def chart_treemap(df, time_col, grupo_col, val_col):
    fig = px.treemap(df, path=[grupo_col, time_col], values=val_col,
        color=val_col, color_continuous_scale=["#051540","#0057FF","#4a8aff"])
    fig.update_traces(
        texttemplate="<b>%{label}</b><br>%{value:,.0f}",
        textfont_size=12,
        hovertemplate="<b>%{label}</b><br>R$ %{value:,.0f}<extra></extra>"
    )
    fig.update_layout(**LAYOUT, coloraxis_showscale=False, height=420)
    return fig


# ─── MAIN ────────────────────────────────────────────────────────────────────
def main():
    # Verifica planilha
    if not os.path.exists(XLSX_PATH):
        st.error(f"⚠️ Planilha não encontrada: **{XLSX_NAME}**\n\nColoque o arquivo na mesma pasta que este script.")
        uploaded = st.file_uploader("Ou faça upload aqui:", type=["xlsx","xls"])
        if uploaded:
            with open(XLSX_PATH, "wb") as f: f.write(uploaded.read())
            st.rerun()
        return

    df, totais = get_data(XLSX_PATH)

    # ── Sidebar ──────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("""
        <div style="padding:22px 0 18px; border-bottom:1px solid rgba(0,87,255,0.2); margin-bottom:22px;">
            <div style="font-family:'Montserrat',sans-serif; font-size:1.5rem; font-weight:900; color:#fff; letter-spacing:-0.5px;">
                <span style="color:#0057FF;">.</span>StartSe
            </div>
            <div style="font-size:0.65rem; color:#1e3560; text-transform:uppercase; letter-spacing:1.5px; margin-top:4px; font-weight:700;">
                People Analytics · FOPAG
            </div>
        </div>
        """, unsafe_allow_html=True)

        grupos = sorted(df["Área"].unique().tolist())
        grupo_filter = st.multiselect("Área", grupos, default=grupos)
        all_bus = sorted(df[df["Área"].isin(grupo_filter)]["Time"].unique().tolist())
        bu_filter = st.multiselect("Times", all_bus, default=all_bus)

        st.markdown("---")
        visao = st.radio("Visão de Valor", ["Fechamento Real (1T2026)", "Orçamento (1T2026)", "Forecast (1T2026)", "Ambos"])

        st.markdown("---")
        st.caption("📅 Realizado: Jan–Mar 2026\n📊 Orçamento: Jan–Dez 2026\n🔮 Forecast: Jan–Dez 2026")

    # ── Filtrar dados ────────────────────────────────────────────────────────
    df_f = df[df["Time"].isin(bu_filter)].copy()
    todos = len(df_f) == len(df)

    val_col = "Fech_1T2026"
    if "Orçamento" in visao:  val_col = "Orc_1T2026"
    if "Forecast"  in visao:  val_col = "For_1T2026"

    total_real = totais["Fech_1T"] if todos else df_f["Fech_1T2026"].sum()
    total_orc  = totais["Orc_1T"]  if todos else df_f["Orc_1T2026"].sum()
    total_for  = totais["For_1T"]  if todos else df_f["For_1T2026"].sum()
    total_ab   = (total_real - total_orc) / total_orc if total_orc else 0
    total_af   = (total_for  - total_orc) / total_orc if total_orc else 0  # forecast vs orc
    maior_bu   = df_f.loc[df_f["Fech_1T2026"].idxmax(), "Time"]
    maior_val  = df_f["Fech_1T2026"].max()
    n_bu       = len(df_f)

    # ── Hero ────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero">
        <div class="hero-badge">⚡ RH · People Analytics · 1T2026</div>
        <h1>FOPAG <em>Breakdown</em><br>de Despesas</h1>
        <p>Alocação da folha por Time · Fechamento Jan–Mar 2026 · Orçamento e Forecast 2026 · StartSe</p>
    </div>
    """, unsafe_allow_html=True)

    # ── KPIs ─────────────────────────────────────────────────────────────────
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    kpis = [
        (c1, "b1", "💰 Realizado 1T",   brl(total_real),              "Fechamento Jan–Mar"),
        (c2, "b2", "📋 Orçado 1T",      brl(total_orc),               "Orçamento Jan–Mar"),
        (c3, "b5", "🔮 Forecast 1T",    brl(total_for),               "Forecast Jan–Mar"),
        (c4, "b3", "📊 A/B Real",       f"{total_ab*100:+.1f}%",      "Real vs Orçamento"),
        (c5, "b4", "📈 A/F Forecast",   f"{total_af*100:+.1f}%",      "Forecast vs Orçamento"),
        (c6, "b4", "🏢 Times Ativos",   str(n_bu),                    "Com despesas alocadas"),
    ]
    for col, bar, lbl, val, sub in kpis:
        col.markdown(f"""
        <div class="kpi">
            <div class="kpi-bar {bar}"></div>
            <div class="kpi-lbl">{lbl}</div>
            <div class="kpi-val">{val}</div>
            <div class="kpi-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tabs ────────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs([
        "🗺️  Visão por Time",
        "📊  Real vs Orçamento",
        "📈  Evolução Mensal",
        "🔎  Tabela Detalhada",
    ])

    # ══════════════════════════════════════════
    # TAB 1 — VISÃO POR TIME
    # ══════════════════════════════════════════
    with tab1:
        visao_label = "Fechamento 1T2026" if "Fechamento" in visao else ("Forecast 1T2026" if "Forecast" in visao else "Orçamento 1T2026")
        col_a, col_b = st.columns([3,2], gap="large")
        with col_a:
            st.markdown(f'<div class="sec"><span class="sec-dot">▌</span> Despesas por Time — {visao_label}</div>', unsafe_allow_html=True)
            st.plotly_chart(chart_hbar(df_f, val_col, "Time"), use_container_width=True)
        with col_b:
            st.markdown(f'<div class="sec"><span class="sec-dot">▌</span> Distribuição % · {visao_label}</div>', unsafe_allow_html=True)
            top9 = df_f.nlargest(9, val_col)
            outros = df_f[val_col].sum() - top9[val_col].sum()
            lbls = top9["Time"].tolist()
            vals = top9[val_col].tolist()
            if outros > 0: lbls.append("Outros"); vals.append(outros)
            st.plotly_chart(chart_donut(lbls, vals), use_container_width=True)

        st.markdown(f'<div class="sec"><span class="sec-dot">▌</span> Treemap Hierárquico · Área › Time · {visao_label}</div>', unsafe_allow_html=True)
        st.plotly_chart(chart_treemap(df_f, "Time", "Área", val_col), use_container_width=True)

        st.markdown('<div class="sec"><span class="sec-dot">▌</span> Composição por Área</div>', unsafe_allow_html=True)
        df_grp = df_f.groupby("Área")[val_col].sum().reset_index().sort_values(val_col, ascending=False)
        st.plotly_chart(chart_donut(df_grp["Área"].tolist(), df_grp[val_col].tolist()), use_container_width=True)

        st.markdown('<div class="sec"><span class="sec-dot">▌</span> Insights Automáticos · 1T2026</div>', unsafe_allow_html=True)

        # Calcula eficiência A/B por time
        df_ab_insight = df_f[["Time","Área","Fech_1T2026","Orc_1T2026","AB_ratio"]].copy()
        df_ab_insight["Diferença"] = df_ab_insight["Fech_1T2026"] - df_ab_insight["Orc_1T2026"]

        # Times com maior eficiência (mais negativos = gastou menos que orçado)
        eficientes = df_ab_insight[df_ab_insight["AB_ratio"] < 0].sort_values("AB_ratio").head(3)
        # Times com maior desvio positivo (gastou mais que orçado)
        atencao = df_ab_insight[df_ab_insight["AB_ratio"] > 0].sort_values("AB_ratio", ascending=False)
        atencao_sem_dir = atencao[atencao["Time"] != "Diretoria"].head(2)
        diretoria_row = df_ab_insight[df_ab_insight["Time"] == "Diretoria"]

        # Insight consolidado
        total_economia = df_ab_insight[df_ab_insight["AB_ratio"] < 0]["Diferença"].sum()
        total_excesso  = df_ab_insight[df_ab_insight["AB_ratio"] > 0]["Diferença"].sum()

        st.markdown(f"""
        <div class="ins">
            <strong>📊 Visão Geral do Trimestre:</strong> O total realizado foi <strong>{brl(total_real)}</strong>
            vs orçado de <strong>{brl(total_orc)}</strong> — variação de <strong>{total_ab*100:+.1f}%</strong>.
            Economias geradas: <strong>{brl(abs(total_economia))}</strong> |
            Extrapolações: <strong>{brl(total_excesso)}</strong>.
        </div>
        """, unsafe_allow_html=True)

        # Eficiências
        if not eficientes.empty:
            linhas_ef = " · ".join([
                f"<strong>{r['Time']}</strong> ({r['AB_ratio']*100:+.1f}%, {brl(abs(r['Diferença']))} abaixo)"
                for _, r in eficientes.iterrows()
            ])
            st.markdown(f"""
            <div class="ins-green">
                <strong>✅ Maiores Eficiências de Folha:</strong> Os times com melhor desempenho
                em relação ao orçamento foram {linhas_ef}.
                Esses times demonstraram otimização de headcount ou remuneração abaixo do planejado no trimestre.
            </div>
            """, unsafe_allow_html=True)

        # Pontos de atenção (exceto Diretoria, que tem contexto específico)
        if not atencao_sem_dir.empty:
            linhas_at = " · ".join([
                f"<strong>{r['Time']}</strong> ({r['AB_ratio']*100:+.1f}%, {brl(r['Diferença'])} acima)"
                for _, r in atencao_sem_dir.iterrows()
            ])
            st.markdown(f"""
            <div class="ins-red">
                <strong>⚠️ Pontos de Atenção:</strong> Os times que mais extrapolaram o orçamento foram
                {linhas_at}. Recomenda-se revisão das causas — admissões não planejadas,
                reajustes ou horas extras podem ser os principais drivers.
            </div>
            """, unsafe_allow_html=True)

        # Diretoria com contexto ICP
        if not diretoria_row.empty:
            dr = diretoria_row.iloc[0]
            st.markdown(f"""
            <div class="ins-yellow">
                <strong>💡 Diretoria — Contexto ICP Trimestral:</strong> O desvio positivo de
                <strong>{dr['AB_ratio']*100:+.1f}%</strong> ({brl(dr['Diferença'])} acima do orçado)
                está diretamente relacionado ao <strong>pagamento do ICP (Incentivo de Curto Prazo)
                trimestral</strong> da Diretoria, evento previsto no calendário de remuneração variável.
                Este valor não representa extrapolação operacional e deve ser desconsiderado
                nas análises de eficiência de folha recorrente.
            </div>
            """, unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # TAB 2 — REAL vs ORÇAMENTO vs FORECAST
    # ══════════════════════════════════════════
    with tab2:
        st.markdown('<div class="sec"><span class="sec-dot">▌</span> Real vs Orçamento vs Forecast — 1T2026 por Time</div>', unsafe_allow_html=True)
        st.plotly_chart(chart_grouped_bar(df_f, "Time",
            ["Fech_1T2026","Orc_1T2026","For_1T2026"],
            ["Fechamento Real","Orçamento","Forecast"]), use_container_width=True)

        col_c, col_d = st.columns([2,3], gap="large")
        with col_c:
            st.markdown('<div class="sec"><span class="sec-dot">▌</span> Distribuição A/B (Real vs Orc)</div>', unsafe_allow_html=True)
            pos = df_f[df_f["AB_ratio"] >= 0]
            neg = df_f[df_f["AB_ratio"] < 0]
            st.metric("⚠️ Acima do orçado", f"{len(pos)} times", "Gastaram mais que o planejado")
            st.metric("✅ Abaixo do orçado", f"{len(neg)} times", "Abaixo do orçamento")

            st.markdown("<br>", unsafe_allow_html=True)
            # Forecast vs Orçamento por área
            df_grp_for = df_f.groupby("Área")[["For_1T2026","Orc_1T2026"]].sum().reset_index()
            df_grp_for["AF%"] = ((df_grp_for["For_1T2026"] - df_grp_for["Orc_1T2026"]) / df_grp_for["Orc_1T2026"] * 100).round(1)
            df_grp_for_show = df_grp_for.copy()
            df_grp_for_show["Forecast 1T"] = df_grp_for["For_1T2026"].apply(brl)
            df_grp_for_show["Orçado 1T"]   = df_grp_for["Orc_1T2026"].apply(brl)
            df_grp_for_show["A/F %"]       = df_grp_for["AF%"].apply(lambda v: f"{v:+.1f}%")
            st.markdown('<div class="sec" style="margin-top:12px"><span class="sec-dot">▌</span> Forecast vs Orc por Área</div>', unsafe_allow_html=True)
            st.dataframe(df_grp_for_show[["Área","Forecast 1T","Orçado 1T","A/F %"]], use_container_width=True, hide_index=True)

        with col_d:
            st.markdown('<div class="sec"><span class="sec-dot">▌</span> Variação A/B por Time (%)</div>', unsafe_allow_html=True)
            st.plotly_chart(chart_ab(df_f, "Time", "AB_ratio"), use_container_width=True)

        st.markdown('<div class="sec"><span class="sec-dot">▌</span> Ranking Detalhado: Real · Orçamento · Forecast</div>', unsafe_allow_html=True)
        df_ab = df_f[["Time","Área","Fech_1T2026","Orc_1T2026","For_1T2026","AB_ratio"]].copy()
        df_ab["Dif. Real-Orc"] = df_ab["Fech_1T2026"] - df_ab["Orc_1T2026"]
        df_ab["Dif. For-Orc"]  = df_ab["For_1T2026"]  - df_ab["Orc_1T2026"]
        df_ab["AF%"] = (df_ab["Dif. For-Orc"] / df_ab["Orc_1T2026"] * 100).round(1)
        df_ab = df_ab.sort_values("AB_ratio", ascending=False)
        df_ab_show = df_ab.copy()
        df_ab_show["Realizado"] = df_ab["Fech_1T2026"].apply(brl)
        df_ab_show["Orçado"]    = df_ab["Orc_1T2026"].apply(brl)
        df_ab_show["Forecast"]  = df_ab["For_1T2026"].apply(brl)
        df_ab_show["A/B %"]     = (df_ab["AB_ratio"]*100).apply(lambda v: f"{v:+.1f}%")
        df_ab_show["A/F %"]     = df_ab["AF%"].apply(lambda v: f"{v:+.1f}%")
        st.dataframe(df_ab_show[["Time","Área","Realizado","Orçado","A/B %","Forecast","A/F %"]],
                     use_container_width=True, hide_index=True)

    # ══════════════════════════════════════════
    # TAB 3 — EVOLUÇÃO MENSAL
    # ══════════════════════════════════════════
    with tab3:
        st.markdown('<div class="sec"><span class="sec-dot">▌</span> Evolução Mensal: Realizado · Orçamento · Forecast — Jan a Dez 2026</div>', unsafe_allow_html=True)
        st.plotly_chart(chart_area_meses(totais, df_f, todos), use_container_width=True)

        col_e, col_f = st.columns(2, gap="large")
        with col_e:
            st.markdown('<div class="sec"><span class="sec-dot">▌</span> Fechamento Real por Time — Jan, Fev, Mar</div>', unsafe_allow_html=True)
            fig_m = go.Figure()
            for i, time_name in enumerate(df_f["Time"].tolist()):
                row = df_f[df_f["Time"]==time_name].iloc[0]
                vals_f = [row[f"Fech_{m}"] for m in ["Jan","Fev","Mar"]]
                fig_m.add_trace(go.Scatter(
                    x=["Jan","Fev","Mar"], y=vals_f, name=time_name,
                    mode="lines+markers",
                    line=dict(color=COLORS[i % len(COLORS)], width=2),
                    marker=dict(size=7),
                    hovertemplate=f"<b>{time_name}</b><br>%{{x}}: R$ %{{y:,.0f}}<extra></extra>"
                ))
            fig_m.update_layout(**LAYOUT, height=400,
                xaxis=dict(showgrid=False, tickfont=dict(color="#b0bcd4")),
                yaxis=dict(showgrid=True, gridcolor="rgba(0,87,255,0.07)", tickformat=",.0f"))
            fig_m.update_layout(legend=dict(font=dict(size=9)))
            st.plotly_chart(fig_m, use_container_width=True)

        with col_f:
            st.markdown('<div class="sec"><span class="sec-dot">▌</span> Forecast Anual por Time — Jan a Dez 2026</div>', unsafe_allow_html=True)
            fig_for = go.Figure()
            for i, time_name in enumerate(df_f["Time"].tolist()):
                row = df_f[df_f["Time"]==time_name].iloc[0]
                vals_for = [row[f"For_{m}"] for m in MESES_TODOS]
                fig_for.add_trace(go.Scatter(
                    x=MESES_TODOS, y=vals_for, name=time_name,
                    mode="lines+markers",
                    line=dict(color=COLORS[i % len(COLORS)], width=2, dash="dot"),
                    marker=dict(size=6),
                    hovertemplate=f"<b>{time_name}</b><br>%{{x}}: R$ %{{y:,.0f}}<extra></extra>"
                ))
            fig_for.update_layout(**LAYOUT, height=400,
                xaxis=dict(showgrid=False, tickfont=dict(color="#b0bcd4")),
                yaxis=dict(showgrid=True, gridcolor="rgba(0,87,255,0.07)", tickformat=",.0f"))
            fig_for.update_layout(legend=dict(font=dict(size=9)))
            st.plotly_chart(fig_for, use_container_width=True)

        # Forecast anual total por área
        st.markdown('<div class="sec"><span class="sec-dot">▌</span> Forecast Anual Total por Área — Jan a Dez 2026</div>', unsafe_allow_html=True)
        for_anual_cols = [f"For_{m}" for m in MESES_TODOS]
        df_for_area = df_f.copy()
        df_for_area["For_Anual"] = df_for_area[for_anual_cols].sum(axis=1)
        df_for_grp = df_for_area.groupby("Área")["For_Anual"].sum().reset_index().sort_values("For_Anual", ascending=False)
        fig_for_area = go.Figure(go.Bar(
            x=df_for_grp["Área"], y=df_for_grp["For_Anual"],
            marker_color=COLORS[:len(df_for_grp)],
            text=[brl(v, True) for v in df_for_grp["For_Anual"]],
            textposition="outside", textfont=dict(color="#a0b0cc", size=11),
            hovertemplate="<b>%{x}</b><br>Forecast Anual: R$ %{y:,.0f}<extra></extra>"
        ))
        fig_for_area.update_layout(**LAYOUT, height=320,
            xaxis=dict(tickfont=dict(color="#b0bcd4"), showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(0,87,255,0.07)", tickformat=",.0f"))
        st.plotly_chart(fig_for_area, use_container_width=True)

        # Variação mês a mês (Real)
        st.markdown('<div class="sec"><span class="sec-dot">▌</span> Variação Real: Jan→Fev e Fev→Mar por Time</div>', unsafe_allow_html=True)
        df_var = df_f[["Time","Fech_Jan","Fech_Fev","Fech_Mar"]].copy()
        df_var["Δ Jan→Fev"] = df_var["Fech_Fev"] - df_var["Fech_Jan"]
        df_var["Δ Fev→Mar"] = df_var["Fech_Mar"] - df_var["Fech_Fev"]
        fig_var = go.Figure()
        fig_var.add_trace(go.Bar(name="Δ Jan→Fev", x=df_var["Time"], y=df_var["Δ Jan→Fev"],
            marker_color=["#00c897" if v>=0 else "#ef4444" for v in df_var["Δ Jan→Fev"]],
            hovertemplate="<b>%{x}</b><br>Δ Jan→Fev: R$ %{y:,.0f}<extra></extra>"))
        fig_var.add_trace(go.Bar(name="Δ Fev→Mar", x=df_var["Time"], y=df_var["Δ Fev→Mar"],
            marker_color=["#4a8aff" if v>=0 else "#f59e0b" for v in df_var["Δ Fev→Mar"]],
            hovertemplate="<b>%{x}</b><br>Δ Fev→Mar: R$ %{y:,.0f}<extra></extra>"))
        fig_var.update_layout(**LAYOUT, barmode="group", height=340,
            xaxis=dict(tickangle=-35, tickfont=dict(color="#b0bcd4"), showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(0,87,255,0.07)", zeroline=True, zerolinecolor="rgba(0,87,255,0.3)"))
        st.plotly_chart(fig_var, use_container_width=True)

    # ══════════════════════════════════════════
    # TAB 4 — TABELA DETALHADA
    # ══════════════════════════════════════════
    with tab4:
        st.markdown('<div class="sec"><span class="sec-dot">▌</span> Tabela Completa — Real · Orçamento · Forecast</div>', unsafe_allow_html=True)
        df_show = df_f[["Time","Área","Fech_Jan","Fech_Fev","Fech_Mar","Fech_1T2026","Orc_1T2026","For_1T2026","AB_ratio"]].copy()
        df_show["% do Total"] = (df_show["Fech_1T2026"] / total_real * 100).round(1).astype(str) + "%"
        df_show["A/B %"] = (df_show["AB_ratio"]*100).apply(lambda v: f"{v:+.1f}%")
        df_show["A/F %"] = ((df_show["For_1T2026"] - df_show["Orc_1T2026"]) / df_show["Orc_1T2026"] * 100).apply(lambda v: f"{v:+.1f}%")
        for c in ["Fech_Jan","Fech_Fev","Fech_Mar","Fech_1T2026","Orc_1T2026","For_1T2026"]:
            df_show[c] = df_show[c].apply(brl)
        df_show = df_show.drop(columns=["AB_ratio"]).rename(columns={
            "Fech_Jan":"Jan","Fech_Fev":"Fev","Fech_Mar":"Mar",
            "Fech_1T2026":"Realizado 1T","Orc_1T2026":"Orçado 1T","For_1T2026":"Forecast 1T"
        })
        st.dataframe(df_show, use_container_width=True, hide_index=True, height=480)

        df_exp = df_f[["Time","Área","Fech_Jan","Fech_Fev","Fech_Mar","Fech_1T2026","Orc_1T2026","For_1T2026","AB_ratio"]].copy()
        df_exp["AB_ratio"] = (df_exp["AB_ratio"]*100).round(2)
        csv = df_exp.to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig")
        st.download_button("⬇️ Exportar CSV", data=csv, file_name="fopag_breakdown_1T2026.csv", mime="text/csv")

    st.markdown('<div class="footer"><em>.StartSe</em> · People Analytics · FOPAG Dashboard · 1T2026 · Dados confidenciais — uso interno RH</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()