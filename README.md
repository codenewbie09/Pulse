# Pulse: Real-Time Network Analysis Engine

A system designed to analyze high-velocity data streams by combining **Probabilistic Data Structures** (for efficiency) with **Graph Theory** (for structural insight).

Pulse solves two major problems in real-time analytics:
1.  **Space Constraint:** Tracking frequencies in massive streams without running out of RAM.
2.  **Context Gap:** Distinguishing between users who are simply "Loud" (High Volume/Spam) and users who are "Important" (High Authority/Influence).

## The Problem: Volume vs. Influence

In social networks, activity does not equal authority.
*   **The Spammer:** Posts 1,000 times but nobody replies. (High Volume, Low Influence).
*   **The Celebrity:** Posts 1 time but receives 1,000 replies. (Low Volume, High Influence).

Standard analytics often fail to distinguish these two. Pulse uses a dual-algorithm approach to separate them.

## How It Works

Pulse integrates concepts from **Algorithms in the Real World (CSD 482)** and **Social & Information Networks (CSD 363)**.

### 1. Count-Min Sketch (Volume Tracking)
A probabilistic data structure that tracks event frequencies using a fixed-size matrix.
*   **Key Feature:** Constant memory usage ($O(1)$).
*   **Result:** Can process 1 million events using only ~40KB of RAM.
*   **Identifies:** The "Loudest" users (The Spammers).

### 2. PageRank on Directed Graphs (Influence Tracking)
Models user interactions as a Directed Graph where edges represent the flow of attention.
*   **Key Feature:** Uses `nx.DiGraph` to distinguish "Talking At" vs. "Being Talked About."
*   **Result:** Identifies nodes with the highest In-Degree and structural authority.
*   **Identifies:** The "Most Important" users (The Celebrities).

## Project Structure

*   `Count_Min_Sketch.py`: Implementation of the probabilistic frequency counter.
*   `main.py`: The core simulation engine and CLI output.
*   `app.py`: A Streamlit dashboard for visualizing the results.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/yourusername/pulse.git
    cd pulse
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Run the CLI Simulation
To see the terminal output comparing Volume vs. Influence:
```bash
python main.py
```

### Run the Dashboard
To launch the interactive Streamlit web app:
```bash
streamlit run app.py
```

## Results: The "Spammer vs. Celebrity" Experiment

The system was tested against a simulated stream containing two specific archetypes:

1.  **Chatter Box (The Spammer):** Active 10% of the time, initiating interactions.
2.  **The Celebrity:** Passive, receiving interactions from 10% of the network.

**Outcome:**
*   **Count-Min Sketch:** Correctly identified `chatter_box_99` as the **Volume Leader** (~500 mentions).
*   **PageRank:** Correctly identified `the_celebrity` as the **Influence Leader** (Highest Score).

This demonstrates Pulse's ability to filter out noise (spam) and highlight true signal (authority).

## Tech Stack

*   **Language:** Python
*   **Algorithms:** Count-Min Sketch, MinHash, PageRank
*   **Graph Processing:** NetworkX
*   **Visualization:** Streamlit, Plotly
*   **Memory Profiling:** psutil

## Math & Theory

For a deep dive into the mathematical foundations (including the CMS update rules and the PageRank recursive formula), see the full technical report included in this repository.

## License

MIT License

---
**Built by Prateek Agrawal**
```


This README is structured to guide a visitor from the high-level concept -> the technical solution -> the proof (results) -> how to use it. It highlights your specific achievement (The Experiment) prominently.
