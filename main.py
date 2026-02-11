import random

import networkx as nx
import psutil

from Count_Min_Sketch import CountMinSketch

# --- Initialization ---
sketch = CountMinSketch(width=1000, depth=5)
G = nx.DiGraph()  # Directed Graph to distinguish 'talking AT' vs 'being talked ABOUT'

# --- Config ---
TOTAL_EVENTS = 5000
SPAMMER = "chatter_box_99"
CELEBRITY = "the_celebrity"
NORMAL_USERS = [f"user_{i}" for i in range(50)]

print("--- Starting Pulse: Spammer vs Celebrity ---")

for i in range(TOTAL_EVENTS):
    # --- Simulation Logic ---

    # 10% chance: Spammer acts (High Volume, Low Influence)
    if random.random() < 0.1:
        actor, target = SPAMMER, random.choice(NORMAL_USERS)

    # 10% chance: Celebrity is targeted (Low Volume, High Influence)
    elif random.random() < 0.1:
        actor, target = random.choice(NORMAL_USERS), CELEBRITY

    # 80% chance: Normal noise
    else:
        actor, target = random.choice(NORMAL_USERS), random.choice(NORMAL_USERS)

    # --- Update CMS (Track Volume) ---
    sketch.add(actor)

    # --- Update Graph (Track Structure) ---
    if G.has_edge(actor, target):
        G[actor][target]["weight"] += 1
    else:
        G.add_edge(actor, target, weight=1)

    # --- Checkpoint ---
    if i % 1000 == 0 and i > 0:
        # Track Spammer's volume in the Sketch
        spammer_vol = sketch.estimate(SPAMMER)

        # Calculate Influence (PageRank) on the Graph
        pr = nx.pagerank(G, weight="weight")
        top_influencer = max(pr, key=pr.get)
        top_score = pr[top_influencer]

        print(f"Event {i}:")
        print(f"  [Volume] Spammer: {spammer_vol}")
        print(f"  [Influence] Top Node: {top_influencer} (Score: {top_score:.4f})")
        print(f"  [Memory] {psutil.Process().memory_info().rss / (1024 * 1024):.2f} MB")
        print("-" * 20)

# --- Final Analysis ---
print("\n--- Final Pulse Analysis ---")

# 1. Find Volume Leader (CMS)
all_users = [SPAMMER, CELEBRITY] + NORMAL_USERS
volume_leader = max(all_users, key=lambda u: sketch.estimate(u))
volume_count = sketch.estimate(volume_leader)

# 2. Find Influence Leader (PageRank)
pr = nx.pagerank(G, weight="weight")
sorted_pr = sorted(pr.items(), key=lambda item: item[1], reverse=True)
influence_leader = sorted_pr[0][0]
influence_score = sorted_pr[0][1]

print(f"1. Volume Leader (CMS): {volume_leader} with ~{volume_count} mentions")
print(
    f"""2. Influence Leader (PageRank): {
        influence_leader
    } with score {influence_score:.4f}"""
)
print(f"3. Graph Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")

# --- Verification ---
if volume_leader != influence_leader:
    print(
        "\n>>> SUCCESS! System correctly identified different users for Volume vs Influence."
    )
    print(f"    '{volume_leader}' is LOUD (Spamming).")
    print(f"    '{influence_leader}' is IMPORTANT (Receiving attention).")
else:
    print("\n>>> Anomaly: Same user is both Loud and Influential.")
