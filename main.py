import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(
    page_title="Futuristic Stock Dashboard",
    page_icon="🚀",
    layout="wide"
)

# ------------------------------------------------
# FUTURISTIC UI (Animated Gradient + Particles + Neon)
# ------------------------------------------------
st.markdown("""
<style>

/* Animated Gradient Background */
.stApp {
    background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #000000);
    background-size: 400% 400%;
    animation: gradientMove 15s ease infinite;
    overflow: hidden;
}

@keyframes gradientMove {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Floating Particles */
body::before {
    content: "";
    position: fixed;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(0,255,255,0.15) 1px, transparent 1px);
    background-size: 50px 50px;
    animation: moveParticles 60s linear infinite;
    z-index: 0;
}

@keyframes moveParticles {
    from { transform: translate(0, 0); }
    to { transform: translate(-500px, -500px); }
}

/* Glass container */
.block-container {
    background: rgba(0, 0, 0, 0.6);
    padding: 2rem;
    border-radius: 20px;
    backdrop-filter: blur(15px);
    z-index: 1;
}

/* Neon Glow Buttons */
.stButton>button {
    color: #00ffff;
    border: 2px solid #00ffff;
    background-color: transparent;
    border-radius: 12px;
    transition: 0.3s;
}

.stButton>button:hover {
    box-shadow: 0 0 20px #00ffff, 0 0 40px #00ffff;
    transform: scale(1.05);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(0, 0, 0, 0.85) !important;
}

/* Headings Neon */
h1, h2, h3 {
    color: #00ffff;
    text-shadow: 0 0 10px #00ffff;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# TITLE
# ------------------------------------------------
st.title("🚀 Futuristic Multi-Stock Intelligence Dashboard")
st.markdown("AI-powered visual stock analytics with cyberpunk UI")

# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------
@st.cache_data
def load_data():
    data_frames = []
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(BASE_DIR, "data")

    for file in os.listdir(data_path):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(data_path, file))
            df["Source"] = file.replace(".csv", "")
            df["Date"] = pd.to_datetime(df["Date"])
            df = df.sort_values("Date")
            data_frames.append(df)

    combined = pd.concat(data_frames)
    return combined

data = load_data()

# ------------------------------------------------
# SIDEBAR FILTER
# ------------------------------------------------
st.sidebar.header("⚙ Filter Stocks")

stocks = st.sidebar.multiselect(
    "Select Stocks",
    data["Source"].unique(),
    default=data["Source"].unique()
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    [data["Date"].min(), data["Date"].max()]
)

filtered = data[
    (data["Source"].isin(stocks)) &
    (data["Date"] >= pd.to_datetime(date_range[0])) &
    (data["Date"] <= pd.to_datetime(date_range[1]))
]

# ------------------------------------------------
# TECHNICAL INDICATORS
# ------------------------------------------------
filtered["MA20"] = filtered.groupby("Source")["Close"].transform(lambda x: x.rolling(20).mean())
filtered["MA50"] = filtered.groupby("Source")["Close"].transform(lambda x: x.rolling(50).mean())
filtered["Daily Return %"] = filtered.groupby("Source")["Close"].pct_change() * 100
filtered["Cumulative Return"] = (
    filtered.groupby("Source")["Close"]
    .apply(lambda x: (x / x.iloc[0]) - 1)
    .reset_index(level=0, drop=True)
)

# ------------------------------------------------
# CLOSING PRICE
# ------------------------------------------------
st.subheader("📈 Closing Price Comparison")

fig1 = px.line(
    filtered,
    x="Date",
    y="Close",
    color="Source",
    template="plotly_dark"
)

st.plotly_chart(fig1, use_container_width=True)

# ------------------------------------------------
# CANDLESTICK
# ------------------------------------------------
st.subheader("🕯 Candlestick Chart")

selected_stock = st.selectbox("Select Stock", stocks)
stock_df = filtered[filtered["Source"] == selected_stock]

fig2 = go.Figure(data=[go.Candlestick(
    x=stock_df["Date"],
    open=stock_df["Open"],
    high=stock_df["High"],
    low=stock_df["Low"],
    close=stock_df["Close"]
)])

fig2.update_layout(template="plotly_dark")
st.plotly_chart(fig2, use_container_width=True)

# ------------------------------------------------
# MOVING AVERAGE
# ------------------------------------------------
st.subheader("📊 Moving Averages")

fig3 = px.line(
    stock_df,
    x="Date",
    y=["Close", "MA20", "MA50"],
    template="plotly_dark"
)

st.plotly_chart(fig3, use_container_width=True)

# ------------------------------------------------
# DAILY RETURNS
# ------------------------------------------------
st.subheader("📉 Daily Return %")

fig4 = px.line(
    filtered,
    x="Date",
    y="Daily Return %",
    color="Source",
    template="plotly_dark"
)

st.plotly_chart(fig4, use_container_width=True)

# ------------------------------------------------
# CUMULATIVE RETURN
# ------------------------------------------------
st.subheader("🚀 Cumulative Performance")

fig5 = px.line(
    filtered,
    x="Date",
    y="Cumulative Return",
    color="Source",
    template="plotly_dark"
)

st.plotly_chart(fig5, use_container_width=True)

# ------------------------------------------------
# ANIMATED RACE
# ------------------------------------------------
st.subheader("🎬 Animated Growth Race")

race_df = filtered.copy()
race_df["Date_str"] = race_df["Date"].dt.strftime("%Y-%m-%d")

fig6 = px.bar(
    race_df,
    x="Source",
    y="Cumulative Return",
    color="Source",
    animation_frame="Date_str",
    template="plotly_dark"
)

st.plotly_chart(fig6, use_container_width=True)

# ------------------------------------------------
# DATA TABLE
# ------------------------------------------------
st.subheader("📄 Combined Dataset")
st.dataframe(filtered.sort_values("Date", ascending=False))
