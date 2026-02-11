import random

import networkx as nx
import pandas as pd
import plotly.express as px
import streamlit as st

# --- Page Configuration ---
st.set_page_config(page_title="Pulse: Volume vs Influence", layout="wide")

st.title("Pulse: Volume vs. Influence Analysis")
st.markdown("""
This dashboard demonstrates the difference between **Activity Volume** (tracked via Count-Min Sketch) 
and **Structural Authority** (tracked via PageRank).
""")

# --- Sidebar Controls ---
st.sidebar.header("Simulation Parameters")
total_events = st.sidebar.slider("Total Stream Events", 1000, 10000, 5000, 1000)

# --- Simulation Logic ---


@st.cache_data  # Cache the simulation result to prevent re-running on every interaction
def run_simulation(n_events):
    # Import the algorithm class from your local file
    from Count_Min_Sketch import CountMinSketch

    # Initialize Data Structures
    sketch = CountMinSketch(width=1000, depth=5)
    G = nx.DiGraph()

    # Define Entities
    SPAMMER = "chatter_box_99"
    CELEBRITY = "the_celebrity"
    NORMAL_USERS = [f"user_{i}" for i in range(50)]

    # Run Stream
    for _ in range(n_events):
        if random.random() < 0.1:
            actor, target = SPAMMER, random.choice(NORMAL_USERS)
        elif random.random() < 0.1:
            actor, target = random.choice(NORMAL_USERS), CELEBRITY
        else:
            actor, target = random.choice(NORMAL_USERS), random.choice(NORMAL_USERS)

        sketch.add(actor)

        if G.has_edge(actor, target):
            G[actor][target]["weight"] += 1
        else:
            G.add_edge(actor, target, weight=1)

    return sketch, G, SPAMMER, CELEBRITY, NORMAL_USERS


# Execute Simulation
sketch, G, spammer, celebrity, users = run_simulation(total_events)

# --- Analysis Processing ---

# 1. Volume Analysis (CMS)
volume_scores = {u: sketch.estimate(u) for u in [spammer, celebrity] + users}
top_volume = sorted(volume_scores.items(), key=lambda x: x[1], reverse=True)[:5]

# 2. Influence Analysis (PageRank)
pr = nx.pagerank(G, weight="weight")
top_influence = sorted(pr.items(), key=lambda x: x[1], reverse=True)[:5]

# --- Visualization Layout ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Volume Leader (CMS)")
    st.caption("Identifies entities with the highest activity (mentions/actions).")
    df_vol = pd.DataFrame(top_volume, columns=["User", "Mentions"])
    fig_vol = px.bar(
        df_vol,
        x="Mentions",
        y="User",
        orientation="h",
        color="Mentions",
        color_continuous_scale="Reds",
        text="Mentions",
    )
    fig_vol.update_layout(height=400, yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_vol, use_container_width=True)

with col2:
    st.subheader("Influence Leader (PageRank)")
    st.caption(
        "Identifies entities with the highest authority based on network structure."
    )
    df_inf = pd.DataFrame(top_influence, columns=["User", "PageRank Score"])
    fig_inf = px.bar(
        df_inf,
        x="PageRank Score",
        y="User",
        orientation="h",
        color="PageRank Score",
        color_continuous_scale="Blues",
        text_auto=True,
    )
    fig_inf.update_layout(height=400, yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_inf, use_container_width=True)

# --- Key Insight ---
st.info(
    f"System Insight: '{spammer}' dominates Volume (Noise), while '{
        celebrity
    }' dominates Influence (Authority)."
)
